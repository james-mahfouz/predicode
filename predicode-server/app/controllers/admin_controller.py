from models.fileModel import File
from models.userModel import User
from fastapi.responses import JSONResponse
import os
from models.historyModel import History


def get_files(user):
    files = File.objects.all()
    files_list = []
    for file in files:
        project_content = get_directory_contents(file.path)
        file_dict = file.to_mongo().to_dict()
        file_dict["_id"] = str(file_dict["_id"])
        if os.path.isfile(file.path):
            file_dict['type'] = 'file'
        else:
            file_dict['type'] = 'folder'
        file_dict["items"] = project_content
        files_list.append(file_dict)

    return JSONResponse(content={
        "files": files_list,
        "admin_name": user.name
    })


def get_directory_contents(path):
    contents = []
    if os.path.isfile(path):
        basename = os.path.basename(path)
        contents.append({
            'type': 'file',
            'name': basename,
            'path': path,
        })
    else:
        for entry in os.scandir(path):
            if entry.is_file():
                contents.append({
                    'type': 'file',
                    'name': entry.name,
                    'path': entry.path,
                })
            elif entry.is_dir():
                subdir_contents = get_directory_contents(entry.path)
                contents.append({
                    'type': 'folder',
                    'name': entry.name,
                    'path': entry.path,
                    'items': subdir_contents
                })
    return contents


def get_users(user):
    users = User.objects.all()
    users_list = []
    for u in users:

        user_dict = u.to_mongo().to_dict()
        user_dict["_id"] = str(user_dict["_id"])

        user_dict.pop("history", None)
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


def get_history(user):
    try:
        history_list = []
        histories = History.objects.all()
        for history in histories:
            file_dict = history.to_mongo().to_dict()
            file_dict["_id"] = str(file_dict["_id"])
            history_list.append(file_dict)

        return JSONResponse(content={
            "history": history_list,
            "user_name": user.name,
            "role": user.role
        })
    except Exception as e:
        print(e)