# api/serializers/order.py
from rest_framework import serializers

from api.models.order import Order
from api.models.product import Product
from api.models.customer import Customer
from api.serializers.customer import CustomerSerializer


def _extract_product_id(item):
    # New schema
    product_id = getattr(item, "product_id", None)
    if product_id:
        return str(product_id)

    # Legacy schema with DBRef/ReferenceField
    legacy_product = getattr(item, "product", None)
    if not legacy_product:
        return ""

    legacy_id = getattr(legacy_product, "id", legacy_product)
    return str(legacy_id)


def _extract_unit_price(item):
    # New schema
    unit_price = getattr(item, "unit_price", None)
    if unit_price is not None:
        return float(unit_price)

    # Legacy schema
    legacy_price = getattr(item, "price", None)
    if legacy_price is not None:
        return float(legacy_price)

    return 0.0


class OrderItemSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    price = serializers.SerializerMethodField()

    def get_product(self, obj):
        # Giữ tương thích với frontend hiện tại: trường `product` là product_id dạng string
        return _extract_product_id(obj)

    def get_product_id(self, obj):
        return _extract_product_id(obj)

    def get_price(self, obj):
        return _extract_unit_price(obj)


class OrderSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    status = serializers.CharField()
    payment_method = serializers.CharField()
    payment_status = serializers.CharField()
    shipping_address = serializers.CharField()
    city = serializers.CharField()
    province = serializers.CharField()
    postal_code = serializers.CharField()
    phone = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_id(self, obj):
        return str(obj.id)

    def get_customer(self, obj):
        return str(obj.customer.id)

    def get_total_price(self, obj):
        return float(obj.total_price)


class OrderDetailSerializer(OrderSerializer):
    customer = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_customer(self, obj):
        try:
            customer_ref = getattr(obj, "customer", None)
            customer_id = getattr(customer_ref, "id", customer_ref)
            customer_instance = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer_instance)
            return serializer.data
        except Customer.DoesNotExist:
            return {
                "id": str(customer_id),
                "email": "Khách hàng không tồn tại",
                "name": "Khách hàng không tồn tại",
            }
        except Exception:
            return {
                "id": "Không xác định",
                "email": "Lỗi khi truy xuất khách hàng",
                "name": "Lỗi khi truy xuất khách hàng",
            }

    def get_items(self, obj):
        items_data = []
        for item in obj.items:
            product_id = _extract_product_id(item)
            unit_price = _extract_unit_price(item)

            # Theo yêu cầu: chỉ giữ ID sản phẩm trong thuộc tính `product`
            items_data.append(
                {
                    "product": str(product_id) if product_id else "",
                    "product_id": str(product_id) if product_id else "",
                    "quantity": item.quantity,
                    "price": unit_price,
                }
            )
        return items_data


class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        write_only=True,
        required=True,
    )
    shipping_address = serializers.CharField(max_length=255, required=True)
    city = serializers.CharField(max_length=100, required=True)
    province = serializers.CharField(max_length=100, required=True)
    postal_code = serializers.CharField(max_length=20, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    payment_method = serializers.ChoiceField(choices=["cod", "momo", "vnpay"], required=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Đơn hàng phải có ít nhất một sản phẩm.")

        validated_items = []
        product_ids = []

        # Chấp nhận cả key mới `product_id` lẫn key cũ `product`
        for item in items:
            product_id = item.get("product_id") or item.get("product")
            if not product_id:
                raise serializers.ValidationError("Mỗi sản phẩm phải có 'product_id'.")
            product_ids.append(product_id)

        existing_products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids)}

        for item in items:
            product_id = item.get("product_id") or item.get("product")
            quantity_value = item.get("quantity")

            try:
                quantity = int(quantity_value)
            except (TypeError, ValueError):
                raise serializers.ValidationError(
                    f"Số lượng cho sản phẩm {product_id} phải là một số nguyên."
                )

            if quantity <= 0:
                raise serializers.ValidationError(
                    f"Số lượng cho sản phẩm {product_id} phải lớn hơn 0."
                )

            if product_id not in existing_products:
                raise serializers.ValidationError(f"Sản phẩm với ID {product_id} không tồn tại.")

            product = existing_products[product_id]
            unit_price = float(product.price)
            validated_items.append(
                {
                    "product_id": str(product.id),
                    "quantity": quantity,
                    "unit_price": unit_price,
                }
            )

        return validated_items
