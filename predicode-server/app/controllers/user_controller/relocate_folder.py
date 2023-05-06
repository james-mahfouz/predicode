import os
import shutil

from controllers.user_controller.user_controller import predict
from models.fileModel import File


def relocate_folder(extracted_files, file, user):
    copied_folders = []
    for extracted_file in extracted_files:
        if not File.objects(name=str(extracted_file).split("/")[0] + "/").first() and not File.objects(
                name=str(extracted_file).split("/")[0]).first():
            if not str(extracted_file).split("/")[0] + "/" in copied_folders:
                save_path = os.path.join('public', extracted_file)
                shutil.move(extracted_file, save_path)

                rating = predict(size=file.size, price=file.price, category=file.category,
                                 content=file.content_rating)

                uploaded_file = File(name=extracted_file, by_user=user.name, path=save_path, size=file.size,
                                     category=file.category, content_rating=file.content_rating, price=file.price,
                                     rating=rating)
                uploaded_file.save()

                user.files.append(uploaded_file)
                user.save()

                copied_folders.append(str(extracted_file))
                return rating
