import os

from pymongo import MongoClient

from .settings import default_settings

default_mongo_client = MongoClient(default_settings.uri)
default_db = default_mongo_client[default_settings.database]
