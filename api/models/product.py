from mongoengine import Document, fields, NULLIFY, CASCADE

class Product(Document):
    """
    Model Product để lưu trữ thông tin sản phẩm trong collection 'products'.
    Kế thừa từ Document của MongoEngine.
    """
    # Meta options để định nghĩa collection name
    meta = {'collection': 'products'}

    name = fields.StringField(required=True, max_length=255, verbose_name="Tên sản phẩm")
    price = fields.DecimalField(required=True, precision=2, verbose_name="Giá bán")
    originalPrice = fields.DecimalField(precision=2, verbose_name="Giá gốc")
    image = fields.URLField(required=True, verbose_name="Hình ảnh chính")
    rating = fields.FloatField(min_value=0, max_value=5, default=0, verbose_name="Đánh giá trung bình")
    category = fields.StringField(required=True, verbose_name="Danh mục")
    brand = fields.StringField(required=True, verbose_name="Thương hiệu")
    isNew = fields.BooleanField(default=False, verbose_name="Sản phẩm mới")



    def __str__(self):
        return f"<Product: {self.name}>"