from models.fileModel import File
from models.userModel import User
from fastapi.responses import JSONResponse
from bson import ObjectId


def get_files(user):
    files = File.objects.all()
    files_list = []
    for file in files:
        file_dict = file.to_mongo().to_dict()
        file_dict["_id"] = str(file_dict["_id"])
        files_list.append(file_dict)

    return JSONResponse(content={"files": files_list})


def get_users(user):
    users = User.objects.all()
    users_list = []
    for u in users:
        if u != user:
            user_dict = u.to_mongo().to_dict()
            user_dict["_id"] = str(user_dict["_id"])
            users_list.append(user_dict)

    return JSONResponse(content={"users": users_list})
