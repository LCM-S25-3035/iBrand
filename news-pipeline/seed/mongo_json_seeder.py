import os
import json
import re
from dotenv import load_dotenv
import argparse
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from datetime import datetime, timezone

# Load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")

def clean_newlines(text):
    """
    Removes newline and carriage return characters from text.
    """
    if isinstance(text, str):
        return re.sub(r'[\r\n]+', ' ', text).strip()
    return text

def clean_article(article):
    """
    Recursively cleans all string fields in the article dictionary.
    """
    cleaned_article = {}
    for key, value in article.items():
        if isinstance(value, str):
            cleaned_article[key] = clean_newlines(value)
        elif isinstance(value, list):
            cleaned_article[key] = [
                clean_article(v) if isinstance(v, dict)
                else clean_newlines(v) if isinstance(v, str)
                else v
                for v in value
            ]
        elif isinstance(value, dict):
            cleaned_article[key] = clean_article(value)
        else:
            cleaned_article[key] = value
    return cleaned_article

def seed_articles(file_path, db_name="articles-db", collection_name="articles", mongo_uri="mongodb://localhost:27017"):
    """
    Loads articles from a JSON file, cleans them, and inserts them into MongoDB.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return

    if not isinstance(data, list):
        print("Error: JSON must be a list of article objects.")
        return

    cleaned_data = []
    for article in data:
        cleaned_article = clean_article(article)
        # Use timezone-aware datetime instead of datetime.utcnow()
        cleaned_article["seeded_at"] = datetime.now(timezone.utc).isoformat()
        cleaned_data.append(cleaned_article)

    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        # Ensure unique index on 'url' to avoid duplicates
        collection.create_index("url", unique=True)
        result = collection.insert_many(cleaned_data, ordered=False)
        print(f"Inserted {len(result.inserted_ids)} cleaned articles into '{db_name}.{collection_name}'.")
    except BulkWriteError as bwe:
        inserted_count = len(cleaned_data) - len(bwe.details.get("writeErrors", []))
        print(f"Some duplicates skipped. Inserted {inserted_count} articles.")
    except Exception as e:
        print(f"Failed to insert into MongoDB: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed cleaned articles into MongoDB.")
    parser.add_argument("-i", "--inputjson", required=True, help="Path to the JSON file to seed.")
    parser.add_argument("-d", "--db", default="articles-db", help="MongoDB database name.")
    parser.add_argument("-c", "--collection", default="articles", help="MongoDB collection name.")
    parser.add_argument("-u", "--uri", default="mongodb://localhost:27017", help="MongoDB URI.")
    args = parser.parse_args()

    seed_articles(
        args.inputjson,
        db_name=args.db,
        collection_name=args.collection,
        mongo_uri=args.uri
    )
