from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from fastapi import FastAPI
from configs.db_config import db_connection_keep_on
from fastapi.staticfiles import StaticFiles


from routes.auth_route import router as auth_router
from routes.user_route import router as user_router
from routes.admin_route import router as admin_router

from middlewares.authMiddleware import get_current_user

app = FastAPI()
db = db_connection_keep_on()
app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/auth")

app.include_router(user_router, prefix="/user")

app.include_router(admin_router, prefix="/admin")

# @app.get("/get_all_employees")
# def get_all_users():
#     users = json.loads(User.objects().to_json())
#
#     return {"users": users}
#
# @app.get("/")
# def read_root():
#     return {
#         "Hello": "World"
#     }
#

#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
