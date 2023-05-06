from models.fileModel import File
from models.userModel import User
from fastapi.responses import JSONResponse
import os


def get_files(user):
    files = File.objects.all()
    files_list = []
    for file in files:
        file_dict = file.to_mongo().to_dict()
        file_dict["_id"] = str(file_dict["_id"])
        files_list.append(file_dict)

    return JSONResponse(content={
        "files": files_list,
        "admin_name": user.name
    })


def get_directory_contents(path):
    contents = []
    for entry in os.scandir(path):
        if entry.is_file():
            contents.append({
                'type': 'file',
                'name': entry.name,
                'path': entry.path,
                'onclick': f"window.open('{entry.path}')"
            })
        elif entry.is_dir():
            subdir_contents = get_directory_contents(entry.path)
            contents.append({
                'type': 'folder',
                'name': entry.name,
                'path': entry.path,
                'contents': subdir_contents
            })
    return contents


def get_users(user):
    users = User.objects.all()
    users_list = []
    for u in users:
        if u != user:
            user_dict = u.to_mongo().to_dict()
            user_dict["_id"] = str(user_dict["_id"])

            files = user_dict.get("files", [])
            for i, file_id in enumerate(files):
                file_obj = File.objects.filter(id=file_id).first()
                if file_obj:
                    files[i] = {"id": str(file_id), "name": file_obj.name}
                else:
                    files[i] = str(file_id)
            user_dict["files"] = files

            users_list.append(user_dict)

    return JSONResponse(content={
        "users": users_list,
        "admin_name": user.name
    })
