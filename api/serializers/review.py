# api/serializers/review.py

from rest_framework import serializers
from typing import Any
from api.models.review import Review
from api.models.customer import Customer

def _objects(model: Any) -> Any:
    return model.objects

class ReviewSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    product_id = serializers.CharField()
    customer_id = serializers.CharField()
    rating = serializers.IntegerField()
    comment = serializers.CharField()
    
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    def get_user_name(self, obj):
        customer = _objects(Customer)(id=obj.customer_id).first()
        if not customer:
            return "Người dùng không tìm thấy"
        first_name = getattr(customer, 'first_name', '')
        last_name = getattr(customer, 'last_name', '')
        return f"{first_name} {last_name}".strip()

    def get_user_avatar(self, obj):
        customer = _objects(Customer)(id=obj.customer_id).first()
        if not customer:
            return "https://ui-avatars.com/api/?name=Unknown&background=random"
        first_name = getattr(customer, 'first_name', '')
        last_name = getattr(customer, 'last_name', '')
        name = f"{first_name}+{last_name}".strip()
        return f"https://ui-avatars.com/api/?name={name}&background=random"

    # --- THÊM PHƯƠNG THỨC NÀY ---
    def create(self, validated_data):
        """
        Tạo và trả về một instance `Review` mới, được tạo từ `validated_data`.
        """
        # validated_data là một dictionary chứa các trường đã được xác thực:
        # {'product_id': '...', 'customer_id': '...', 'rating': 5, 'comment': '...'}
        
        review = _objects(Review).create(**validated_data)
        return review
