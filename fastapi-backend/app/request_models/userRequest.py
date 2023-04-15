from fastapi import UploadFile, File, Form
from pydantic import BaseModel
import zipfile
from io import BytesIO
from typing import List



class FileRequest(BaseModel):
    file: UploadFile = File(...)
    name: str = Form(...)


class SubFile(BaseModel):
    filename: str
    contents: bytes


class UploadFolder(BaseModel):
    folder: UploadFile
    sub_files: List[SubFile]

    def __init__(self, folder: UploadFile):
        self.folder = folder
        self.sub_files = []
        with zipfile.ZipFile(folder.file, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                with zip_ref.open(filename) as sub_file:
                    sub_file_object = SubFile(
                        filename=filename,
                        contents=sub_file.read(),
                    )
                    self.sub_files.append(sub_file_object)
