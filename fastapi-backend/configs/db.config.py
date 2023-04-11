import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("DB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)


async def connect_to_mongo():
    try:
        db = client.get_default_database()
        print("MongoDB connected successfully")
        return db
    except:
        print("Failed to connect to MongoDB")


async def close_mongo_connection():
    client.close()

db = await connect_to_mongo()
