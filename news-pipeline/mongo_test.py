from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# DEBUG: Check if URI is loaded
mongo_uri = os.getenv("MONGO_URI")
print("🔍 Loaded Mongo URI:", mongo_uri)

# Try connecting
try:
    client = MongoClient(mongo_uri)
    db = client["iBrandDB"]
    collection = db["test_collection"]

    # Insert a test document
    result = collection.insert_one({"test": "MongoDB connection success!"})
    print("✅ Inserted test document successfully!", result.inserted_id)

except Exception as e:
    print("❌ Failed to connect or insert:", e)
