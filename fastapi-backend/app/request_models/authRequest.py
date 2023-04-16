from pydantic import BaseModel, constr, validator


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "user"

    @validator('name')
    def capitalize_name(cls, name):
        return name.capitalize()


class LoginRequest(BaseModel):
    email: str
    password: str
