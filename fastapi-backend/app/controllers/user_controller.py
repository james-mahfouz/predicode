import shutil
from bson import ObjectId
from fastapi.responses import JSONResponse
import base64
import os
from models.fileModel import File
from models.userModel import User


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

        save_path = os.path.join('public', temp_file_path)
        if File.objects(name=temp_file_path).first():
            os.remove(temp_file_path)
            temp_file_path += "_copy"

        with open(temp_file_path, "rb") as src, open(save_path, "wb") as dest:
            shutil.copyfileobj(src, dest)

        uploaded_file = File(name=file.name, by_user=user.name, path=save_path)
        uploaded_file.save()

        user.files.append(uploaded_file)
        user.save()

        os.remove(temp_file_path)
        return {
            "message": "File created successfully",
            "file_path": save_path
        }


