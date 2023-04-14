from models.fileModel import File
from models.userModel import User
import shutil


def get_files(user):
    # user1 = User.objects(id=user.id).first()
    # user1.files = File.objects.all()
    # user1.populate("files")
    for file in user.files:
        print(f"File Name: {str(file)}")
        print(f"File Path: {file.path}")
    return {"files": "files"}


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
