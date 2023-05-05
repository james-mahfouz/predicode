import shutil
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
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
    if file.size < 819200:
        raise HTTPException(status_code=404, detail="file is too small")

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
                    print(len(functions))
                    if len(functions) == 0:
                        print("removing")
                        remove_folders(extracted_files)
                        raise HTTPException(status_code=404, detail="This isn't a Java Project")
                    if len(functions) < 5:
                        remove_folders(extracted_files)
                        raise HTTPException(status_code=500, detail="This project is too small to be deployed")

                    selected_functions = random.sample(functions, 3)
                    functions_string = "\n".join(selected_functions)
                    maintainability = check_maintainability(functions_string)
                    searched_folders.append(str(extracted_file))
                    remove_folders(extracted_files)

            return {
                "rating": rating,
                "maintainability": maintainability
            }

    except Exception as e:
        raise e


def check_maintainability(code):
    # prompt = "those are 3 functions form a project Please check the following functions and tell me if it's maintainable or not:\n\n" + code + "\n\nWhat are the potential issues with this code?\n\nWhat changes would you suggest to improve its maintainability?\n\nAnswer: "
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


def remove_folders(extracted_files):
    removed_folders = []
    for extracted_file in extracted_files:
        if not str(extracted_file).split("/")[0] + "/" in removed_folders:
            if os.path.exists(extracted_file):
                if os.path.isdir(extracted_file):
                    shutil.rmtree(extracted_file)
                else:
                    os.remove(extracted_file)

            removed_folders.append(str(extracted_file))
