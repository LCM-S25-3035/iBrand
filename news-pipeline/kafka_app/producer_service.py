# kafka/producer.py

from kafka import KafkaProducer
import json
from scrapers.bbc_trend.bbc import scrape_bbc_full_articles
from scrapers.techcrunch.techcrunch import scrape_multiple_articles
from scrapers.sportingNews.sporting_news_scrape import main as sporting_main
from scrapers.vogue.vogue_scrape import scrape_multiple_articles as scrape_vogue
from kafka_app.config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS
import asyncio



def send_articles_to_kafka():
    print("Scraping BBC articles...")
    articles = scrape_bbc_full_articles()

    print(f"Found {len(articles)} articles. Connecting to Kafka...")
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    for article in articles:
        try:
            producer.send(KAFKA_TOPIC, article)
            print(f"Sent to Kafka: {article['title']}")
        except Exception as e:
            print(f"Failed to send: {e}")

    producer.flush()
    print("All BBC articles sent!")

    # TechCrunch
    print("Scraping TechCrunch Articles.")
    scrape_multiple_articles()
    print("All TechCrunch articles sent!")

    # Sporting News
    print("Scraping Sporting News Article.")
    asyncio.run(sporting_main()) 
    print("All Sporting News Article sent")
    print("Scraping vouge articles")
    
    # Vogue
    print("Scraping Vogue articles...")
    vogue_articles = scrape_vogue()
    print(f"Vogue Articles found: {len(vogue_articles)}")
    scrape_vogue(producer, vogue_articles, source_name="VOGUE")

    producer.flush()
    print("All articles sent to Kafka!")


if __name__ == "__main__":
    send_articles_to_kafka()
