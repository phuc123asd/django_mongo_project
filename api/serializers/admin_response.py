# api/serializers/admin_response.py

from rest_framework import serializers
from api.models.admin_response import AdminResponse

class AdminResponseSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    review_id = serializers.CharField()
    response = serializers.CharField()
    admin_id = serializers.CharField()
    admin_name = serializers.CharField()
    created_at = serializers.DateTimeField(format='iso-8601', read_only=True)
    updated_at = serializers.DateTimeField(format='iso-8601', read_only=True)
    response_type = serializers.CharField(required=False, default='manual')

    def get_id(self, obj):
        return str(obj.id)

    def create(self, validated_data):
        """
        Tạo và trả về một instance `AdminResponse` mới
        """
        response = AdminResponse.objects.create(**validated_data)
        return response