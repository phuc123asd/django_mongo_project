from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist, ValidationError
from api.serializers.order import OrderSerializer, OrderDetailSerializer, CreateOrderSerializer
from api.models.order import Order, OrderItem
from api.models.product import Product
from api.models.customer import Customer
from api.decorators.decorators import require_session_auth
from api.decorators.admin_decorators import require_admin_auth
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@require_session_auth
def get_orders_by_customer(request, customer_id):
    """
    Lấy danh sách đơn hàng của một khách hàng (customer only, authenticated).
    """
    # if request.session.get('user_id') != customer_id:
    #     return Response(
    #         {"error": "Bạn không có quyền xem đơn hàng này."},
    #         status=status.HTTP_403_FORBIDDEN
    #     )
    
    try:
        orders = Order.objects.filter(customer=customer_id).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_order_detail(request, order_id):
    """
    Lấy chi tiết đơn hàng (public for now, should add auth later).
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
        logger.error(f"Error fetching order detail: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def create_order(request):
    """
    Tạo đơn hàng mới.
    """
    customer_id = request.data.get('customer')
    if not customer_id:
        return Response(
            {"error": "Thiếu thông tin 'customer' trong yêu cầu."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {"error": f"Không tìm thấy khách hàng với ID: {customer_id}"},
            status=status.HTTP_404_NOT_FOUND
        )

    order_data = request.data.copy()
    order_data.pop('customer', None)

    serializer = CreateOrderSerializer(data=order_data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        order_items_data = validated_data['items']

        total_price = sum(item['price'] * item['quantity'] for item in order_items_data)

        try:
            order = Order.objects.create(
                customer=customer,
                items=[OrderItem(**item) for item in order_items_data],
                total_price=total_price,
                shipping_address=validated_data['shipping_address'],
                city=validated_data['city'],
                province=validated_data['province'],
                postal_code=validated_data['postal_code'],
                phone=validated_data['phone'],
                status='Đang Xử Lý'
            )

            response_serializer = OrderDetailSerializer(order)
            logger.info(f"Order created: {order.id}")
            
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return Response(
                {"error": "Đã xảy ra lỗi khi tạo đơn hàng. Vui lòng thử lại."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@require_admin_auth
def get_all_orders(request):
    """
    Lấy tất cả đơn hàng (admin only).
    """
    try:
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching all orders: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH'])
@require_admin_auth
def update_order_status(request, order_id):
    """
    Cập nhật trạng thái đơn hàng (admin only).
    """
    try:
        order = Order.objects.get(id=order_id)
    except DoesNotExist:
        return Response(
            {"error": "Không tìm thấy đơn hàng."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    new_status = request.data.get('status')
    if not new_status:
        return Response(
            {"error": "Thiếu trường 'status'."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if new_status not in Order.STATUS_CHOICES:
        return Response(
            {"error": f"Trạng thái không hợp lệ. Chọn một trong: {Order.STATUS_CHOICES}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    order.status = new_status
    order.save()
    
    logger.info(f"Admin {request.session.get('admin_email')} updated order {order_id} status to {new_status}")
    
    serializer = OrderSerializer(order)
    return Response(
        {
            "message": "Cập nhật trạng thái đơn hàng thành công.",
            "order": serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
@require_admin_auth
def delete_order(request, order_id):
    """
    Xóa đơn hàng (admin only).
    """
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        
        logger.info(f"Admin {request.session.get('admin_email')} deleted order {order_id}")
        
        return Response(
            {"message": "Đơn hàng đã được xóa thành công."},
            status=status.HTTP_200_OK
        )
    except DoesNotExist:
        return Response(
            {"error": "Không tìm thấy đơn hàng."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error deleting order: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@require_admin_auth
def get_order_statistics(request):
    """
    Lấy thống kê đơn hàng (admin only).
    """
    try:
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='Đang Xử Lý').count()
        shipping_orders = Order.objects.filter(status='Đang Vận Chuyển').count()
        completed_orders = Order.objects.filter(status='Đã Giao').count()
        
        total_revenue = sum(float(order.total_price) for order in Order.objects.all())
        
        return Response({
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "shipping_orders": shipping_orders,
            "completed_orders": completed_orders,
            "total_revenue": total_revenue
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching order statistics: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
