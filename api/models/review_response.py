# api/models/review_response.py

import mongoengine as me
from datetime import datetime

class ReviewResponse(me.Document):
    """
    Model để lưu trữ phản hồi của Admin/Shop cho một đánh giá (Review) cụ thể.
    Mỗi phản hồi sẽ liên kết với một review duy nhất thông qua review_id.
    """
    meta = {'collection': 'review_responses'}

    # Liên kết đến review gốc mà phản hồi này dành cho
    review_id = me.StringField(required=True)
    
    # Thông tin về người phản hồi (thường là Admin)
    responder_id = me.StringField(required=True)  # ID của admin/staff
    responder_name = me.StringField(required=True) # Tên hiển thị của admin/staff
    
    # Nội dung của phản hồi
    response_text = me.StringField(required=True)
    
    # Các trường timestamp để theo dõi thời gian
    created_at = me.DateTimeField(default=datetime.utcnow, required=True)
    updated_at = me.DateTimeField(default=datetime.utcnow, required=True)

    def save(self, *args, **kwargs):
        # Tự động cập nhật thời gian sửa đổi
        self.updated_at = datetime.utcnow()
        return super(ReviewResponse, self).save(*args, **kwargs)

    def __str__(self):
        return f"Phản hồi cho review {self.review_id} bởi {self.responder_name}"
