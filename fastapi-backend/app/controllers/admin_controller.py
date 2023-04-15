from models.fileModel import File
import json


def get_files(user):
    files = File.objects.all()
    files_dict = {"files": []}
    for file in files:
        files_dict["files"].append({
            "id": str(file.id),
            "name": file.name,
            "path": file.path,
            "by_user": file.by_user
        })
    files_json = json.dumps(files_dict)

    return files_json
