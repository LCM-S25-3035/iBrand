from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get Mongo URI
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["iBrandDB"]
collection = db["test_collection"]

# Insert a test document
result = collection.insert_one({"test": "MongoDB connection success!"})
print("✅ Inserted test document successfully!", result.inserted_id)
