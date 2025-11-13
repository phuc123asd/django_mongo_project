# your_app/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated # <-- Đối với phiên bản an toàn
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist
from api.models.order import Order
from api.serializers.order import OrderSerializer
from mongoengine.errors import DoesNotExist, ValidationError

# --- PHIÊN BẢN AN TOÀN (KHUYẾN NGHỊ) ---
# Yêu cầu người dùng phải đăng nhập. Frontend cần gửi kèm cookie.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_by_customer(request, customer_id):
    """
    API endpoint để lấy danh sách đơn hàng của một khách hàng.
    Yêu cầu xác thực người dùng.
    """
    try:
        # Lấy tất cả đơn hàng của khách hàng, sắp xếp theo ngày tạo mới nhất
        orders = Order.objects.filter(customer=customer_id).order_by('-created_at')
        
        # Sử dụng many=True vì chúng ta đang serialize một danh sách các đối tượng
        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# --- PHIÊN BẢN KHÔNG AN TOÀN (HOẠT ĐỘNG NGAY VỚI FRONTEND HIỆN TẠI) ---
# Không yêu cầu xác thực. Bất kỳ ai cũng có thể xem đơn hàng nếu có ID.
# CẢNH BÁO: Đây là lỗ hổng bảo mật. Chỉ dùng cho mục đích phát triển.
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # <-- XÓC hoặc COMMENT dòng này
def get_orders_by_customer(request, customer_id):
    """
    API endpoint để lấy danh sách đơn hàng của một khách hàng.
    CẢNH BÁO: View này KHÔNG YÊU CẦU XÁC THỰC.
    """
    try:
        orders = Order.objects.filter(customer=customer_id).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# your_app/views.py

@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # <-- XÓC hoặc COMMENT dòng này
def get_order_detail(request, order_id):
    """
    API endpoint để lấy thông tin chi tiết của một đơn hàng.
    CẢNH BÁO: View này KHÔNG YÊU CẦU XÁC THỰC.
    """
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except DoesNotExist:
        return Response(
            {"error": "Không tìm thấy đơn hàng."},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValidationError:
        return Response(
            {"error": "ID đơn hàng không hợp lệ."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
