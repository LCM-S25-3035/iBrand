import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
from urllib.parse import urljoin
from datetime import datetime
from kafka import KafkaProducer

# Constants
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}
OUTPUT_FILE = "news-pipeline/scrapers/BBC/bbc_all_articles.json"
KAFKA_TOPIC = "bbc-news-stream"
BASE_URL = "https://www.bbc.com"

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# BBC Sections to Scrape
SECTION_LINKS = [
    "https://www.bbc.com/news/topics/c2vdnvdg6xxt",
    "https://www.bbc.com/news/war-in-ukraine",
    "https://www.bbc.com/news/us-canada",
    "https://www.bbc.com/news/uk",
    "https://www.bbc.com/news/world/africa",
    "https://www.bbc.com/news/world/asia",
    "https://www.bbc.com/news/world/australia",
    "https://www.bbc.com/news/world/europe",
    "https://www.bbc.com/news/world/latin_america",
    "https://www.bbc.com/news/world/middle_east",
    "https://www.bbc.com/news/in_pictures",
    "https://www.bbc.com/news/bbcverify",
    "https://www.bbc.com/sport",
    "https://www.bbc.com/sport/football",
    "https://www.bbc.com/sport/cricket",
    "https://www.bbc.com/sport/formula1",
    "https://www.bbc.com/sport/rugby-union",
    "https://www.bbc.com/sport/tennis",
    "https://www.bbc.com/sport/golf",
    "https://www.bbc.com/sport/athletics",
    "https://www.bbc.com/sport/cycling",
    "https://www.bbc.com/business/executive-lounge",
    "https://www.bbc.com/business/technology-of-business",
    "https://www.bbc.com/business/future-of-business",
    "https://www.bbc.com/innovation/technology",
    "https://www.bbc.com/innovation/science",
    "https://www.bbc.com/innovation/artificial-intelligence",
    "https://www.bbc.com/innovation/ai-v-the-mind",
    "https://www.bbc.com/culture/film-tv",
    "https://www.bbc.com/culture/music",
    "https://www.bbc.com/culture/art",
    "https://www.bbc.com/culture/style",
    "https://www.bbc.com/culture/books",
    "https://www.bbc.com/culture/entertainment-news",
    "https://www.bbc.com/arts/arts-in-motion",
    "https://www.bbc.com/travel/destinations",
    "https://www.bbc.com/travel/worlds-table",
    "https://www.bbc.com/travel/cultural-experiences",
    "https://www.bbc.com/travel/adventures",
    "https://www.bbc.com/future-planet/natural-wonders",
    "https://www.bbc.com/future-planet/weather-science",
    "https://www.bbc.com/future-planet/solutions",
    "https://www.bbc.com/future-planet/sustainable-business",
    "https://www.bbc.com/future-planet/green-living"
]

# Reusable Helpers
def get_soup(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as err:
        print(f"Error fetching {url}: {err}")
        return None

def extract_tag_text(soup, selector, attr=None):
    tag = soup.select_one(selector)
    if not tag:
        return None
    return tag.get(attr).strip() if attr else tag.get_text(strip=True)

def delay(min_sec=1.5, max_sec=3.0):
    time.sleep(random.uniform(min_sec, max_sec))

def read_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Failed to decode existing JSON.")
    return []

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Article Utilities
def get_article_links(section_url, pages=2):
    all_links = set()
    for page in range(1, pages + 1):
        page_url = section_url if page == 1 else f"{section_url}?page={page}"
        soup = get_soup(page_url)
        if not soup:
            continue
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith("/news") or href.startswith("/sport"):
                full_url = urljoin(BASE_URL, href)
                all_links.add(full_url)
    return list(all_links)

def is_recent(published_date):
    if published_date:
        try:
            pub_date = datetime.fromisoformat(published_date.replace("Z", ""))
            return (datetime.now() - pub_date).days < 2
        except ValueError:
            return True
    return True

def extract_article(url):
    soup = get_soup(url)
    if not soup:
        return None

    title = extract_tag_text(soup, 'h1')
    published_date = extract_tag_text(soup, 'time', attr='datetime')
    content_block = soup.find('article') or soup.find('main')
    content = "\n".join(p.get_text(strip=True) for p in content_block.find_all('p')) if content_block else ""
    summary = content[:200] if content else None

    author = None
    meta_author = soup.find("meta", {"name": "byl"})
    if meta_author and meta_author.get("content"):
        author = meta_author["content"].replace("By", "").strip()
    else:
        selectors = ['.byline__name', '[rel="author"]', 'span.ssrcss-1pjc44v-Contributor', 'span.sc-801dd632-7.lasLGY']
        for selector in selectors:
            author = extract_tag_text(soup, selector)
            if author:
                break

    return {
        "source": "BBC",
        "title": title,
        "summary": summary,
        "published_date": published_date,
        "author": author,
        "url": url,
        "content": content
    }

# Main Scraper Logic
def scrape_bbc_all():
    existing_articles = read_json(OUTPUT_FILE)
    existing_urls = {a['url'] for a in existing_articles if 'url' in a}
    all_articles = existing_articles.copy()

    for section in SECTION_LINKS:
        print(f"Scraping section: {section}")
        links = get_article_links(section)
        for link in links:
            if link in existing_urls:
                continue
            article = extract_article(link)
            if article and is_recent(article.get("published_date")):
                all_articles.append(article)
                existing_urls.add(link)
                producer.send(KAFKA_TOPIC, article)
            delay()
    return all_articles

def main():
    articles = scrape_bbc_all()
    write_json(OUTPUT_FILE, articles)
    print(f"Done! Total articles scraped: {len(articles)}")

if __name__ == '__main__':
    main()
