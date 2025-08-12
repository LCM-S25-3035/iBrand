from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Kafka config
KAFKA_TOPIC = "bbc-news-stream"
KAFKA_BOOTSTRAP_SERVER = "kafka:9092"

# MongoDB config
MONGO_URI = "mongodb://host.docker.internal:27017"
MONGO_DB = "news"
MONGO_COLLECTION = "bbc_articles"

# MongoDB connection
client = MongoClient(MONGO_URI)
collection = client[MONGO_DB][MONGO_COLLECTION]

# Connect to Kafka
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    auto_offset_reset='earliest',
    group_id='bbc-consumer-group',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("✅ Kafka consumer started. Waiting for messages...")

# Consume messages
for message in consumer:
    try:
        article = message.value
        print(f"📥 Received message: {json.dumps(article)[:100]}...")
        if collection.count_documents({'url': article['url']}, limit=1) == 0:
            collection.insert_one(article)
            print(f"✅ Inserted: {article['title']}")
        else:
            print(f"⚠️ Skipped duplicate: {article['title']}")
    except Exception as e:
        print(f"❌ Error processing message: {e}")
