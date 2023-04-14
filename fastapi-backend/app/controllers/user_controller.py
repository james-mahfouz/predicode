from models.fileModel import File
import shutil
import json


def get_files(user):
    file_list = []
    for file in user.files:
        file_dict = file.to_mongo().to_dict()
        file_list.append(file_dict)

    # json_content = json.loads(str(file_list))
    # print(json_content)
    return {"files": str(file_list)}


def upload_file(file, user):
    save_path = f"public/{file.filename}"
    if File.objects(name=file.filename).first():
        return {"message": "file with this name already exist"}

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    uploaded_file = File(name=file.filename, by_user=user.name, path=save_path)
    uploaded_file.save()

    user.files.append(uploaded_file)
    user.save()

    return {
        "message": "File created successfully",
        "file_path": save_path
    }
