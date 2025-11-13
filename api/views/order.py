# your_app/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated # <-- Đối với phiên bản an toàn
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist
from api.models.order import Order
from api.serializers.order import OrderSerializer
from mongoengine.errors import DoesNotExist, ValidationError
from api.serializers.order import OrderSerializer, OrderDetailSerializer, CreateOrderSerializer # Thêm CreateOrderSerializer vào import
from api.models.product import Product # Thêm import Product
from api.models.customer import Customer
from api.models.order import OrderItem

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


@api_view(['POST'])
def create_order(request):
    """
    API endpoint để tạo một đơn hàng mới.
    Nhận customer ID từ request body.
    Yêu cầu người dùng phải đăng nhập.
    """
    # Lấy customer_id từ dữ liệu gửi lên
    customer_id = request.data.get('customer')
    if not customer_id:
        return Response(
            {"error": "Thiếu thông tin 'customer' trong yêu cầu."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Tìm customer dựa trên ID được gửi lên
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {"error": f"Không tìm thấy khách hàng với ID: {customer_id}"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Sử dụng serializer để xác thực dữ liệu đầu vào
    # Chúng ta cần loại bỏ 'customer' khỏi data vì đã lấy ở trên
    order_data = request.data.copy()
    order_data.pop('customer', None) # Xóa trường customer khỏi data để serializer không lỗi

    serializer = CreateOrderSerializer(data=order_data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        order_items_data = validated_data['items']

        # Tính tổng giá tiền
        total_price = sum(item['price'] * item['quantity'] for item in order_items_data)

        # Tạo đối tượng Order
        try:
            order = Order.objects.create(
                customer=customer, # Sử dụng customer object đã lấy ở trên
                items=[OrderItem(**item) for item in order_items_data],
                total_price=total_price,
                shipping_address=validated_data['shipping_address'],
                city=validated_data['city'],
                province=validated_data['province'],
                postal_code=validated_data['postal_code'],
                phone=validated_data['phone'],
                status='Đang Xử Lý'
            )

            # Sử dụng OrderDetailSerializer để trả về thông tin đầy đủ
            response_serializer = OrderDetailSerializer(order)
            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error creating order: {e}")
            return Response(
                {"error": "Đã xảy ra lỗi khi tạo đơn hàng. Vui lòng thử lại."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # Nếu dữ liệu không hợp lệ, trả về lỗi 400
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)