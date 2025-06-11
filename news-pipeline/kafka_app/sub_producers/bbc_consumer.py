import os, json, logging
from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db["bbc_articles"]

consumer = KafkaConsumer(
    "bbc-news-stream",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="bbc-consumer-group"
)

logging.info("Listening for messages...")
for message in consumer:
    article = message.value
    collection.insert_one(article)
    logging.info(f"Inserted: {article.get('title', 'No Title')}")
