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

class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer dùng để xác thực dữ liệu khi tạo một đơn hàng mới.
    """
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()), # <-- SỬA LỖI: Thêm dấu '='
        write_only=True,
        required=True
    )
    shipping_address = serializers.CharField(max_length=255, required=True)
    city = serializers.CharField(max_length=100, required=True)
    province = serializers.CharField(max_length=100, required=True)
    postal_code = serializers.CharField(max_length=20, required=True)
    phone = serializers.CharField(max_length=20, required=True)

    def validate_items(self, items):
        """
        Kiểm tra danh sách các mặt hàng trong đơn hàng.
        - Đảm bảo không rỗng.
        - Đảm bảo mỗi item có 'product_id' và 'quantity'.
        - Kiểm tra sản phẩm có tồn tại không.
        """
        if not items:
            raise serializers.ValidationError("Đơn hàng phải có ít nhất một sản phẩm.")

        validated_items = []
        product_ids = []
        
        # Lấy tất cả product_id để kiểm tra tồn tại một lần (tối ưu)
        for item in items:
            product_id = item.get('product')
            if not product_id:
                raise serializers.ValidationError("Mỗi sản phẩm phải có 'product_id'.")
            product_ids.append(product_id)

        # Kiểm tra sự tồn tại của các sản phẩm
        existing_products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids)}
        
        for item in items:
            product_id = item.get('product')
            quantity_str = item.get('quantity') # Lấy quantity dưới dạng chuỗi trước

            # --- BẮT ĐẦU PHẦN SỬA ---
            try:
                # Cố gắng chuyển chuỗi thành số nguyên
                quantity = int(quantity_str)
            except (TypeError, ValueError):
                # Nếu không chuyển được (ví dụ quantity là "abc" hoặc null)
                raise serializers.ValidationError(f"Số lượng cho sản phẩm {product_id} phải là một số nguyên.")

            # Kiểm tra xem số lượng có lớn hơn 0 không
            if quantity <= 0:
                raise serializers.ValidationError(f"Số lượng cho sản phẩm {product_id} phải lớn hơn 0.")
            # --- KẾT THÚC PHẦN SỬA ---

            if product_id not in existing_products:
                raise serializers.ValidationError(f"Sản phẩm với ID {product_id} không tồn tại.")
            
            product = existing_products[product_id]
            validated_items.append({
                'product': product,
                'quantity': quantity, # Dùng biến 'quantity' đã được chuyển đổi
                'price': product.price
            })
        
        return validated_items   
