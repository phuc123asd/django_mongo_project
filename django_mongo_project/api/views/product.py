from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from api.models.product import Product
from api.models.productdetail import ProductDetail
from api.serializers.product import ProductSerializer
from api.serializers.productdetail import ProductDetailSerializer
from api.decorators.admin_decorators import require_admin_auth
from mongoengine.errors import DoesNotExist, ValidationError
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def product_list(request):
    """Lấy danh sách tất cả sản phẩm (public)."""
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, product_id):
    """Lấy chi tiết một sản phẩm (public)."""
    try:
        product = Product.objects.get(id=ObjectId(product_id))
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    product_data = ProductSerializer(product).data
    product_detail = ProductDetail.objects(product=product).first()
    product_data['detail'] = ProductDetailSerializer(product_detail).data if product_detail else {}
    return Response(product_data)


@api_view(['POST'])
@require_admin_auth
def product_create(request):
    """Tạo sản phẩm mới (admin only)."""
    try:
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product = serializer.save()
            logger.info(f"Admin {request.session.get('admin_email')} created product: {product.name}")
            
            return Response(
                {
                    "message": "Product created successfully",
                    "product": ProductSerializer(product).data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT', 'PATCH'])
@require_admin_auth
def product_update(request, product_id):
    """Cập nhật sản phẩm (admin only)."""
    try:
        product = Product.objects.get(id=ObjectId(product_id))
    except DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        partial = request.method == 'PATCH'
        serializer = ProductSerializer(product, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_product = serializer.save()
            logger.info(f"Admin {request.session.get('admin_email')} updated product: {updated_product.name}")
            
            return Response(
                {
                    "message": "Product updated successfully",
                    "product": ProductSerializer(updated_product).data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except ValidationError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error updating product: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@require_admin_auth
def product_delete(request, product_id):
    """Xóa sản phẩm (admin only)."""
    try:
        product = Product.objects.get(id=ObjectId(product_id))
        product_name = product.name
        product.delete()
        
        logger.info(f"Admin {request.session.get('admin_email')} deleted product: {product_name}")
        
        return Response(
            {"message": f"Product '{product_name}' deleted successfully"},
            status=status.HTTP_200_OK
        )
        
    except DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error deleting product: {str(e)}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
