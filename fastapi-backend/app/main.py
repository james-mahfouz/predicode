from configs.config import DB_NAME, DB_HOST, DB_PORT
# from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from fastapi import FastAPI
from mongoengine import connect, get_db
from configs.db_config import db_connection_keep_on

app = FastAPI()

connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)
db = get_db()

db_connection_keep_on(client=db)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# router = APIRouter()
@app.get("/")
def read_root():
    return {
        "Hello": "World"
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
