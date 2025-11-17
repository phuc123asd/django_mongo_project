from rest_framework_mongoengine import serializers
from api.models.customer import Customer

# Kế thừa từ mongo_serializers.DocumentSerializer thay vì serializers.ModelSerializer
class CustomerSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {  # Làm optional cho update
            'password': {'required': False, 'write_only': True},
            'email': {'required': False},  # Nếu không cho update email
            # Thêm tương tự cho các field khác nếu cần
        }