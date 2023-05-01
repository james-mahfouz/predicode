import shutil
from bson import ObjectId
from fastapi.responses import JSONResponse
import base64
import os
import zipfile
from models.fileModel import File
from models.userModel import User


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
    if file.content_type == "data:application/zip;base64":
        decoded_data = base64.b64decode(file.data)

        temp_file_path = file.name
        with open(temp_file_path, 'wb') as f:
            f.write(decoded_data)

        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            zip_ref.extractall()

        unzipped_file_name = os.path.splitext(file.name)[0]

        save_path = os.path.join('public', unzipped_file_name)

        if File.objects(name=unzipped_file_name).first():
            unzipped_file_name += "_copy"

        save_path_copy = os.path.join('public', unzipped_file_name)

        shutil.move(unzipped_file_name, save_path)

        uploaded_file = File(name=unzipped_file_name, by_user=user.name, path=save_path)
        uploaded_file.save()

        user.files.append(uploaded_file)
        user.save()

        os.remove(temp_file_path)
        return {
            "message": "File created successfully",
            "file_path": save_path
        }

