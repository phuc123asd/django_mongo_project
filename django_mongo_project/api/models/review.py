# api/models/review.py

import mongoengine as me
from datetime import datetime

class Review(me.Document):
    """
    Model cho Đánh giá, khớp với dữ liệu có sẵn trong DB.
    """
    meta = {'collection': 'reviews'}

    # THAY ĐỔI: Sử dụng StringField thay vì ReferenceField
    product_id = me.StringField(required=True)
    customer_id = me.StringField(required=True)
    
    rating = me.IntField(required=True, min_value=1, max_value=5)
    comment = me.StringField(required=True)
    
    # Thêm field để lưu phản hồi tự động từ admin/AI
    # admin_response = me.StringField(required=False)
    # response_generated_at = me.DateTimeField(required=False)
    
    created_at = me.DateTimeField(default=datetime.utcnow, required=True)
    updated_at = me.DateTimeField(default=datetime.utcnow, required=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Review, self).save(*args, **kwargs)
