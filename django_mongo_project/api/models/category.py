from mongoengine import Document, fields, NULLIFY, CASCADE

class Category(Document):
    id = fields.IntField(primary_key=True, verbose_name="ID Thương hiệu")
    name = fields.StringField(required=True, max_length=100)
    meta = {'collection': 'categories'}
    def __str__(self): return self.name