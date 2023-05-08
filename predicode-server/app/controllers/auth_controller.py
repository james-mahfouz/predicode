import jwt
from models.userModel import User
from configs.config import SECRET_KEY
from fastapi import HTTPException, status
from mongoengine import ValidationError
import re
import hashlib
from google.oauth2 import id_token
from google.auth.transport import requests

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email_pattern = re.compile(email_regex)


async def register(request):
    try:
        existing_user = User.objects(email=request.email.lower()).first()
        if len(request.name) < 3:
            details = {"error": "name", "detail": "Name must have 3 characters or more"}
            raise HTTPException(status_code=500, detail=details)

        if not email_pattern.match(request.email.lower()):
            details = {"error": "email", "detail": "Email must be in name@mail.com format"}
            raise HTTPException(status_code=500, detail=details)

        if existing_user:
            details = {"error": "email", "detail": "Email already exists"}
            raise HTTPException(status_code=500, detail=details)

        if len(request.password) < 8:
            details = {"error": "password", "detail": "password must be at least 8 characters"}
            raise HTTPException(status_code=404, detail=details)
        hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
        user = User(
            name=request.name,
            email=request.email.lower(),
            password=hashed_password,
            role=request.role,
        )
        user.save()
    except ValidationError as e:
        print(e)

    token = jwt.encode({"id": str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    return {"user": new_user, "token": token}, status.HTTP_201_CREATED


async def login(request):
    email = request.email.lower()
    password = request.password
    try:
        user = User.objects(email=email).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="email"
            )
        if user.login_method == "normal":
            raise HTTPException(
                status_code=404,
                detail="you are signed in using google"
            )
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(hashed_password)
        print(user.password)
        if not hashed_password == user.password:
            raise HTTPException(
                status_code=404,
                detail="password"
            )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    token = jwt.encode({"id": str(user.id), "email": user.email}, SECRET_KEY, algorithm="HS256")
    new_user = user.to_mongo().to_dict()
    del new_user["_id"]
    del new_user["password"]
    del new_user["files"]
    return {"user": new_user, "token": token}


async def google_login(token):
    try:
        token = str(token)
        token = token.split('token=')[1]
        token = token.strip("'")
        idinfo = id_token.verify_oauth2_token(token, requests.Request())

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid issuer')

        user_email = idinfo['email']
        user_name = idinfo['name']
        print(user_email, user_name)
        existing_user = User.objects(email=user_email).first()
        if existing_user:
            token = jwt.encode({"id": str(existing_user.id), "email": existing_user.email}, SECRET_KEY, algorithm="HS256")
            new_user = existing_user.to_mongo().to_dict()
            del new_user["_id"]
            del new_user["password"]
            del new_user["files"]
            return {"user": new_user, "token": token}
        else:
            token = jwt.encode({"id": str(existing_user.id), "email": existing_user.email}, SECRET_KEY, algorithm="HS256")
            new_user = existing_user.to_mongo().to_dict()
            del new_user["_id"]
            del new_user["password"]
            return {"user": new_user, "token": token}, status.HTTP_201_CREATED
    except ValueError:
        raise HTTPException(status_code=401, detail='Invalid token.')