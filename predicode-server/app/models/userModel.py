import bcrypt
from mongoengine import Document, StringField, ListField, EmailField, ReferenceField
from models.fileModel import File


class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField()
    role = StringField(choices=["user", "admin"], default="user")
    files = ListField(ReferenceField(File))
