from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "suraksha_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


def get_database():
    return db


async def close_database_connection():
    client.close()
