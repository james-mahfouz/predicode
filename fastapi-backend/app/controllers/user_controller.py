import shutil
# from bson import ObjectId
from fastapi.responses import JSONResponse
import base64
import os
from zipfile import ZipFile
from models.fileModel import File
import joblib
from rapidfuzz import fuzz
import textract

rf = joblib.load('../predicode-prediction-model/model.joblib')
category_list = ['ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY', 'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'EDUCATION', 'ENTERTAINMENT', 'EVENTS', 'FAMILY', 'FINANCE', 'FOOD_AND_DRINK', 'GAME', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME', 'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'MAPS_AND_NAVIGATION', 'MEDICAL', 'NEWS_AND_MAGAZINES', 'PARENTING', 'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'SHOPPING', 'SOCIAL', 'SPORTS', 'TOOLS', 'TRAVEL_AND_LOCAL', 'VIDEO_PLAYERS', 'WEATHER']
content_list = ['Adults only 18+', 'Everyone', 'Everyone 10+', 'Mature 17+', 'Teen']


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
    rating = 0
    try:
        if file.content_type == "data:application/zip;base64":
            decoded_data = base64.b64decode(file.data)
            temp_file_path = f"./{file.name}"
            with open(temp_file_path, 'wb') as f:
                f.write(decoded_data)

            extracted_files = []

            with ZipFile(temp_file_path, "r") as zip_ref:
                for filename in zip_ref.namelist():
                    if not filename.startswith("__MACOSX"):
                        zip_ref.extract(filename)
                        if os.path.exists(filename):
                            extracted_files.append(filename)
            os.remove(temp_file_path)

            copied_folders = []
            for extracted_file in extracted_files:
                if not File.objects(name=str(extracted_file).split("/")[0] + "/").first() and not File.objects(name=str(extracted_file).split("/")[0]).first():
                    if not str(extracted_file).split("/")[0] + "/" in copied_folders:
                        save_path = os.path.join('public', extracted_file)
                        shutil.move(extracted_file, save_path)

                        data = [int(file.size), float(file.price)]

                        for i in range(33):
                            if category_list[i] == file.category:
                                data.append(1)
                            else:
                                data.append(0)

                        for i in range(5):
                            if content_list[i] == file.content_rating:
                                data.append(1)
                            else:
                                data.append(0)

                        rating = rf.predict([data])
                        print(rating)
                        uploaded_file = File(name=extracted_file, by_user=user.name, path=save_path, size=file.size,
                                             category=file.category, content_rating=file.content_rating, price=file.price, rating=rating)
                        uploaded_file.save()

                        user.files.append(uploaded_file)
                        user.save()

                        copied_folders.append(str(extracted_file))

            if not rating:
                data = [int(file.size), float(file.price)]

                for i in range(33):
                    if category_list[i] == file.category:
                        data.append(1)
                    else:
                        data.append(0)

                for i in range(5):
                    if content_list[i] == file.content_rating:
                        data.append(1)
                    else:
                        data.append(0)

                rating = rf.predict([data])

            removed_folders = []
            for extracted_file in extracted_files:
                if not str(extracted_file).split("/")[0] + "/" in removed_folders:
                    if os.path.exists(extracted_file):
                        if os.path.isdir(extracted_file):
                            shutil.rmtree(extracted_file)
                        else:
                            os.remove(extracted_file)

                    removed_folders.append(str(extracted_file))
            return {"rating": rating[0]}
            # for extracted_file in extracted_files:
            #     print("started determining category")
            #     dict_counts = {category: 0 for category in word_dict}
            #
            #     category_won = recursive_read_file(f"public/{extracted_file}", dict_counts)
            #     print("final count: ", category_won)
            #     return{
            #         'category': category_won
            #     }

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
            "message": "An error occurred while processing the file",
            "error": e
        }


# def recursive_read_file(folder_path, count):
#     if os.path.isfile(folder_path):
#         count = read_file(folder_path, count, word_dict)
#     else:
#         for item in os.listdir(folder_path):
#             item_path = os.path.join(folder_path, item)
#             if os.path.isdir(item_path):
#                 recursive_read_file(item_path, count)
#             elif os.path.isfile(item_path):
#                 count = read_file(item_path, count, word_dict)
#
#     # print("finalcount: ", max(dict_counts, key=lambda k: dict_counts[k]))
#     # print(count)
#     # print(max(count, key=lambda k: count[k]))
#     return count
#     # return max(count, key=lambda k: count[k])
#
#
# def read_file(file_path, category_counts, keywords):
#     try:
#         # print("trying")
#         text = textract.process(file_path).decode('utf-8', errors='ignore')
#         # print(text)
#         for category, category_keywords in keywords.items():
#             for keyword in category_keywords:
#
#                 # Use fuzzy matching to find all occurrences of the keyword in the text
#                 # for word in text.split(" "):
#                 for word in text.split(" "):
#                     score = fuzz.partial_ratio(keyword, word, score_cutoff=80)
#
#                     if score > 80:
#                         category_counts[category] += 1
#                 # Increment the category count for each match
#         return category_counts
#         # return max(category_counts, key=category_counts.get)
#     except Exception as e:
#         print(e)
#         print("can't read")
#         return False