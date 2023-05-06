import shutil
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import base64
import os

from controllers.user_controller.check_maintainability import check_maintainability
from controllers.user_controller.predict import predict
from controllers.user_controller.remove_folder import remove_folders
from controllers.user_controller.search_java_file import search_java_files
from controllers.user_controller.unzip_file import unzip_file
from models.fileModel import File
import joblib
import openai
from configs.config import OPEN_AI_KEY
import random

openai.api_key = OPEN_AI_KEY


def verify_user(user):
    return JSONResponse(content={
        "verified": "true",
        "username": user.name,
        "role": user.role
    })


def get_files(user):
    files_list = []
    for file in user.files:
        if File.objects(id=file.id).first() is not None:
            file_dict = file.to_mongo().to_dict()
            file_dict["_id"] = str(file_dict["_id"])
            files_list.append(file_dict)
        else:
            user.files.remove(file)
            user.save()

    return JSONResponse(content={
        "files": files_list,
        "user_name": user.name,
        "role": user.role
    })


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

            rating = relocate_folder(extracted_files=extracted_files, file=file, user=user)

            remove_folders(extracted_files)

            if not rating:
                rating = predict(size=file.size, price=file.price, category=file.category, content=file.content_rating)

            return {
                "rating": rating,
                "maintainability": maintainability
            }

    except Exception as e:
        raise e


def search_apply(extracted_files):
    searched_folders = []
    for extracted_file in extracted_files:
        if not str(extracted_file).split("/")[0] + "/" in searched_folders:
            functions = search_java_files(extracted_file)
            if len(functions) == 0:
                print("removing")
                remove_folders(extracted_files)
                raise HTTPException(status_code=404, detail="This isn't a Java Project")
            if len(functions) < 5:
                remove_folders(extracted_files)
                raise HTTPException(status_code=500, detail="This project is too small to be deployed")

            selected_functions = random.sample(functions, 3)
            functions_string = "\n".join(selected_functions)
            maintainability = check_maintainability(functions_string)
            searched_folders.append(str(extracted_file))
            return maintainability


def relocate_folder(extracted_files, file, user):
    copied_folders = []
    for extracted_file in extracted_files:
        if not File.objects(name=str(extracted_file).split("/")[0] + "/").first() and not File.objects(
                name=str(extracted_file).split("/")[0]).first():
            if not str(extracted_file).split("/")[0] + "/" in copied_folders:
                save_path = os.path.join('public', extracted_file)
                shutil.move(extracted_file, save_path)

                rating = predict(size=file.size, price=file.price, category=file.category,
                                 content=file.content_rating)

                uploaded_file = File(name=extracted_file, by_user=user.name, path=save_path, size=file.size,
                                     category=file.category, content_rating=file.content_rating, price=file.price,
                                     rating=rating)
                uploaded_file.save()

                user.files.append(uploaded_file)
                user.save()

                copied_folders.append(str(extracted_file))
                return rating


