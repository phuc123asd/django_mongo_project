from mongoengine import Document, fields, CASCADE
from api.models.product import Product

class ProductDetail(Document):
    """
    Mô hình chi tiết sản phẩm tương ứng với dữ liệu mock từ frontend.
    Dùng cho trang chi tiết sản phẩm.
    """
    meta = {'collection': 'productdetails'}

    # Liên kết 1–1 với Product
    product = fields.ReferenceField('Product', required=True, unique=True, reverse_delete_rule=CASCADE)


    # Trường chính
    images = fields.ListField(fields.URLField(), verbose_name="Danh sách ảnh chi tiết")
    rating = fields.FloatField(min_value=0, max_value=5, default=0.0)
    reviewCount = fields.IntField(min_value=0, default=0)
    description = fields.StringField()
    features = fields.ListField(fields.StringField(), verbose_name="Danh sách tính năng")
    specifications = fields.DictField(field=fields.StringField(), verbose_name="Thông số kỹ thuật")
    inStock = fields.BooleanField(default=True, verbose_name="Còn hàng hay không")
    hasARView = fields.BooleanField(default=False, verbose_name="Có hỗ trợ AR view không")

    def __str__(self):
        return f"<ProductDetail: {self.product.name}>"
