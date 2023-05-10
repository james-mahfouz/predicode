from mongoengine import Document, StringField, ListField, EmailField, ReferenceField
from models.fileModel import File
from models.historyModel import History


class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(default="None")
    login_method = StringField(choices=["normal", "google"], default="normal")
    role = StringField(choices=["user", "admin"], default="user")
    profile_picture = StringField(default="../../assets/no_pp.webp")
    files = ListField(ReferenceField(File))
    history = ListField(ReferenceField(History))
