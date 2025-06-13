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

def get_article_links(section_url, pages=2):
    all_links = set()
    for page in range(1, pages + 1):
        url = section_url if page == 1 else f"{section_url}?page={page}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith("/news") or href.startswith("/sport"):
                    full_url = urljoin("https://www.bbc.com", href)
                    all_links.add(full_url)
        except requests.RequestException as err:
            print(f"Error accessing {url}: {err}")
    return list(all_links)

def fetch_html(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException as err:
        print(f"Error fetching {url}: {err}")
        return None

def extract_title(soup):
    title_tag = soup.find('h1')
    return title_tag.get_text(strip=True) if title_tag else None

def extract_date(soup):
    time_tag = soup.find('time')
    return time_tag.get('datetime') if time_tag else None

def extract_content(soup):
    body_tag = soup.find('article') or soup.find('main')
    if not body_tag:
        return ""
    return "\n".join(p.get_text(strip=True) for p in body_tag.find_all('p'))

def extract_summary(content):
    return content[:200] if content else None

def extract_author(soup):
    meta_author = soup.find("meta", {"name": "byl"})
    if meta_author and meta_author.get("content"):
        return meta_author["content"].replace("By", "").strip()

    selectors = [
        '.byline__name', '[rel="author"]',
        'span.ssrcss-1pjc44v-Contributor', 'span.sc-801dd632-7.lasLGY'
    ]
    for selector in selectors:
        tag = soup.select_one(selector)
        if tag:
            return tag.get_text(strip=True)
    return None

def is_recent(published_date):
    if published_date:
        try:
            pub_date = datetime.fromisoformat(published_date.replace("Z", ""))
            return (datetime.now() - pub_date).days < 2
        except ValueError:
            return True
    return True

def extract_article(url):
    res = fetch_html(url)
    if not res:
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    title = extract_title(soup)
    published_date = extract_date(soup)
    content = extract_content(soup)
    summary = extract_summary(content)
    author = extract_author(soup)

    return {
        "source": "BBC",
        "title": title,
        "summary": summary,
        "published_date": published_date,
        "author": author,
        "url": url,
        "content": content
    }

def load_existing_data():
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Warning: Failed to decode existing JSON. Starting fresh.")
    return []

def scrape_bbc_all():
    existing_articles = load_existing_data()
    existing_urls = {article['url'] for article in existing_articles if 'url' in article}
    all_articles = existing_articles.copy()

    for section in SECTION_LINKS:
        print(f"Crawling section: {section}")
        links = get_article_links(section)
        for link in links:
            if link in existing_urls:
                continue
            article = extract_article(link)
            if article and is_recent(article.get("published_date")):
                all_articles.append(article)
                existing_urls.add(link)
                producer.send(KAFKA_TOPIC, article)
                time.sleep(random.uniform(1.5, 3.0))
    producer.flush()
    return all_articles

def save_to_json(data):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def main():
    print("Starting BBC Scraper...")
    articles = scrape_bbc_all()
    print(f"📰 Total articles scraped: {len(articles)}")
    save_to_json(articles)
    print("Finished scraping and saving to JSON.")

if __name__ == '__main__':
    main()
