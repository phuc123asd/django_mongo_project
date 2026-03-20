"""
MoMo Payment Integration
Docs: https://developers.momo.vn/v3/docs/payment/api/payment-api/create-order
Sandbox: https://test-payment.momo.vn/v2/gateway/api/create
"""

import uuid
import hmac
import hashlib
from datetime import datetime
from typing import Any

import httpx
from decouple import config
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist, ValidationError

from api.models.order import Order

def _env_str(name: str, default: str) -> str:
    value = config(name, default=default)
    return str(value)

def _objects(model: Any) -> Any:
    return model.objects

# ── Cấu hình MoMo (đọc từ .env) ──────────────────────────────────────────────
MOMO_PARTNER_CODE = _env_str('MOMO_PARTNER_CODE', 'MOMO')
MOMO_ACCESS_KEY   = _env_str('MOMO_ACCESS_KEY', 'F8BBA842ECF85')
MOMO_SECRET_KEY   = _env_str('MOMO_SECRET_KEY', 'K951B6PE1waDMi640xX08PD3vg6EkVlz')
MOMO_ENDPOINT     = _env_str('MOMO_ENDPOINT', 'https://test-payment.momo.vn/v2/gateway/api/create')

FRONTEND_URL = _env_str('FRONTEND_URL', 'http://localhost:3000')
BACKEND_URL  = _env_str('BACKEND_URL', 'http://127.0.0.1:8000')

# Tỉ giá quy đổi USD → VND (chỉnh sửa nếu hệ thống đã dùng VND)
USD_TO_VND = config('USD_TO_VND', default=25000, cast=int)
MIN_PAYMENT_VND = 1000
MAX_PAYMENT_VND = 50000000


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


def _validate_amount_range(amount_vnd: int):
    if amount_vnd < MIN_PAYMENT_VND:
        return (
            f"Số tiền quy đổi ({amount_vnd:,} VND) nhỏ hơn mức tối thiểu "
            f"{MIN_PAYMENT_VND:,} VND."
        )
    if amount_vnd > MAX_PAYMENT_VND:
        return (
            f"Số tiền quy đổi ({amount_vnd:,} VND) vượt mức tối đa "
            f"{MAX_PAYMENT_VND:,} VND."
        )
    return ""


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
        order = _objects(Order).get(id=order_id)
    except (DoesNotExist, ValidationError):
        return Response({'error': 'Không tìm thấy đơn hàng'}, status=status.HTTP_404_NOT_FOUND)

    # Chuyển đổi sang VND (MoMo yêu cầu số nguyên, đơn vị VND)
    amount_vnd = int(float(str(order.total_price)) * USD_TO_VND)
    amount_error = _validate_amount_range(amount_vnd)
    if amount_error:
        return Response(
            {
                "error": amount_error,
                "amount_vnd": amount_vnd,
                "min_vnd": MIN_PAYMENT_VND,
                "max_vnd": MAX_PAYMENT_VND,
                "exchange_rate": USD_TO_VND,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    request_id   = str(uuid.uuid4())
    # Thêm timestamp vào orderId để tránh trùng khi retry
    momo_order_id = f"{order_id}_{int(datetime.now().timestamp())}"
    order_info   = f"Thanh toan don hang {str(order_id)[-8:]}"
    redirect_url = f"{FRONTEND_URL}/momo-return"
    # IPN cần HTTPS public URL — khi dev local dùng placeholder (MoMo sandbox không ping lại)
    ipn_url      = config('MOMO_IPN_URL', default='https://webhook.site/momo-ipn-placeholder')
    extra_data   = ""
    request_type = "payWithMethod"

    # Chữ ký v2 — các key phải theo thứ tự alphabet
    # MoMo yêu cầu các key phải đúng thứ tự alphabet
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
        "accessKey": MOMO_ACCESS_KEY,
        "requestId": request_id,
        "amount": str(amount_vnd),
        "orderId": momo_order_id,
        "orderInfo": order_info,
        "redirectUrl": redirect_url,
        "ipnUrl": ipn_url,
        "extraData": extra_data,
        "requestType": request_type,
        "autoCapture": True,
        "lang": "vi",
        "signature": signature,
    }

    try:
        print(f"[MoMo] Bắt đầu tạo thanh toán cho order_id: {order_id}")
        print(f"[MoMo] Payload gửi lên: {payload}")
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(str(MOMO_ENDPOINT), json=payload)
        result = resp.json()
        print(f"[MoMo] Response từ MoMo: {result}")

        if result.get('resultCode') == 0:
            print(f"[MoMo] Tạo thanh toán thành công cho order_id: {order_id}, payUrl: {result['payUrl']}")
            return Response(
                {
                    'payUrl':   result['payUrl'],
                    'deeplink': result.get('deeplink', ''),
                    'qrCodeUrl': result.get('qrCodeUrl', ''),
                    'message': result.get('message', '')
                },
                status=status.HTTP_200_OK
            )
        else:
            print(f"[MoMo] Tạo thanh toán thất bại cho order_id: {order_id}, message: {result.get('message', '')}")
            return Response(
                {'error': result.get('message', 'MoMo trả về lỗi'), 'momo_result': result},
                status=status.HTTP_400_BAD_REQUEST
            )
    except httpx.TimeoutException:
        print(f"[MoMo] Timeout khi gọi API MoMo cho order_id: {order_id}")
        return Response({'error': 'MoMo API không phản hồi (timeout). Vui lòng thử lại.'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
    except Exception as e:
        print(f"[MoMo] Lỗi không xác định khi tạo thanh toán cho order_id: {order_id}: {str(e)}")
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

    print(f"[MoMo-IPN] Nhận IPN từ MoMo: {data}")
    if data.get('signature') != expected_sig:
        print(f"[MoMo-IPN] Invalid signature cho orderId: {data.get('orderId', '')}")
        return Response({'message': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    momo_order_id = data.get('orderId', '')
    original_order_id = momo_order_id.rsplit('_', 1)[0] if '_' in momo_order_id else momo_order_id
    result_code = data.get('resultCode')

    try:
        order = _objects(Order).get(id=original_order_id)
        if result_code == 0:
            print(f"[MoMo-IPN] Thanh toán thành công cho order_id: {original_order_id}")
            order.payment_status = 'paid'
        else:
            print(f"[MoMo-IPN] Thanh toán thất bại cho order_id: {original_order_id}, result_code: {result_code}")
            order.payment_status = 'failed'
        order.save()
    except Exception as e:
        print(f"[MoMo-IPN] Lỗi khi cập nhật trạng thái đơn hàng: {str(e)}")
        pass

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

    print(f"[MoMo-Confirm] Nhận xác nhận thanh toán từ redirect: {data}")
    if data.get('signature') != expected_sig:
        print(f"[MoMo-Confirm] Invalid signature cho orderId: {data.get('orderId', '')}")
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    momo_order_id = data.get('orderId', '')
    original_order_id = momo_order_id.rsplit('_', 1)[0] if '_' in momo_order_id else momo_order_id
    result_code = int(data.get('resultCode', -1))

    try:
        order = _objects(Order).get(id=original_order_id)
        order.payment_status = 'paid' if result_code == 0 else 'failed'
        order.save()
        print(f"[MoMo-Confirm] Cập nhật trạng thái đơn hàng {original_order_id}: {order.payment_status}")
        return Response({'payment_status': order.payment_status}, status=status.HTTP_200_OK)
    except (DoesNotExist, ValidationError) as e:
        print(f"[MoMo-Confirm] Không tìm thấy đơn hàng {original_order_id}: {str(e)}")
        return Response({'error': 'Không tìm thấy đơn hàng'}, status=status.HTTP_404_NOT_FOUND)


# ── Kiểm tra trạng thái thanh toán của đơn hàng ─────────────────────────────
@api_view(['GET'])
def get_payment_status(request, order_id):
    """
    GET /api/order/momo/payment-status/<order_id>/
    Frontend gọi để kiểm tra payment_status sau khi redirect về từ MoMo.
    """
    try:
        order = _objects(Order).get(id=order_id)
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
