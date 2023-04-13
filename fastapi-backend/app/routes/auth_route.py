from fastapi import APIRouter
from app.controllers.auth_controller import login, register

router = APIRouter()

router.post("/login", login)
router.post("/register", register)

