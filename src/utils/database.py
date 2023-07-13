from pymongo import MongoClient
from .settings import MongoSettings 

mongo_settings = MongoSettings()
mongo_client = MongoClient(mongo_settings.uri)
mongo_collection = mongo_client[mongo_settings.database][mongo_settings.collection]
