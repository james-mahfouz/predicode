from mongoengine import Document, StringField, FloatField


class File(Document):
    name = StringField(max_length=100, required=True)
    path = StringField(required=True)
    by_user = StringField(required=True)
    category = StringField(required=True)
    content_rating = StringField(required=True)
    price = FloatField(required=True)
    size = FloatField(required=True)
