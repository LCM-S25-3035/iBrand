import os
import json
from dotenv import load_dotenv
import argparse
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from datetime import datetime

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

def clean_newlines(text):
    """
    Removes newline and carriage return characters from text.
    """
    if isinstance(text, str):
        return text.replace('\n', ' ').replace('\r', ' ').strip()
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
                clean_newlines(v) if isinstance(v, str)
                else clean_article(v) if isinstance(v, dict)
                else v
                for v in value
            ]
        elif isinstance(value, dict):
            cleaned_article[key] = clean_article(value)
        else:
            cleaned_article[key] = value
    return cleaned_article

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

    # Clean and add timestamp at seeding
    cleaned_data = []
    for article in data:
        cleaned_article = clean_article(article)
        cleaned_article["seeded_at"] = datetime.utcnow().isoformat()
        cleaned_data.append(cleaned_article)

    # Connect to MongoDB and insert
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Create a unique index on 'url' to avoid duplicates
        collection.create_index("url", unique=True)

        # Attempt bulk insert
        result = collection.insert_many(cleaned_data, ordered=False)
        print(f"Inserted {len(result.inserted_ids)} new articles into '{db_name}.{collection_name}'")

    except BulkWriteError as bwe:
        inserted_count = len(cleaned_data) - len(bwe.details.get("writeErrors", []))
        print(f"Some duplicates skipped. Inserted {inserted_count} articles.")
    except Exception as e:
        print(f"Failed to insert into MongoDB: {e}")

def check_and_clean_existing_data(db_name="articles-db", collection_name="articles", mongo_uri="mongodb://localhost:27017", field_name="content", clean=False):
    """
    Checks existing data in MongoDB for newline characters in the specified field.
    If clean=True, it also removes the newline characters in-place.
    """
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        query = {field_name: {"$regex": r"[\n\r]"}}
        count = collection.count_documents(query)
        print(f"Found {count} documents with newline characters in '{field_name}' field.")

        if count == 0:
            print("No cleaning required.")
            return

        if clean:
            bulk_updates = []
            for doc in collection.find(query):
                cleaned_content = clean_newlines(doc[field_name])
                bulk_updates.append(
                    UpdateOne(
                        {"_id": doc["_id"]},
                        {"$set": {field_name: cleaned_content}}
                    )
                )

            if bulk_updates:
                result = collection.bulk_write(bulk_updates)
                print(f"Cleaned {result.modified_count} documents.")
            else:
                print("No documents needed cleaning.")
        else:
            print("Run with --clean flag to apply cleaning.")
    except Exception as e:
        print(f"Failed to check or clean data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed articles from a JSON file into MongoDB or check existing data.")
    parser.add_argument("-i", "--inputjson", help="Path to the JSON file")
    parser.add_argument("-d", "--db", default="articles-db", help="MongoDB database name")
    parser.add_argument("-c", "--collection", default="articles", help="MongoDB collection name")
    parser.add_argument("-u", "--uri", default="mongodb://localhost:27017", help="MongoDB connection URI")
    parser.add_argument("--check", action="store_true", help="Check existing data for newline characters")
    parser.add_argument("--clean", action="store_true", help="Clean newline characters in-place if found")

    args = parser.parse_args()

    if args.check:
        check_and_clean_existing_data(
            db_name=args.db,
            collection_name=args.collection,
            mongo_uri=args.uri,
            field_name="content",
            clean=args.clean
        )
    elif args.inputjson:
        seed_articles(args.inputjson, args.db, args.collection, args.uri)
    else:
        print("Please provide either an input JSON file (-i) or use --check to inspect existing data.")
