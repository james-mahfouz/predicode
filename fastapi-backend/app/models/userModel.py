import bcrypt
from mongoengine import Document, StringField, ListField, EmailField

class User(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    password_hash = StringField()
    files = ListField()

    @property
    def password(self):
        raise AttributeError('Password cannot be accessed directly')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
