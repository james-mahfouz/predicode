from fastapi import APIRouter
from controllers.auth_controller import login, register
from request_models.authRequest import RegisterRequest, LoginRequest

router = APIRouter()


# @router.post("/login")
# async def do_login(request):
#     result = await login(request=request)
#     return result

@router.post("/login")
async def login_user(request: LoginRequest):
    return await login(request=request)


@router.post("/register")
async def register_user(request: RegisterRequest):
    return await register(request=request)
