import shutil
from fastapi.responses import JSONResponse
import base64
import os
from zipfile import ZipFile
from models.fileModel import File
import joblib
import openai
from configs.config import OPEN_AI_KEY
import glob
import random
import re


openai.api_key = OPEN_AI_KEY
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

                        rating = predict(size=file.size, price=file.price, category=file.category,
                                         content=file.content_rating)

                        uploaded_file = File(name=extracted_file, by_user=user.name, path=save_path, size=file.size,
                                             category=file.category, content_rating=file.content_rating, price=file.price, rating=rating)
                        uploaded_file.save()

                        user.files.append(uploaded_file)
                        user.save()

                        copied_folders.append(str(extracted_file))

            if not rating:
                rating = predict(size=file.size, price=file.price, category=file.category, content=file.content_rating)

            searched_folders = []
            for extracted_file in extracted_files:
                if not str(extracted_file).split("/")[0] + "/" in searched_folders:
                    functions = search_java_files(extracted_file)
                    selected_functions = random.sample(functions, 3)
                    functions_string = "\n".join(selected_functions)
                    maintainability = check_maintainability(functions_string)
                    searched_folders.append(str(extracted_file))

            removed_folders = []
            for extracted_file in extracted_files:
                if not str(extracted_file).split("/")[0] + "/" in removed_folders:
                    if os.path.exists(extracted_file):
                        if os.path.isdir(extracted_file):
                            shutil.rmtree(extracted_file)
                        else:
                            os.remove(extracted_file)

                    removed_folders.append(str(extracted_file))
            return {
                "rating": rating,
                "maintainability": maintainability
            }

    except Exception as e:
        return {
            "message": "An error occurred while processing the file",
            "error": e
        }


def check_maintainability(code):
    # prompt = "Please check the following code and tell me if it's maintainable or not:\n\n" + code + "\n\nWhat are the potential issues with this code?\n\nWhat changes would you suggest to improve its maintainability?\n\nAnswer: "
    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=prompt,
    #     temperature=0.7,
    #     max_tokens=2048,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )
    #
    # return response.choices[0].text.strip()
    return "This code is not very maintainable. It is difficult to read and understand, and it is also difficult to make changes or add features. There are also some potential issues, such as the lack of error handling and the use of hardcoded values. \nTo improve its maintainability, I would suggest using meaningful variable names, refactoring long methods, and adding comments to explain what the code is doing. I would also suggest using an object-oriented approach and encapsulating the code into classes and methods. Additionally, error handling should be added to ensure that the code is robust and can handle unexpected errors."


def search_java_files(folder_path, count=3, functions=[]):
    if count == 0:
        return functions

    for file_path in glob.glob(os.path.join(folder_path, '*.java')):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if re.search(r"public\s+\S+\s*\(", line):

                    function_lines = [line.strip() for line in lines[i:i+30]]
                    function = '\n'.join(function_lines)

                    functions.append(function)

    for dir_path in glob.glob(os.path.join(folder_path, '*/')):
        functions = search_java_files(dir_path, count, functions)

    return functions


def predict(size, price, category, content):
    data = [int(size), float(price)]

    for i in range(33):
        if category_list[i] == category:
            data.append(1)
        else:
            data.append(0)

    for i in range(5):
        if content_list[i] == content:
            data.append(1)
        else:
            data.append(0)

    rating = rf.predict([data])
    rating = str(rating[0])[:4]

    return rating
# response = check_maintainability(inspect.getsource(verify_user) + inspect.getsource(get_files))
# print(response)
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