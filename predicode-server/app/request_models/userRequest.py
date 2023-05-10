from fastapi import UploadFile, File, Form
from pydantic import BaseModel
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile


class FileRequest(BaseModel):
    data: str
    content_type: str
    price: float
    category: str
    content_rating: str
    name: str
    size: float


class UpdateRequest(BaseModel):
    name: str
    email: str
    file_name: str
    profile_picture: str = None
