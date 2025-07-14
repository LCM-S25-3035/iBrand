from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
print("🔍 Loaded Mongo URI:", mongo_uri)

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["iBrandDB"]
collection = db["test_collection"]

# Insert a test document
collection.insert_one({"test": "MongoDB connection success!"})
print("✅ Inserted test document successfully!")
