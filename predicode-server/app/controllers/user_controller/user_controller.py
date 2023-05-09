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
from models.fileModel import File
from models.historyModel import History


def verify_user(user):
    return JSONResponse(content={
        "verified": "true",
        "username": user.name,
        "role": user.role
    })


def get_history(user):
    history_list = []
    for history in user.history:
        if History.objects(id=history.id).first() is not None:
            file_dict = history.to_mongo().to_dict()
            file_dict["_id"] = str(file_dict["_id"])
            history_list.append(file_dict)
        else:
            user.files.remove(history)
            user.save()

    return JSONResponse(content={
        "history": history_list,
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


