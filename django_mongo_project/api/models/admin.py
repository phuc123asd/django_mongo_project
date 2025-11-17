from mongoengine import Document, fields
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

class Admin(Document):
    """
    Model Admin cho hệ thống quản trị.
    """
    
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True, max_length=256)
    
    username = fields.StringField(required=True, unique=True, max_length=50)
    full_name = fields.StringField(max_length=100)
    
    role = fields.StringField(default='admin', choices=['admin', 'super_admin'])
    is_active = fields.BooleanField(default=True)
    
    created_at = fields.DateTimeField(default=datetime.utcnow)
    last_login = fields.DateTimeField()
    
    meta = {
        'collection': 'admins',
    }

    @property
    def id(self):
        """Trả về id dưới dạng chuỗi."""
        return str(self.pk)
    
    def set_password(self, raw_password):
        """Hash và lưu password."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Kiểm tra password với hash đã lưu."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.email})"
