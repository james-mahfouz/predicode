from uuid import uuid4
from models.fileModel import File


def get_files(user):
    print(f"hello {user.name}")
    return {"message": "welcome"}


# def upload_file(request, user):
#     filename = f"{uuid4()}-{request.filename}"

#     s3 = boto3.client("s3")
#     s3.upload_filobj(request.file, "predicode_files", filename)

#     file = File(filename=request.filename, by_user=user.name, path=f"s3://predicode_files/{filename}")
#     file.save()

#     user.files.append(file)

#     return {"message": "File created successfully"}


print("hello")