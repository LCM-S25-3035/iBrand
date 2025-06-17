import json
import logging
from kafka import KafkaConsumer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
KAFKA_TOPIC = "real-news-aljazeera"
KAFKA_SERVER = 'localhost:9092'  # Same as used in the producer

def consume_articles():
    try:
        # Create Kafka consumer
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='aljazeera-consumer-group'
        )
        logging.info(f"Connected to Kafka topic: {KAFKA_TOPIC}")

        # Consume messages
        for message in consumer:
            article = message.value
            logging.info(f"Received article: {article['title']}")
            print(json.dumps(article, indent=2, ensure_ascii=False))  # For readability

    except Exception as e:
        logging.error(f"Consumer error: {e}")

if __name__ == "__main__":
    consume_articles()
