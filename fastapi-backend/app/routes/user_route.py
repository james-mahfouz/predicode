from fastapi import APIRouter, UploadFile, File
from controllers.user_controller import get_files, upload_file, verify_user
from middlewares.authMiddleware import get_current_user
from fastapi import Depends
from models.userModel import User
from request_models.userRequest import FileRequest

router = APIRouter()


@router.get("/get_files")
async def files(user: User = Depends(get_current_user)):
    return get_files(user)


@router.post("/upload_files")
async def upload(file: FileRequest, user: User = Depends(get_current_user)):
    return upload_file(file, user=user)


@router.get("/verify")
async def verify(user: User = Depends(get_current_user)):
    return verify_user(user=user)