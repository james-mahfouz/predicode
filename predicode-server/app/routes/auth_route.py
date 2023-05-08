from fastapi import APIRouter
from controllers.auth_controller import login, register, google_login
from request_models.authRequest import RegisterRequest, LoginRequest, GoogleRequest


router = APIRouter()


@router.post("/login")
async def login_user(request: LoginRequest):
    return await login(request=request)


@router.post("/register")
async def register_user(request: RegisterRequest):
    return await register(request=request)


@router.post("/google_login")
async def google_login_user(token: GoogleRequest):
    return await google_login(token)
