from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from api.models.product import Product
from api.models.productdetail import ProductDetail
from api.serializers.product import ProductSerializer
from api.serializers.productdetail import ProductDetailSerializer

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=ObjectId(product_id))
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    product_data = ProductSerializer(product).data
    product_detail = ProductDetail.objects(product=product).first()
    product_data['detail'] = ProductDetailSerializer(product_detail).data if product_detail else {}
    return Response(product_data)
