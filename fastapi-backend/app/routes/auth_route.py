from fastapi import APIRouter
from controllers.auth_controller import login, register
from request_models.authRequest import RegisterRequest

router = APIRouter()


# @router.post("/login")
# async def do_login(request):
#     result = await login(request=request)
#     return result

@router.post("/login")
async def login_user(user: RegisterRequest):
    return await login(user)

# @router.post("/register")
# async def register_user(user: NewUser):
#     return await register(request=request)
