print("📌 Script started (TOP LEVEL)- 2")

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
from urllib.parse import urljoin
from datetime import datetime
from kafka import KafkaProducer

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

OUTPUT_FILE = "news-pipeline/scrapers/BBC/bbc_all_articles.json"
KAFKA_TOPIC = "bbc-news-stream"

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_html(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException as err:
        print(f"Error fetching {url}: {err}")
        return None

def get_all_bbc_sections():
    homepage = "https://www.bbc.com"
    try:
        res = fetch_html(homepage)
        soup = BeautifulSoup(res.text, 'html.parser')
        section_links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if (
                href.startswith("/news") or href.startswith("/sport") or
                href.startswith("/business") or href.startswith("/culture") or
                href.startswith("/travel") or href.startswith("/future-planet") or
                href.startswith("/innovation") or href.startswith("/arts")
            ):
                full_url = urljoin(homepage, href)
                if 'live' not in full_url and '#' not in full_url:
                    section_links.add(full_url)
        return list(section_links)
    except Exception as e:
        print(f"❌ Failed to fetch sections: {e}")
        return []

def extract_element(soup, selector=None, tag=None, attr=None):
    try:
        if tag:
            el = soup.find(tag)
        else:
            el = soup.select_one(selector) if selector else None
        if el:
            return el.get(attr) if attr else el.get_text(strip=True)
    except Exception:
        return None
    return None

def get_article_links(section_url, pages=10):
    links = set()
    for page in range(1, pages + 1):
        url = section_url if page == 1 else f"{section_url}?page={page}"
        res = fetch_html(url)
        if res:
            soup = BeautifulSoup(res.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith("/news") or href.startswith("/sport"):
                    links.add(urljoin("https://www.bbc.com", href))
    return list(links)

def extract_article(url):
    res = fetch_html(url)
    if not res:
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    content = "\n".join(p.get_text(strip=True) for p in (soup.find('article') or soup.find('main') or soup).find_all('p'))

    article = {
        "source": "BBC",
        "title": extract_element(soup, tag='h1'),
        "summary": content[:200] if content else None,
        "published_date": extract_element(soup, tag='time', attr='datetime'),
        "author": extract_element(soup, selector="meta[name='byl']", attr='content') or
                  extract_element(soup, selector='.byline__name') or
                  extract_element(soup, selector='[rel="author"]'),
        "url": url,
        "content": content
    }
    return article

def is_recent(published_date):
    try:
        pub_date = datetime.fromisoformat(published_date.replace("Z", ""))
        return (datetime.now() - pub_date).days < 2
    except Exception:
        return True

def load_existing_data():
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("⚠️ JSON decode failed. Starting fresh.")
    return []

def save_to_json(data):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def scrape_and_produce():
    articles = load_existing_data()
    seen_urls = {a['url'] for a in articles if 'url' in a}

    sections = get_all_bbc_sections()
    print(f"📚 Found {len(sections)} sections to scrape.")

    for section in sections:
        print(f"🔍 Crawling: {section}")
        for link in get_article_links(section):
            if link in seen_urls:
                continue
            article = extract_article(link)
            if article and is_recent(article.get("published_date")):
                articles.append(article)
                seen_urls.add(link)
                producer.send(KAFKA_TOPIC, article)
                time.sleep(random.uniform(1.5, 3.0))

    producer.flush()
    return articles

def main():
    print("🚀 Starting BBC Producer")
    all_articles = scrape_and_produce()
    print(f"✅ Total scraped: {len(all_articles)}")
    save_to_json(all_articles)
    print("💾 Saved to JSON and sent to Kafka.")

if __name__ == "__main__":
    main()
