# api/models/order.py
from mongoengine import Document, fields, EmbeddedDocument
from api.models.customer import Customer
from datetime import datetime


class OrderItem(EmbeddedDocument):
    # Cấu trúc mới: lưu product_id + quantity trong order item
    product_id = fields.StringField(required=False)
    quantity = fields.IntField(required=True, min_value=1)
    unit_price = fields.DecimalField(required=False, precision=2, force_string=True)
    meta = {"strict": False}

class Order(Document):
    STATUS_CHOICES = ['Đang Xử Lý', 'Đang Vận Chuyển', 'Đã Giao']
    PAYMENT_METHOD_CHOICES = ['cod', 'momo', 'vnpay']
    PAYMENT_STATUS_CHOICES = ['pending', 'paid', 'failed']
    
    customer = fields.ReferenceField(Customer, required=True)
    items = fields.ListField(fields.EmbeddedDocumentField(OrderItem))
    total_price = fields.DecimalField(required=True, precision=2)
    status = fields.StringField(required=True, choices=STATUS_CHOICES, default='Đang Xử Lý')
    payment_method = fields.StringField(required=True, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = fields.StringField(choices=PAYMENT_STATUS_CHOICES, default='pending')
    shipping_address = fields.StringField(required=True)
    city = fields.StringField(required=True)
    province = fields.StringField(required=True)
    postal_code = fields.StringField(required=True)
    phone = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.utcnow, required=True)
    updated_at = fields.DateTimeField(default=datetime.utcnow, required=True)

    meta = {
        'collection': 'orders',
        'indexes': [
            'customer'
        ]
    }

    def save(self, *args, **kwargs):
        """
        Ghi đè phương thức save để tự động cập nhật trường 'updated_at'.
        """
        self.updated_at = datetime.utcnow()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.customer.email if self.customer else 'Unknown'}"
