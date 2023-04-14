from fastapi import UploadFile, File, Form
from pydantic import BaseModel


class FileRequest(BaseModel):
    file: UploadFile = File(...)
    name: str = Form(...)
