# api/serializers/review_response.py

from rest_framework import serializers
from api.models.review_response import ReviewResponse

class ReviewResponseSerializer(serializers.Serializer):
    """
    Serializer để validate và chuyển đổi dữ liệu của model ReviewResponse.
    """
    id = serializers.SerializerMethodField(read_only=True)
    review_id = serializers.CharField(required=True)
    responder_id = serializers.CharField(required=True)
    responder_name = serializers.CharField(required=True)
    response_text = serializers.CharField(required=True)
    
    created_at = serializers.DateTimeField(format='iso-8601', read_only=True)
    updated_at = serializers.DateTimeField(format='iso-8601', read_only=True)

    def get_id(self, obj):
        """Chuyển đổi ObjectId của MongoEngine thành chuỗi."""
        return str(obj.id)

    def create(self, validated_data):
        """
        Tạo và trả về một instance `ReviewResponse` mới từ dữ liệu đã được xác thực.
        """
        response = ReviewResponse.objects.create(**validated_data)
        return response
