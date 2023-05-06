import os
from zipfile import ZipFile


def unzip_file(file_path):
    extracted_files = []
    with ZipFile(file_path, "r") as zip_ref:
        for filename in zip_ref.namelist():
            if not filename.startswith("__MACOSX"):
                zip_ref.extract(filename)
                if os.path.exists(filename):
                    extracted_files.append(filename)
    return extracted_files
