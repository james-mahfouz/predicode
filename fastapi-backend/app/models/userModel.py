import bcrypt
from mongoengine import Document, StringField, ListField, EmailField, ReferenceField
from models.fileModel import File
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    role = StringField(choices=["user", "admin"], default="user")
    files = ListField(ReferenceField(File))

    def save(self, *args, **kwargs):
        if self.password:
            self.password = Hasher.get_password_hash(password=self.password)
        super().save(*args, **kwargs)

    def verify_password(self, password):
        return Hasher.verify_password(password, self.password)


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
