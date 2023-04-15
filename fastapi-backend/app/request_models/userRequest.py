from fastapi import UploadFile, File, Form
from pydantic import BaseModel
import zipfile
from io import BytesIO
from typing import List


class FileRequest(BaseModel):
    file: UploadFile = File(...)
    name: str = Form(...)


