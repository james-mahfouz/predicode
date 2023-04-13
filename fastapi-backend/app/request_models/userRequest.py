from fastapi import UploadFile, File
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    file: UploadFile = File(..., description="File to upload")
    file_name: str
    