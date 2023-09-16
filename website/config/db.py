from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
# import motor.motor_asyncio

# conn = motor.motor_asyncio.AsyncIOMotorClient(config("MONGO_CREDENTIALS"))


conn = MongoClient(os.getenv("MONGO_CREDENTIALS"))

PORT_DB = os.getenv("PORT_DB")

db = conn[PORT_DB]
