from configs.config import DB_URL
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from fastapi import FastAPI
from pymongo import MongoClient
from controllers.db_controller import db_connection_keep_on

app = FastAPI()

router = APIRouter()

client = MongoClient(DB_URL)

predicode_client = client['predicode_db']

db_connection_keep_on(client=predicode_client)





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {
        "Hello": "World"
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
