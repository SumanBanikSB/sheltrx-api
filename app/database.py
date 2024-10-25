# app/database.py
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.config import settings

client = None
db = None

try:
    client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=5000)
    db = client[settings.database_name]
    client.admin.command("ping")
    print("Successfully connected to MongoDB!")

except ServerSelectionTimeoutError:
    print("Failed to connect to MongoDB. Please check your MongoDB URI and try again.")
    raise Exception("Database connection error")
