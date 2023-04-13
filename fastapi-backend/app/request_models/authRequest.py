from pydantic import BaseModel


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str
    # name = StringField(max_length=100, required=True)
    # email = EmailField(unique=True, required=True)
    # password = StringField(required=True)
    # role = StringField(choices=["user", "admin"], default="user")
    # courses = ListField(ReferenceField("Course"))


class LoginRequest(BaseModel):
    email: str
    password: str
