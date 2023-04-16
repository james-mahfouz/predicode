import jwt
from models.userModel import User
from configs.config import SECRET_KEY
from fastapi import HTTPException, status
from mongoengine import connect, ValidationError, DoesNotExist


async def register(request):
    print(request.name, request.email.lower(), request.password.lower(), request.role)
    try:
        existing_user = User.objects(email=request.email.lower()).first()
        if existing_user:
            print("hello existing user", existing_user)
            raise HTTPException(status_code=404, detail="Email already exists")

        user = User(
            name=request.name,
            email=request.email.lower(),
            password=request.password,
            role=request.role,
        )
        user.save()
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    token = jwt.encode({"id": str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    return {"user": new_user, "token": token}, status.HTTP_201_CREATED


async def login(request):
    email = request.email.lower()
    password = request.password

    user = User.objects(email=email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="email"
        )
    if not user.verify_password(password):
        raise HTTPException(
            status_code=404,
            detail="password"
        )

    token = jwt.encode({"id": str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    return {"user": new_user, "token": token}
