from mongoengine import Document, StringField


class File(Document):
    name = StringField(max_length=100, required=True)
    path = StringField(required=True)
    by_user = StringField(required=True)
