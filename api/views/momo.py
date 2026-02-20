"""
MoMo Payment Integration
Docs: https://developers.momo.vn/v3/docs/payment/api/payment-api/create-order
Sandbox: https://test-payment.momo.vn/v2/gateway/api/create
"""

import uuid
import hmac
import hashlib
from datetime import datetime

import httpx
from decouple import config
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist, ValidationError

from api.models.order import Order

# ── Cấu hình MoMo (đọc từ .env) ──────────────────────────────────────────────
MOMO_PARTNER_CODE = config('MOMO_PARTNER_CODE', default='MOMO')
MOMO_ACCESS_KEY   = config('MOMO_ACCESS_KEY',   default='F8BBA842ECF85')
MOMO_SECRET_KEY   = config('MOMO_SECRET_KEY',   default='K951B6PE1waDMi640xX08PD3vg6EkVlz')
MOMO_ENDPOINT     = config('MOMO_ENDPOINT',     default='https://test-payment.momo.vn/v2/gateway/api/create')

FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:5173')
BACKEND_URL  = config('BACKEND_URL',  default='http://127.0.0.1:8001')

# Tỉ giá quy đổi USD → VND (chỉnh sửa nếu hệ thống đã dùng VND)
USD_TO_VND = config('USD_TO_VND', default=25000, cast=int)


def _build_signature(data: dict) -> str:
    """Tạo chữ ký HMAC-SHA256 từ dict đã sắp xếp theo thứ tự alphabet của key."""
    raw = "&".join(f"{k}={v}" for k, v in sorted(data.items()))
    return hmac.new(
        MOMO_SECRET_KEY.encode('utf-8'),
        raw.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def _create_signature(raw_signature: str) -> str:
    return hmac.new(
        MOMO_SECRET_KEY.encode('utf-8'),
        raw_signature.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


# ── Tạo yêu cầu thanh toán ───────────────────────────────────────────────────
@api_view(['POST'])
def create_momo_payment(request):
    """
    POST /api/order/momo/create-payment/
    Body: { "order_id": "<order_mongo_id>" }
    Trả về: { "payUrl": "...", "deeplink": "..." }
    """
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({'error': 'Thiếu order_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(id=order_id)
    except (DoesNotExist, ValidationError):
        return Response({'error': 'Không tìm thấy đơn hàng'}, status=status.HTTP_404_NOT_FOUND)

    # Chuyển đổi sang VND (MoMo yêu cầu số nguyên, đơn vị VND)
    amount_vnd = int(float(str(order.total_price)) * USD_TO_VND)
    # Đảm bảo tối thiểu 1000 VND
    amount_vnd = max(amount_vnd, 1000)

    request_id   = str(uuid.uuid4())
    # Thêm timestamp vào orderId để tránh trùng khi retry
    momo_order_id = f"{order_id}_{int(datetime.now().timestamp())}"
    order_info   = f"Thanh toan don hang #{str(order_id)[-8:]}"
    redirect_url = f"{FRONTEND_URL}/momo-return"
    # IPN cần HTTPS public URL — khi dev local dùng placeholder (MoMo sandbox không ping lại)
    ipn_url      = config('MOMO_IPN_URL', default='https://webhook.site/momo-ipn-placeholder')
    extra_data   = ""
    request_type = "payWithMethod"

    # Chữ ký v2 — các key phải theo thứ tự alphabet
    raw_signature = (
        f"accessKey={MOMO_ACCESS_KEY}"
        f"&amount={amount_vnd}"
        f"&extraData={extra_data}"
        f"&ipnUrl={ipn_url}"
        f"&orderId={momo_order_id}"
        f"&orderInfo={order_info}"
        f"&partnerCode={MOMO_PARTNER_CODE}"
        f"&redirectUrl={redirect_url}"
        f"&requestId={request_id}"
        f"&requestType={request_type}"
    )
    signature = _create_signature(raw_signature)

    payload = {
        "partnerCode": MOMO_PARTNER_CODE,
        "accessKey":   MOMO_ACCESS_KEY,
        "requestId":   request_id,
        "amount":      amount_vnd,
        "orderId":     momo_order_id,
        "orderInfo":   order_info,
        "redirectUrl": redirect_url,
        "ipnUrl":      ipn_url,
        "extraData":   extra_data,
        "requestType": request_type,
        "signature":   signature,
        "lang":        "vi",
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(MOMO_ENDPOINT, json=payload)
        result = resp.json()

        if result.get('resultCode') == 0:
            return Response(
                {
                    'payUrl':   result['payUrl'],
                    'deeplink': result.get('deeplink', ''),
                    'qrCodeUrl': result.get('qrCodeUrl', ''),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': result.get('message', 'MoMo trả về lỗi'), 'momo_result': result},
                status=status.HTTP_400_BAD_REQUEST
            )
    except httpx.TimeoutException:
        return Response({'error': 'MoMo API không phản hồi (timeout). Vui lòng thử lại.'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ── IPN (Instant Payment Notification) ───────────────────────────────────────
@api_view(['POST'])
def momo_ipn(request):
    """
    POST /api/order/momo/ipn/
    MoMo gọi endpoint này sau khi người dùng thanh toán xong.
    Cần BACKEND_URL trỏ ra internet (dùng ngrok khi dev local).
    """
    data = request.data

    # Xác thực chữ ký từ MoMo
    raw_signature = (
        f"accessKey={MOMO_ACCESS_KEY}"
        f"&amount={data.get('amount')}"
        f"&extraData={data.get('extraData', '')}"
        f"&message={data.get('message', '')}"
        f"&orderId={data.get('orderId', '')}"
        f"&orderInfo={data.get('orderInfo', '')}"
        f"&orderType={data.get('orderType', '')}"
        f"&partnerCode={data.get('partnerCode', '')}"
        f"&payType={data.get('payType', '')}"
        f"&requestId={data.get('requestId', '')}"
        f"&responseTime={data.get('responseTime', '')}"
        f"&resultCode={data.get('resultCode', '')}"
        f"&transId={data.get('transId', '')}"
    )
    expected_sig = _create_signature(raw_signature)

    if data.get('signature') != expected_sig:
        return Response({'message': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    # Lấy orderId gốc (trước khi thêm timestamp)
    momo_order_id = data.get('orderId', '')
    original_order_id = momo_order_id.rsplit('_', 1)[0] if '_' in momo_order_id else momo_order_id
    result_code = data.get('resultCode')

    try:
        order = Order.objects.get(id=original_order_id)
        if result_code == 0:   # Thanh toán thành công
            order.payment_status = 'paid'
        else:                  # Thanh toán thất bại / huỷ
            order.payment_status = 'failed'
        order.save()
    except Exception:
        pass  # Không trả lỗi để MoMo không retry mãi

    return Response({'message': 'ok'}, status=status.HTTP_200_OK)


# ── Xác nhận thanh toán từ redirect URL (thay thế IPN khi dev local) ────────
@api_view(['POST'])
def confirm_momo_payment(request):
    """
    POST /api/order/momo/confirm-payment/
    Frontend gọi sau khi MoMo redirect về, gửi lại các params từ URL.
    Backend xác thực chữ ký rồi cập nhật payment_status.
    """
    data = request.data

    # Xác thực chữ ký redirect từ MoMo (alphabet order)
    raw_signature = (
        f"accessKey={MOMO_ACCESS_KEY}"
        f"&amount={data.get('amount', '')}"
        f"&extraData={data.get('extraData', '')}"
        f"&message={data.get('message', '')}"
        f"&orderId={data.get('orderId', '')}"
        f"&orderInfo={data.get('orderInfo', '')}"
        f"&orderType={data.get('orderType', '')}"
        f"&partnerCode={data.get('partnerCode', '')}"
        f"&payType={data.get('payType', '')}"
        f"&requestId={data.get('requestId', '')}"
        f"&responseTime={data.get('responseTime', '')}"
        f"&resultCode={data.get('resultCode', '')}"
        f"&transId={data.get('transId', '')}"
    )
    expected_sig = _create_signature(raw_signature)

    if data.get('signature') != expected_sig:
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    momo_order_id = data.get('orderId', '')
    original_order_id = momo_order_id.rsplit('_', 1)[0] if '_' in momo_order_id else momo_order_id
    result_code = int(data.get('resultCode', -1))

    try:
        order = Order.objects.get(id=original_order_id)
        order.payment_status = 'paid' if result_code == 0 else 'failed'
        order.save()
        return Response({'payment_status': order.payment_status}, status=status.HTTP_200_OK)
    except (DoesNotExist, ValidationError):
        return Response({'error': 'Không tìm thấy đơn hàng'}, status=status.HTTP_404_NOT_FOUND)


# ── Kiểm tra trạng thái thanh toán của đơn hàng ─────────────────────────────
@api_view(['GET'])
def get_payment_status(request, order_id):
    """
    GET /api/order/momo/payment-status/<order_id>/
    Frontend gọi để kiểm tra payment_status sau khi redirect về từ MoMo.
    """
    try:
        order = Order.objects.get(id=order_id)
        return Response(
            {
                'order_id':       str(order.id),
                'payment_status': order.payment_status,
                'payment_method': order.payment_method,
                'status':         order.status,
            },
            status=status.HTTP_200_OK
        )
    except (DoesNotExist, ValidationError):
        return Response({'error': 'Không tìm thấy đơn hàng'}, status=status.HTTP_404_NOT_FOUND)
