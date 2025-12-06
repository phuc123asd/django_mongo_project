from rest_framework_mongoengine import serializers as me_serializers
from api.models.brand import Brand

class BrandSerializer(me_serializers.DocumentSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
