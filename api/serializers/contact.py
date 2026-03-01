from rest_framework_mongoengine import serializers
from api.models.contact import Contact

class ContactSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'is_read', 'reply']

class ContactListSerializer(serializers.DocumentSerializer):
    """Serializer để hiển thị danh sách contact cho admin"""
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'created_at', 'is_read']
