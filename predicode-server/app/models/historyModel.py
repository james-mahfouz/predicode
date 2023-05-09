from mongoengine import Document, StringField, FloatField, DateTimeField
from datetime import datetime


class History(Document):
    name = StringField(max_length=100, required=True)
    category = StringField(required=True)
    content_rating = StringField(required=True)
    price = FloatField(required=True)
    size = FloatField(required=True)
    rating = FloatField(required=True)
    maintainability = StringField(required=True)
    date_created = DateTimeField(default=datetime.now)

