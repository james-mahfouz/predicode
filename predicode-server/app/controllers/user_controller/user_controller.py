import shutil
import uuid
import re
import base64
import imghdr
from configs.config import SERVER_HOST

from mongoengine import ValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import base64
import os

from controllers.user_controller.predict import predict
from controllers.user_controller.relocate_folder import relocate_folder
from controllers.user_controller.remove_folder import remove_folders
from controllers.user_controller.search_apply import search_apply
from controllers.user_controller.unzip_file import unzip_file
from controllers.user_controller.add_history import add_history
from models.historyModel import History
from models.userModel import User

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email_pattern = re.compile(email_regex)


def verify_user(user):
    print(user.profile_picture)
    return JSONResponse(content={
        "verified": "true",
        "username": user.name,
        "email": user.email,
        "profile_picture": f"{SERVER_HOST}{user.profile_picture}",
        "role": user.role
    })


def get_history(user):
    try:
        history_list = []
        for history in user.history:
            if History.objects(id=history.id).first() is not None:
                file_dict = history.to_mongo().to_dict()
                file_dict["_id"] = str(file_dict["_id"])
                history_list.append(file_dict)
            else:
                user.history.remove(history)
                user.save()

        return JSONResponse(content={
            "history": history_list,
            "user_name": user.name,
            "role": user.role
        })
    except Exception as e:
        print(e)


def upload_file(file, user):
    if file.size < 614400:
        raise HTTPException(status_code=404, detail="file is too small")
    if file.size > 28147456:
        raise HTTPException(status_code=404, detail="file is too big")
    rating = 0
    try:
        if file.content_type == "data:application/zip;base64":
            decoded_data = base64.b64decode(file.data)
            temp_file_path = f"./{file.name}"
            with open(temp_file_path, 'wb') as f:
                f.write(decoded_data)

            extracted_files = unzip_file(file_path=temp_file_path)
            os.remove(temp_file_path)
            maintainability = search_apply(extracted_files=extracted_files)

            rating = relocate_folder(extracted_files=extracted_files, file=file, user=user, maintainability=maintainability)

            remove_folders(extracted_files)

            if not rating:
                rating = predict(size=file.size, price=file.price, category=file.category, content=file.content_rating)
            add_history(name=file.name, category=file.category, content_rating=file.content_rating,
                        price=file.price, size=file.size, maintainability=maintainability, rating=rating, user=user)

            return {
                "rating": rating,
                "maintainability": maintainability
            }

    except Exception as e:
        raise e


def update_info(user, request):
    try:
        if request.profile_picture is not None:
            image_data = base64.b64decode(request.profile_picture)
            if imghdr.what(None, image_data) is None:
                details = {"error": "file", "detail": "file must be an image"}
                raise HTTPException(status_code=500, detail=details)
            unique_id = uuid.uuid4()
            filename = f"{unique_id}_{request.file_name}"
            file_path = os.path.join("public/profile_pictures", filename)
            with open(file_path, "wb") as buffer:
                buffer.write(image_data)
            updated_user = User.objects(id=user.id).first()
            updated_user.profile_picture = file_path
        else:
            updated_user = User.objects(id=user.id).first()

        if len(request.name) < 3:
            details = {"error": "name", "detail": "Name must have 3 characters or more"}
            updated_user.save()
            raise HTTPException(status_code=500, detail=details)
        updated_user.name = request.name
        if not email_pattern.match(request.email.lower()):
            updated_user.save()
            details = {"error": "email", "detail": "Email must be in name@mail.com format"}
            raise HTTPException(status_code=500, detail=details)
        existing_user = User.objects(email=request.email).first()
        if existing_user and existing_user.id != user.id:
            updated_user.save()
            details = {"error": "email", "detail": "Email already exists"}
            raise HTTPException(status_code=500, detail=details)
        updated_user.name = request.name
        updated_user.email = request.email
        updated_user.save()

        return {"message": "updated successfully"}

    except ValidationError as e:
        print(e)
