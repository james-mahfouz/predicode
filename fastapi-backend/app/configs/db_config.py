from configs.config import DB_URL
from pymongo import MongoClient
from controllers.db_controller import db_connection_keep_on

client = MongoClient(DB_URL)

db = db_connection_keep_on()
