from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["iBrandDB"]
collection = db["test_collection"]

# Insert a test document
collection.insert_one({"test": "MongoDB connection success!"})
print("✅ Inserted test document successfully!")
