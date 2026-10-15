from pymongo import AsyncMongoClient

from app.config import settings

client = AsyncMongoClient(settings.mongo_uri)
db = client[settings.mongo_db_name]
