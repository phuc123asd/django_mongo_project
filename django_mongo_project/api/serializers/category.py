from rest_framework_mongoengine import serializers as me_serializers
from api.models.category import Category

class CategorySerializer(me_serializers.DocumentSerializer):
    class Meta:
        model = Category
        fields = '__all__'
