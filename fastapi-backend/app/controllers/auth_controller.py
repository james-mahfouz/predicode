import jwt
from models.userModel import User
from configs.config import SECRET_KEY
from fastapi import HTTPException, status
from mongoengine import ValidationError
import re
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email_pattern = re.compile(email_regex)


async def register(request):
    try:
        existing_user = User.objects(email=request.email.lower()).first()
        if len(request.name) < 3:
            details = {"error": "name", "detail": "Name must have 3 characters or more"}
            raise HTTPException(status_code=404, detail=details)

        if not email_pattern.match(request.email.lower()):
            details = {"error": "email", "detail": "Email must be in name@mail.com format"}
            raise HTTPException(status_code=422, detail=details)

        if existing_user:
            details = {"error": "email", "detail": "Email already exists"}
            raise HTTPException(status_code=404, detail=details)

        if len(request.password) < 8:
            details = {"error": "password", "detail": "password must be at least 8 characters"}
            raise HTTPException(status_code=404, detail=details)
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

        # password = hashlib.sha256(self.password.encode()).hexdigest()
        raise HTTPException(
            status_code=404,
            detail="password"
        )
    print(pwd_context.hash(password))
    print(user.password)
    token = jwt.encode({"id": str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    return {"user": new_user, "token": token}
