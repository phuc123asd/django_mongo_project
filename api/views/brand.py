from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from typing import Any
from bson import ObjectId
from api.models.brand import Brand
from api.serializers.brand import BrandSerializer

def _objects(model: Any) -> Any:
    return model.objects

@api_view(['GET'])
def brand_list(request):
        brands = _objects(Brand).all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
