import shutil
# from bson import ObjectId
from fastapi.responses import JSONResponse
import base64
import os
import zipfile
from models.fileModel import File
# from models.userModel import User


def verify_user(user):
    return JSONResponse(content={
        "verified": "true",
        "username": user.name,
        "role": user.role
    })


def get_files(user):
    files_list = []
    for file in user.files:
        if File.objects(id=file.id).first() is not None:
            file_dict = file.to_mongo().to_dict()
            file_dict["_id"] = str(file_dict["_id"])
            files_list.append(file_dict)
        else:
            user.files.remove(file)
            user.save()

    return JSONResponse(content={
        "files": files_list,
        "user_name": user.name,
        "role": user.role
    })


def upload_file(file, user):
    unzipped_file_path = ""
    unzipped_file_name = ""
    temp_file_path = ''

    try:
        if file.content_type == "data:application/zip;base64":
            decoded_data = base64.b64decode(file.data)
            temp_file_path = file.name
            with open(temp_file_path, 'wb') as f:
                f.write(decoded_data)

            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                zip_ref.extractall()

            unzipped_file_name = os.path.splitext(file.name)[0]
            if not File.objects(name=unzipped_file_name).first():
                unzip_dir = os.path.commonprefix(zip_ref.namelist()).rstrip('/')
                save_path = os.path.join('public', unzipped_file_name)
                shutil.move(unzip_dir, save_path)

                file_size = os.path.getsize(save_path)
                print(file_size)
                uploaded_file = File(name=unzipped_file_name, by_user=user.name, path=save_path, size=file.size, category=file.category, content_rating=file.content_rating, price=file.price)
                uploaded_file.save()

                user.files.append(uploaded_file)
                user.save()

                os.remove(temp_file_path)

                macosx_folder = os.path.join(save_path, '__MACOSX')
                if os.path.exists(macosx_folder):
                    shutil.rmtree(macosx_folder)

            else:
                os.remove(temp_file_path)
                shutil.rmtree(unzipped_file_name)

            index = recursive_read_file(f"public/{unzipped_file_name}", 0)
            print(index)

    except Exception as e:
        print(e)
        print("removing content")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(unzipped_file_name):
            unzipped_file_path = os.path.join('public', unzipped_file_name)
        if os.path.exists(unzipped_file_path):
            shutil.rmtree(unzipped_file_path)

        # Return an error message
        return {
            "message": "An error occurred while processing the file"
        }


def recursive_read_file(folder_path, index):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            index = recursive_read_file(item_path, index)
        else:
            read_file(item_path)
            index += 1
    return index


def read_file(file_path):
    print("hello")
