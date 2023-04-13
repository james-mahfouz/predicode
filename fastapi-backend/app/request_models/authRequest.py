from pydantic import BaseModel


class NewUser(BaseModel):
    user_id: int
    name: str
    email: str
    role: str
    # name = StringField(max_length=100, required=True)
    # email = EmailField(unique=True, required=True)
    # password = StringField(required=True)
    # role = StringField(choices=["user", "admin"], default="user")
    # courses = ListField(ReferenceField("Course"))