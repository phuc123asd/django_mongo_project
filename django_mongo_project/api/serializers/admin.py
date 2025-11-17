from rest_framework import serializers  # DRF SerializerMethodField
from rest_framework_mongoengine.serializers import DocumentSerializer
from api.models.admin import Admin

class AdminSerializer(DocumentSerializer):
    """
    Serializer cho Admin model.
    """
    id = serializers.SerializerMethodField()  # DRF SerializerMethodField
    
    class Meta:
        model = Admin
        fields = ['id', 'email', 'username', 'full_name', 'role', 'is_active', 'created_at', 'last_login']
        read_only_fields = ['id', 'created_at', 'last_login']
    
    def get_id(self, obj):
        return str(obj.pk)
