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
        # print(decoded_data)

        temp_file_path = 'temp.zip'
        with open(temp_file_path, 'wb') as f:
            f.write(decoded_data)

        save_path = os.path.join('public', 'hello.zip')
        if File.objects(name="hello.zip").first():
            os.remove(temp_file_path)
            return {"message": "file with this name already exist"}

        with open(temp_file_path, "rb") as src, open(save_path, "wb") as dest:
            shutil.copyfileobj(src, dest)

        uploaded_file = File(name="hello.zip", by_user=user.name, path=save_path)
        uploaded_file.save()

        user.files.append(uploaded_file)
        user.save()

        os.remove(temp_file_path)
        return {
            "message": "File created successfully",
            "file_path": save_path
        }


