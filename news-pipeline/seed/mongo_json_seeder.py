import os
import json
from dotenv import load_dotenv
import argparse
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from datetime import datetime

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

def seed_articles(file_path, db_name="articles-db", collection_name="articles", mongo_uri="mongodb://localhost:27017"):
    # Load JSON
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return

    if not isinstance(data, list):
        print("JSON must be a list of article objects.")
        return

    # Adding timestamp at seeding
    for article in data:
        article["seeded_at"] = datetime.utcnow().isoformat()

    # Connect to MongoDB and insert
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Create a unique index on 'url' to avoid duplicates
        collection.create_index("url", unique=True)

        # Attempt bulk insert
        result = collection.insert_many(data, ordered=False)
        print(f"Inserted {len(result.inserted_ids)} new articles into '{db_name}.{collection_name}'")

    except BulkWriteError as bwe:
        inserted_count = len(bwe.details.get("writeErrors", []))
        print(f"Some duplicates skipped. Inserted {len(data) - inserted_count} articles.")
    except Exception as e:
        print(f"Failed to insert into MongoDB: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed articles from a JSON file into MongoDB.")
    parser.add_argument("-i", "--inputjson", required=True, help="Path to the JSON file")
    parser.add_argument("-d", "--db", default="articles-db", help="MongoDB database name")
    parser.add_argument("-c", "--collection", default="articles", help="MongoDB collection name")
    parser.add_argument("-u", "--uri", default="mongodb://localhost:27017", help="MongoDB connection URI")

    args = parser.parse_args()
    seed_articles(args.inputjson, args.db, args.collection, args.uri)
