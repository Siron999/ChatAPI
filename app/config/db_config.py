from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .logger_config import logger

uri = "mongodb://mongouser:password123@localhost:27017/?authSource=admin"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.chatapi
user_collections = db["users"]

try:
    client.admin.command("ping")
    logger.info("MongoDB connection estyablished successfully!")
except Exception as e:
    print(e)
