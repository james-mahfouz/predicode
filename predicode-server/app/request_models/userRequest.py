from fastapi import UploadFile, File, Form
from pydantic import BaseModel
import zipfile
from io import BytesIO
from typing import List


class FileRequest(BaseModel):
    data: str
    content_type: str
    price: float
    category: str
    content_rating: str
    name: str
    size: float

