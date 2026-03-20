from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from typing import Any
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from api.models.product import Product
from api.models.productdetail import ProductDetail
from api.serializers.product import ProductSerializer
from api.serializers.productdetail import ProductDetailSerializer

def _objects(model: Any) -> Any:
    return model.objects

@api_view(['GET'])
def product_list(request):
    products = _objects(Product).all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, product_id):
    try:
        product = _objects(Product).get(id=ObjectId(product_id))
    except DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    product_data = dict(ProductSerializer(product).data)
    product_detail = _objects(ProductDetail)(product=product).first()
    product_data['detail'] = ProductDetailSerializer(product_detail).data if product_detail else {}
    return Response(product_data)
