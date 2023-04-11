import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient

load_dotenv()

app = FastAPI()

client = MongoClient(os.getenv('DB_URL'))
db = client["predicode_db"]

if db is not None:
    print("MongoDB connected successfully")
else:
    print("Error connecting to MongoDB")
