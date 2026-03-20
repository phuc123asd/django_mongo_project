from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from typing import Any
from bson import ObjectId
from api.models.category import Category
from api.serializers.category import CategorySerializer

def _objects(model: Any) -> Any:
    return model.objects

@api_view(['GET'])
def category_list(request):
    categories = _objects(Category).all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
