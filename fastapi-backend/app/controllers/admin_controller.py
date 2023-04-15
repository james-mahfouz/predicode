from models.fileModel import File
from models.userModel import User
from fastapi.responses import JSONResponse


def get_files(user):
    files = File.objects.all()
    files_list = []
    for file in files:
        file_dict = file.to_mongo().to_dict()
        file_dict["_id"] = str(file_dict["_id"])
        files_list.append(file_dict)

    return JSONResponse(content={"files": files_list})
#     files = File.objects.all()
#     files_dict = {"files": []}
#     for file in files:
#         files_dict["files"].append({
#             "id": str(file.id),
#             "name": file.name,
#             "path": file.path,
#             "by_user": file.by_user
#         })
#     files_json = json.dumps(files_dict)
#     files_json = json.dumps(files_list)
#     return JSONResponse(content={"files": files_list})


def get_users(user):
    users = User.objects.all()
#     users_dict = {"files": []}
#     for user in users:
#         files_dict["files"].append({
#             "id": str(file.id),
#             "name": file.name,
#             "path": file.path,
#             "by_user": file.by_user
#         })
#     files_json = json.dumps(files_dict)
#
#     return {"files": files_json}