from mongoengine import Document, fields
from django.contrib.auth.hashers import make_password, check_password

class Customer(Document):
    """
    Model Customer sử dụng mongoengine.
    Sẽ được lưu vào collection 'customer' trong MongoDB.
    """
    # Mongoengine tự động quản lý trường _id (ObjectId), không cần khai báo.
    
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True, max_length=256)
    
    first_name = fields.StringField(max_length=50)
    last_name = fields.StringField(max_length=50)
    phone = fields.StringField(max_length=20)
    
    address = fields.StringField()
    city = fields.StringField(max_length=100)
    province = fields.StringField(max_length=100)
    postal_code = fields.StringField(max_length=20)

    # Định nghĩa tên collection trong MongoDB
    meta = {
        'collection': 'customers',
    }

    @property
    def id(self):
        """Để truy cập id như một thuộc tính, trả về chuỗi."""
        return str(self.pk) # pk là primary key, là ObjectId

    def set_password(self, raw_password):
        """Hash và lưu password."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Kiểm tra password với hash đã lưu."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"