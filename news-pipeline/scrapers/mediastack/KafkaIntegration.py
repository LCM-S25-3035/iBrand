import os
import json
import time
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from playwright.sync_api import sync_playwright
from kafka import KafkaProducer

# === 1. Kafka Producer Config ===
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
TOPIC_NAME = 'scraped-articles'

# === 2. API Config ===
API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX' 
BASE_URL = 'http://api.mediastack.com/v1/news'

# === 3. Excluded sources ===
EXCLUDED_SOURCES = [
    "9to5mac", "appleinsider", "ars technica", "bbc news", "bloomberg", "business insider", "cnet", "cnn",
    "engadget", "espn", "eurogamer", "financial post", "forbes", "fox news", "gamesradar", "gizmodo",
    "gsm arena", "ign", "marketwatch", "mashable", "nbc news", "npr", "polygon", "san francisco chronicle",
    "techcrunch", "techradar", "the verge", "tom’s hardware", "venturebeat", "wired", "yahoo finance",
    "npr.org", "aljazeera.com", "bbc.co.uk", "bbc.com", "reuters.com", "theguardian.com"
]

# === 4. Fetch articles using pagination ===
def fetch_articles(limit_per_page=100, max_articles=500):
    all_articles = []
    for offset in range(0, max_articles, limit_per_page):
        params = {
            'access_key': API_KEY,
            'languages': 'en',
            'limit': limit_per_page,
            'offset': offset
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"❌ Error fetching data: {response.status_code}")
            break

        data = response.json()
        batch = data.get('data', [])
        if not batch:
            break
        all_articles.extend(batch)
        print(f"📥 Fetched {len(batch)} articles (Offset: {offset})")
        time.sleep(1)
    return all_articles

# === 5. Fallback content extraction with Playwright ===
def fetch_with_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()
            soup = BeautifulSoup(html, 'html.parser')
            paragraphs = soup.find_all('p')
            text = '\n'.join([p.get_text() for p in paragraphs])
            return text.strip()
    except Exception as e:
        print(f"❌ Playwright failed for {url[:50]}... Error: {e}")
        return ''

# === 6. Try newspaper3k, fallback to Playwright ===
def get_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        if len(article.text) > 200:
            return article.text
        raise ValueError("Article too short, fallback needed")
    except:
        print(f"⚠️ Newspaper3k failed for {url}")
        print(f"🔁 Falling back to Playwright for {url}")
        return fetch_with_playwright(url)

# === 7. Main logic: Scrape → Send to Kafka ===
def process_and_send_to_kafka():
    articles = fetch_articles()
    new_count = 0

    for article in articles:
        url = article.get('url')
        source = article.get('source', '').lower()

        if not url or source in EXCLUDED_SOURCES:
            continue

        content = get_article_content(url)
        if not content or len(content) < 200:
            continue

        processed = {
            "source": article.get('source'),
            "title": article.get('title'),
            "summary": article.get('description'),
            "published_date": article.get('published_at'),
            "url": url,
            "author": article.get('author'),
            "content": content,
            "origin": "mediastack"
        }

        # === Send to Kafka ===
        producer.send(TOPIC_NAME, processed)
        print(f"📤 Sent to Kafka: {processed['title'][:60]}...")
        new_count += 1
        time.sleep(1)

    producer.flush()
    print(f"\n✅ Total {new_count} new articles sent to Kafka topic '{TOPIC_NAME}'.")

# === 8. Run Script ===
if __name__ == "__main__":
    process_and_send_to_kafka()
