import feedparser
import requests
from bs4 import BeautifulSoup
import json
import time
import os
from kafka import KafkaProducer

# RSS feed list
rss_feeds = [
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

output_file = "aljazeera_articles.json"
kafka_topic = "real-news-aljazeera"

# Fetch full article content
def fetch_article_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        content_div = soup.find('div', class_='l-col l-col--8')
        if not content_div:
            return "Full content not found"

        paragraphs = content_div.find_all('p')
        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return content if content else "Content empty"
    except Exception as e:
        return f"Error fetching content: {str(e)}"

# Load already-saved articles from JSON
def load_existing_links():
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_articles = json.load(f)
        return existing_articles, set(article["url"] for article in existing_articles)
    return [], set()

# Fetch articles and send new ones to Kafka
def fetch_articles():
    existing_articles, existing_links = load_existing_links()
    new_articles = []

    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for feed_url in rss_feeds:
        print(f"Fetching RSS feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            if entry.link in existing_links:
                continue  # Skip already fetched article

            article = {
                "url": entry.link,
                "source": "Al Jazeera",
                "title": entry.title,
                "author": entry.get("author", "N/A"),
                "published_at": entry.get("published", "N/A"),
                "summary": entry.get("summary", "N/A"),
                "content": fetch_article_content(entry.link)
            }

            new_articles.append(article)
            existing_links.add(entry.link)
            print(f"✓ New: {entry.title}")

            # Send to Kafka
            producer.send(kafka_topic, article)

            time.sleep(1)

    # Flush and close Kafka producer
    producer.flush()
    producer.close()

    # Save all articles back to JSON
    all_articles = existing_articles + new_articles
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Added {len(new_articles)} new articles. Total: {len(all_articles)}")

if __name__ == "__main__":
    fetch_articles()
    input("Press Enter to exit...")

