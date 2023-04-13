from uuid import uuid4
import boto3
from models.fileModel import File


def get_files(user):
    print(f"hello {user.name}")
    return {"message": "welcome"}


def upload_file(file, user):
    filename = f"{uuid4()}-{file.filename}"

    s3 = boto3.client("s3")
    s3.upload_fileobj(file.file, "predicode_files", filename)

    uploaded_file = File(filename=file.filename, by_user=user.name, path=f"s3://predicode_files/{filename}")
    uploaded_file.save()

    user.files.append(file)

    return {"message": "File created successfully"}
