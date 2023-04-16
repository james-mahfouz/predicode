import jwt
from models.userModel import User
from configs.config import SECRET_KEY
from fastapi import status, HTTPException


async def register(request):
    name = request.name
    email = request.email
    password = request.password
    role = request.role
    existing_user = User.objects(email=email).first()

    if existing_user:
        return {"message": "Email already exists"}, 409
    user = User(name=name, email=email, password=password, role=role)
    user.save()

    token = jwt.encode({"id": str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    return {"user": new_user, "token": token}, 201


async def login(request):
    email = request.email
    password = request.password

    user = User.objects(email=email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_UNSUPPORTED_MEDIA_TYPE,
            detail="email"
        )
        # return {
        #
        # }, 500
    if not user.verify_password(password):
        return {
            "message": "Invalid password",
            "error": "password"
        }

    token = jwt.encode({"id": str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    return {"user": new_user, "token": token}
