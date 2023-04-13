import jwt
from models.userModel import User
from configs.config import SECRET_KEY
import json


async def register(request):
    print(request)
    data = json.loads(request)
    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data.get("role", "user")
    existing_user = User.objects(email=email).first()

    if existing_user:
        return {"message": "Email already exists"}, 409
    user = User(name=name, email=email, password=password, role=role)
    user.save()

    token = jwt.encode({"id":str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    return {"user": new_user, "token": token}, 201

async def login():
    print("hello login")