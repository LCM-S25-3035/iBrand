import os
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from kafka import KafkaProducer

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

OUTPUT_FILE = "news-pipeline/scrapers/BBC/bbc_all_articles.json"
KAFKA_TOPIC = "bbc-news-stream"

SECTION_LINKS = [  # (Same as your original list, trimmed here for clarity)
    "https://www.bbc.com/news/topics/c2vdnvdg6xxt",
    "https://www.bbc.com/news/war-in-ukraine",
    "https://www.bbc.com/news/world/asia",
    "https://www.bbc.com/future-planet/green-living"
]

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

def extract_text(soup, selector, attr=None, default=None):
    tag = soup.select_one(selector)
    if tag:
        return tag.get(attr) if attr else tag.get_text(strip=True)
    return default

def extract_title(soup):
    return extract_text(soup, "h1")

def extract_date(soup):
    return extract_text(soup, "time", "datetime")

def extract_content(soup):
    body_tag = soup.find('article') or soup.find('main')
    return "\n".join(p.get_text(strip=True) for p in body_tag.find_all('p')) if body_tag else ""

def extract_summary(content):
    return content[:200] if content else None

def extract_author(soup):
    meta = soup.find("meta", {"name": "byl"})
    if meta and meta.get("content"):
        return meta["content"].replace("By", "").strip()
    for selector in ['.byline__name', '[rel="author"]', 'span.ssrcss-1pjc44v-Contributor', 'span.sc-801dd632-7.lasLGY']:
        text = extract_text(soup, selector)
        if text:
            return text
    return None

def is_recent(published_date):
    try:
        pub_date = datetime.fromisoformat(published_date.replace("Z", ""))
        return (datetime.now() - pub_date).days < 2
    except Exception:
        return True

def get_article_links(section_url, pages=2):
    links = set()
    for page in range(1, pages + 1):
        url = section_url if page == 1 else f"{section_url}?page={page}"
        try:
            res = fetch_html(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith("/news") or href.startswith("/sport"):
                    links.add(urljoin("https://www.bbc.com", href))
        except Exception as err:
            print(f"Error accessing {url}: {err}")
    return list(links)

def extract_article(url):
    res = fetch_html(url)
    if not res:
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    content = extract_content(soup)
    return {
        "source": "BBC",
        "title": extract_title(soup),
        "summary": extract_summary(content),
        "published_date": extract_date(soup),
        "author": extract_author(soup),
        "url": url,
        "content": content
    }

def load_existing_data():
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON. Starting fresh.")
    return []

def save_to_json(data):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scrape_bbc_all():
    existing = load_existing_data()
    seen_urls = {a['url'] for a in existing if 'url' in a}
    all_articles = existing.copy()

    for section in SECTION_LINKS:
        print(f"🔍 Scanning section: {section}")
        links = get_article_links(section)
        for link in links:
            if link in seen_urls:
                continue
            article = extract_article(link)
            if article and is_recent(article.get("published_date")):
                all_articles.append(article)
                seen_urls.add(link)
                producer.send(KAFKA_TOPIC, article)
                print(f"[Kafka] Sent: {article['title']}")
            time.sleep(random.uniform(1.5, 3.0))
    return all_articles

def main():
    print("🚀 Starting BBC Kafka Producer...")
    articles = scrape_bbc_all()
    save_to_json(articles)
    print(f"✅ Done! Scraped and sent {len(articles)} articles.")

if __name__ == '__main__':
    main()
