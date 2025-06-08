import os
import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv

# Load Mongo URI from .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")  # Atlas URI

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["multimodal"]
collection = db["posts"]

# Kafka Consumer setup
consumer = KafkaConsumer(
    'scraped-articles',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("📡 Listening to Kafka topic: scraped-articles...")

for message in consumer:
    article = message.value
    if not collection.find_one({"url": article.get("url")}):
        collection.insert_one(article)
        print(f"✅ Inserted: {article.get('title')[:60]}...")
    else:
        print(f"⚠️ Duplicate skipped: {article.get('title')[:60]}")
