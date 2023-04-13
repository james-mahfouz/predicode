from uuid import uuid4
import boto3
from models.fileModel import File
import shutil


def get_files(user):
    print(f"hello {user.name}")
    return {"message": "welcome"}


def upload_file(file, user):

    save_path = f"public/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    uploaded_file = File(name=file.filename, by_user=user.name, path=save_path)
    uploaded_file.save()

    user.files.append(uploaded_file)

    return {
        "message": "File created successfully",
        "file_path": save_path
    }
