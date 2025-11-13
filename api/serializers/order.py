# api/serializers/order.py
from rest_framework import serializers
from api.models.order import Order, OrderItem
from api.models.product import Product
from api.models.customer import Customer
from api.serializers.customer import CustomerSerializer

# --- Serializer cho các mặt hàng trong đơn hàng ---
class OrderItemSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    price = serializers.SerializerMethodField()

    def get_product(self, obj):
        # obj là một instance của OrderItem
        # obj.product là một ReferenceField, ta cần lấy ID của nó
        return str(obj.product)
    def get_price(self, obj):
        # QUAN TRỌNG: Chuyển đổi Decimal thành float
        # để JSON serialize nó thành một con số (number), không phải chuỗi (string)
        return float(obj.price)

# --- Serializer chính cho Order ---
class OrderSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    shipping_address = serializers.CharField()
    city = serializers.CharField()
    province = serializers.CharField()
    postal_code = serializers.CharField()
    phone = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_id(self, obj):
        # obj là một instance của Order
        # obj.id là một ObjectId, ta chỉ cần chuyển nó thành chuỗi
        return str(obj.id)

    def get_customer(self, obj):
        # obj.customer là một ReferenceField, ta cần lấy ID của nó
        return str(obj.customer.id)
    
    def get_total_price(self, obj):
        # obj.total_price là một Decimal, chuyển nó thành float để JSON serialize thành số
        return float(obj.total_price)

    def get_price(self, obj):
        # obj.price là một Decimal, chuyển nó thành float để JSON serialize thành số
        return float(obj.price)
class OrderDetailSerializer(OrderSerializer):
    customer = CustomerSerializer(read_only=True)
    
    def get_items(self, obj):
        # Lấy thông tin chi tiết của sản phẩm
        items = []
        for item in obj.items:
            try:
                product = Product.objects.get(id=item.product)
                items.append({
                    'product': {
                        'id': str(product.id),
                        'name': product.name,
                        'image': product.image,
                    },
                    'quantity': item.quantity,
                    'price': item.price
                })
            except Product.DoesNotExist:
                items.append({
                    'product': {
                        'id': str(item.product),
                        'name': 'Sản phẩm không tồn tại',
                        'image': '',
                    },
                    'quantity': item.quantity,
                    'price': item.price
                })
        return items