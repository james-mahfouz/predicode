from fastapi import APIRouter
from controllers.admin_controller import get_files, get_users, get_history
from middlewares.adminMiddleware import get_current_user
from fastapi import Depends
from models.userModel import User

router = APIRouter()


@router.get("/get_files")
async def files(user: User = Depends(get_current_user)):
    return get_files(user)


@router.get("/get_users")
async def users(user: User = Depends(get_current_user)):
    return get_users(user=user)


@router.get("/get_history")
async def history(user: User = Depends(get_current_user)):
    return get_history(user=user)
