from fastapi import APIRouter
from controllers.auth_controller import login, register

router = APIRouter()


@router.post("/login")
async def do_login(request):
    result = await login(request=request)
    return result


@router.post("/register")
async def do_register(request):
    result = await register(request=request)
    return result

