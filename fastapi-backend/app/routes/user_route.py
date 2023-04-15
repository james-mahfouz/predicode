from fastapi import APIRouter, File
from controllers.user_controller import get_files, upload_file
from middlewares.authMiddleware import get_current_user
from fastapi import Depends
from models.userModel import User
from request_models.userRequest import FileRequest, UploadFolder

router = APIRouter()


@router.get("/get_files")
async def files(user: User = Depends(get_current_user)):
    return get_files(user)


@router.post("/upload_files/")
async def upload(folder: UploadFolder = File(...), user: User = Depends(get_current_user)):
    return upload_file(folder, user=user)
