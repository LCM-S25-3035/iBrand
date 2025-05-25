# kafka/producer.py

from kafka import KafkaProducer
import json
from scrapers.bbc_trend.bbc import scrape_bbc_full_articles
from kafka_app.config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS


def send_articles_to_kafka():
    print("🕸️ Scraping BBC articles...")
    articles = scrape_bbc_full_articles()

    print(f"📦 Found {len(articles)} articles. Connecting to Kafka...")
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    for article in articles:
        try:
            producer.send(KAFKA_TOPIC, article)
            print(f"✅ Sent to Kafka: {article['title']}")
        except Exception as e:
            print(f"❌ Failed to send: {e}")

    producer.flush()
    print("🚀 All articles sent!")


if __name__ == "__main__":
    send_articles_to_kafka()
