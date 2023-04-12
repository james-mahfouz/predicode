from configs.config import DB_URL

from fastapi import FastAPI
from pymongo import MongoClient
from controllers.db_controller import db_connection_keep_on




client = MongoClient(DB_URL)

db = db_connection_keep_on()
print(db.name)



#     print("Error connecting to MongoDB")
