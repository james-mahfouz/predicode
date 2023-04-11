from configs.db_config import db
from fastapi import APIRouter
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from fastapi import FastAPI
# import sys
import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/configs')

print(db)

app = FastAPI()
load_dotenv()
router = APIRouter()

# print(os.environ['DB_URL'])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    cpu_count = os.cpu_count()
    return {
        "Hello": "World"
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
