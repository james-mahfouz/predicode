from mongoengine import Document, StringField, ReferenceField


class File(Document):
    name = StringField(max_length=100, required=True)
    by_user = StringField(required=True)
