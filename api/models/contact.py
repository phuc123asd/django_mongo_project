from mongoengine import Document, fields, NULLIFY, CASCADE
from datetime import datetime

class Contact(Document):
    """
    Model Contact để lưu trữ các tin nhắn liên hệ từ người dùng.
    """
    meta = {'collection': 'contacts'}

    name = fields.StringField(required=True, max_length=255, verbose_name="Tên người gửi")
    email = fields.EmailField(required=True, verbose_name="Email")
    subject = fields.StringField(required=True, max_length=255, verbose_name="Tiêu đề")
    message = fields.StringField(required=True, verbose_name="Nội dung tin nhắn")
    created_at = fields.DateTimeField(default=datetime.utcnow, verbose_name="Ngày tạo")
    is_read = fields.BooleanField(default=False, verbose_name="Đã đọc")
    reply = fields.StringField(null=True, verbose_name="Phản hồi từ admin")

    def __str__(self):
        return f"<Contact: {self.name} - {self.subject}>"
