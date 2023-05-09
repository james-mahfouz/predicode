import random

from fastapi import HTTPException

from controllers.user_controller.check_maintainability import check_maintainability
from controllers.user_controller.remove_folder import remove_folders
from controllers.user_controller.search_java_file import search_java_files


def search_apply(extracted_files):
    searched_folders = []
    for extracted_file in extracted_files:
        if not str(extracted_file).split("/")[0] + "/" in searched_folders:
            functions = search_java_files(extracted_file)
            if len(functions) == 0:
                remove_folders(extracted_files)
                raise HTTPException(status_code=404, detail="This isn't a Java Project")
            if len(functions) < 5:
                remove_folders(extracted_files)
                raise HTTPException(status_code=500, detail="This project is too small to be deployed")

            selected_functions = random.sample(functions, 3)
            functions_string = "\n".join(selected_functions)
            maintainability = check_maintainability(functions_string)
            searched_folders.append(str(extracted_file))
            return maintainability
