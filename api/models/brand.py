from mongoengine import Document, fields, NULLIFY, CASCADE

class Brand(Document):
    name = fields.StringField(max_length=100)

    meta = {
        'collection': 'brands'
    }
