
# api/models/admin_response.py

import mongoengine as me
from datetime import datetime

class AdminResponse(me.Document):
    """
    Model cho phản hồi của admin, độc lập với bảng Review
    """
    meta = {'collection': 'admin_responses'}
    
    # Liên kết đến review
    review_id = me.StringField(required=True)
    
    # Nội dung phản hồi
    response = me.StringField(required=True)
    
    # Thông tin admin
    admin_id = me.StringField(required=True)
    admin_name = me.StringField(required=True)
    
    # Thời gian tạo và cập nhật
    created_at = me.DateTimeField(default=datetime.utcnow, required=True)
    updated_at = me.DateTimeField(default=datetime.utcnow, required=True)
    
    # Loại phản hồi (manual: admin nhập, ai: tự động từ AI)
    response_type = me.StringField(required=True, choices=['manual', 'ai'], default='manual')
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(AdminResponse, self).save(*args, **kwargs)
