from bbc_full_scraper import scrape_bbc_all, save_to_json
import json
import logging
from kafka import KafkaProducer

KAFKA_TOPIC = "bbc-news-stream"
KAFKA_SERVER = "kafka:9092"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_articles_to_kafka(articles):
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
    except Exception as e:
        logging.error(f"Kafka connection failed: {e}")
        return

    for article in articles:
        try:
            producer.send(KAFKA_TOPIC, article)
            logging.info(f"Sent to Kafka: {article.get('title')[:60]}")
        except Exception as e:
            logging.error(f"Failed to send article: {e}")

    producer.flush()
    producer.close()

def main():
    logging.info("Starting BBC Producer...")
    articles = scrape_bbc_all()
    send_articles_to_kafka(articles)
    save_to_json(articles)
    logging.info(f"Finished! {len(articles)} articles processed.")

if __name__ == "__main__":
    main()
