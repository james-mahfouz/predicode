from fastapi import APIRouter
from controllers.auth_controller import login, register

router = APIRouter()


@router.post("/login")
async def do_login():
    result = await login()
    return result


@router.post("/register")
async def do_register():
    result = await register()
    return result

