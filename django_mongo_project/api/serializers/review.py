# api/serializers/review.py

from rest_framework import serializers
from api.models.review import Review
from api.models.customer import Customer

class ReviewSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    product_id = serializers.CharField()
    customer_id = serializers.CharField()
    rating = serializers.IntegerField()
    comment = serializers.CharField()
    
    # Thêm các field mới cho auto-response
    # admin_response = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # response_generated_at = serializers.DateTimeField(format='iso-8601', read_only=True, required=False)
    
    created_at = serializers.DateTimeField(format='iso-8601', read_only=True)
    updated_at = serializers.DateTimeField(format='iso-8601', read_only=True)

    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    def get_user_name(self, obj):
        try:
            customer = Customer.objects.get(id=obj.customer_id)
            first_name = getattr(customer, 'first_name', '')
            last_name = getattr(customer, 'last_name', '')
            return f"{first_name} {last_name}".strip()
        except Customer.DoesNotExist:
            return "Người dùng không tìm thấy"

    def get_user_avatar(self, obj):
        try:
            customer = Customer.objects.get(id=obj.customer_id)
            first_name = getattr(customer, 'first_name', '')
            last_name = getattr(customer, 'last_name', '')
            name = f"{first_name}+{last_name}".strip()
            return f"https://ui-avatars.com/api/?name={name}&background=random"
        except Customer.DoesNotExist:
            return "https://ui-avatars.com/api/?name=Unknown&background=random"

    # --- THÊM PHƯƠNG THỨC NÀY ---
    def create(self, validated_data):
        """
        Tạo và trả về một instance `Review` mới, được tạo từ `validated_data`.
        """
        # validated_data là một dictionary chứa các trường đã được xác thực:
        # {'product_id': '...', 'customer_id': '...', 'rating': 5, 'comment': '...'}
        
        review = Review.objects.create(**validated_data)
        return review
