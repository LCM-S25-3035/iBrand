import feedparser
import requests
from bs4 import BeautifulSoup
import json
import time
import os
import logging
from kafka import KafkaProducer
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
RSS_FEEDS = [
    "https://www.aljazeera.com/xml/rss/all.xml?category=africa",
    "https://www.aljazeera.com/xml/rss/all.xml?category=asia",
    "https://www.aljazeera.com/xml/rss/all.xml?category=middle-east",
    "https://www.aljazeera.com/xml/rss/all.xml?category=europe",
    "https://www.aljazeera.com/xml/rss/all.xml?category=us-canada",
    "https://www.aljazeera.com/xml/rss/all.xml?category=latin-america",
    "https://www.aljazeera.com/xml/rss/all.xml?category=economy",
    "https://www.aljazeera.com/xml/rss/all.xml?category=opinion",
    "https://www.aljazeera.com/xml/rss/all.xml?category=features",
    "https://www.aljazeera.com/xml/rss/all.xml?category=in-pictures",
    "https://www.aljazeera.com/xml/rss/all.xml?category=video",
    "https://www.aljazeera.com/xml/rss/all.xml?category=coronavirus-pandemic",
    "https://www.aljazeera.com/xml/rss/all.xml?category=investigations"
]

OUTPUT_FILE = "aljazeera_articles.json"
KAFKA_TOPIC = "real-news-aljazeera"
KAFKA_SERVER = 'localhost:9092'

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])

def fetch_article_content(url):
    if not is_valid_url(url):
        logging.warning(f"Invalid URL skipped: {url}")
        return "Invalid URL"

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='l-col l-col--8')
        if not content_div:
            return "Full content not found"
        paragraphs = content_div.find_all('p')
        return "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)) or "Content empty"
    except requests.RequestException as e:
        logging.error(f"Request error for {url}: {e}")
        return f"Error fetching content: {str(e)}"

def load_existing_articles():
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                articles = json.load(f)
                return articles, set(article.get("url") for article in articles)
        except Exception as e:
            logging.error(f"Failed to read existing file: {e}")
    return [], set()

def build_article(entry):
    return {
        "url": entry.link,
        "source": "Al Jazeera",
        "title": entry.title,
        "author": entry.get("author", "N/A"),
        "published_at": entry.get("published", "N/A"),
        "summary": entry.get("summary", "N/A"),
        "content": fetch_article_content(entry.link)
    }

def fetch_articles():
    existing_articles, seen_links = load_existing_articles()
    new_articles = []

    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except Exception as e:
        logging.error(f"Failed to connect to Kafka: {e}")
        return

    for feed_url in RSS_FEEDS:
        logging.info(f"Fetching RSS feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            if entry.link in seen_links:
                continue

            article = build_article(entry)
            new_articles.append(article)
            seen_links.add(entry.link)

            try:
                producer.send(KAFKA_TOPIC, article)
                logging.info(f"Published article: {entry.title}")
            except Exception as e:
                logging.error(f"Kafka send failed for {entry.title}: {e}")

            time.sleep(1)

    producer.flush()
    producer.close()

    all_articles = existing_articles + new_articles
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Failed to write to output file: {e}")

    logging.info(f"✅ Added {len(new_articles)} new articles. Total stored: {len(all_articles)}")

if __name__ == "__main__":
    try:
        fetch_articles()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")


