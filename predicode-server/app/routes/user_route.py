from fastapi import APIRouter
from controllers.user_controller.user_controller import get_history, upload_file, verify_user, update_info
from middlewares.authMiddleware import get_current_user
from fastapi import Depends
from models.userModel import User
from request_models.userRequest import FileRequest, UpdateRequest
from fastapi import File, UploadFile

router = APIRouter()


@router.get("/get_history")
async def history(user: User = Depends(get_current_user)):
    return get_history(user)


@router.post("/upload_files")
async def upload(file: FileRequest, user: User = Depends(get_current_user)):
    return upload_file(file, user=user)


@router.get("/verify")
async def verify(user: User = Depends(get_current_user)):
    return verify_user(user=user)


@router.post("/update")
async def update(file: UpdateRequest, user: User = Depends(get_current_user)):
    return update_info(request=file, user=user)
