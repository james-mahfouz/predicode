from fastapi.responses import JSONResponse
from fastapi import HTTPException
import base64
import os

from controllers.user_controller.predict import predict
from controllers.user_controller.relocate_folder import relocate_folder
from controllers.user_controller.remove_folder import remove_folders
from controllers.user_controller.search_apply import search_apply
from controllers.user_controller.unzip_file import unzip_file
from models.fileModel import File
import joblib
import openai
from configs.config import OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY
rf = joblib.load('../predicode-prediction-model/model.joblib')

category_list = ['ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY', 'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS',
                 'COMMUNICATION', 'DATING', 'EDUCATION', 'ENTERTAINMENT', 'EVENTS', 'FAMILY', 'FINANCE',
                 'FOOD_AND_DRINK', 'GAME', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME', 'LIBRARIES_AND_DEMO', 'LIFESTYLE',
                 'MAPS_AND_NAVIGATION', 'MEDICAL', 'NEWS_AND_MAGAZINES', 'PARENTING', 'PERSONALIZATION', 'PHOTOGRAPHY',
                 'PRODUCTIVITY', 'SHOPPING', 'SOCIAL', 'SPORTS', 'TOOLS', 'TRAVEL_AND_LOCAL', 'VIDEO_PLAYERS', 'WEATHER']
content_list = ['Adults only 18+', 'Everyone', 'Everyone 10+', 'Mature 17+', 'Teen']


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


