from fastapi import UploadFile, File
from pydantic import BaseModel


class FileRequest(BaseModel):
    file: UploadFile = File(...)
    file_name: str = file.filename
