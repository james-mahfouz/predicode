from fastapi import APIRouter
from controllers.user_controller import get_files
from middlewares.authMiddleware import get_current_user
from fastapi import Depends
from models.userModel import User

router = APIRouter()



@router.get("/get_files")
async def files(user: User = Depends(get_current_user)):
    return get_files()
