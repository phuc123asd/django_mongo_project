from rest_framework_mongoengine import serializers
from api.models.productdetail import ProductDetail

class ProductDetailSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'
