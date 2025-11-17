from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models.customer import Customer
from api.serializers.customer import CustomerSerializer
from api.decorators.admin_decorators import require_admin_auth
from mongoengine.errors import DoesNotExist
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@require_admin_auth
def get_all_customers(request):
    """
    Lấy danh sách tất cả khách hàng (admin only).
    """
    try:
        customers = Customer.objects.all().order_by('-id')
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@require_admin_auth
def delete_customer(request, customer_id):
    """
    Xóa khách hàng (admin only).
    """
    try:
        customer = Customer.objects.get(id=customer_id)
        customer_email = customer.email
        customer.delete()
        
        logger.info(f"Admin {request.session.get('admin_email')} deleted customer: {customer_email}")
        
        return Response(
            {"message": f"Khách hàng {customer_email} đã được xóa thành công."},
            status=status.HTTP_200_OK
        )
    except DoesNotExist:
        return Response(
            {"error": "Không tìm thấy khách hàng."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error deleting customer: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@require_admin_auth
def get_customer_statistics(request):
    """
    Lấy thống kê khách hàng (admin only).
    """
    try:
        total_customers = Customer.objects.count()
        
        return Response({
            "total_customers": total_customers
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching customer statistics: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
