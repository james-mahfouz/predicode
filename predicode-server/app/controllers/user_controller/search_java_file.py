import glob
import os
import re


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
