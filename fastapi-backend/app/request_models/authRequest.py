from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, constr, validator


class RegisterRequest(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    password: constr(min_length=8)
    role: str

    @validator('name')
    def capitalize_name(cls, name):
        return name.capitalize()


class LoginRequest(BaseModel):
    email: str
    password: str
