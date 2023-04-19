import bcrypt
from mongoengine import Document, StringField, ListField, EmailField, ReferenceField
from models.fileModel import File


class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    role = StringField(choices=["user", "admin"], default="user")
    files = ListField(ReferenceField(File))

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password = hashlib.sha256(self.password.encode()).hexdigest()
    #     super().save(*args, **kwargs)
    #
    # def verify_password(self, password):
    #     hashed_password = hashlib.sha256(password.encode()).hexdigest()
    #     print(hashed_password)
    #     print(self.password)
    #     if hashed_password == self.password:
    #         print('Passwords matched correctly')
    #     return hashed_password == self.password
