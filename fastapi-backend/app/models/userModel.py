import bcrypt
from mongoengine import Document, StringField, ListField, EmailField, ReferenceField
from models.fileModel import File


class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    role = StringField(choices=["user", "admin"], default="user")
    files = ListField(ReferenceField(File))

    def save(self, *args, **kwargs):
        if self.password:
            self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        super(User, self).save(*args, **kwargs)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
