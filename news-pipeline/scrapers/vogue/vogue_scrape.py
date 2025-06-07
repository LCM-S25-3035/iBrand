from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from kafka import KafkaProducer
from datetime import datetime
import json
import time
import os

OUTPUT_FILE = "vogue_output.json"
MAX_ARTICLES = 200
KAFKA_TOPIC = "vogue-articles"
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def send_to_kafka(producer, topic, article_data):
    try:
        producer.send(topic, article_data)
        producer.flush()
        print(f"Sent to Kafka: {article_data['title']}")
    except Exception as e:
        print(f"Kafka send failed: {e}")

def get_existing_urls():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return {a["url"] for a in json.load(f)}
    return set()

def scrape_vogue_article(page, url):
    try:
        page.goto(url, timeout=60000)

        title_el = page.query_selector('h1[data-testid="ContentHeaderHed"]')
        title = title_el.inner_text().strip() if title_el else "Unknown"

        author_el = page.query_selector('a.byline__name-link')
        author = author_el.inner_text().strip() if author_el else "Vogue"

        date_el = page.query_selector("time")
        date_val = date_el.get_attribute("datetime") if date_el else None
        published_at = (
            datetime.fromisoformat(date_val.replace("Z", "+00:00")).isoformat()
            if date_val else datetime.utcnow().isoformat() + "Z"
        )

        summary_el = page.query_selector("meta[name='description']")
        summary = summary_el.get_attribute("content").strip() if summary_el else "Not found"

        content_tags = page.query_selector_all("article p")
        content = "\n".join([p.inner_text().strip() for p in content_tags if p.inner_text().strip()])

        return {
            "url": url,
            "source": urlparse(url).hostname.replace("www.", ""),
            "title": title,
            "author": author,
            "published_at": published_at,
            "summary": summary,
            "content": content
        }

    except Exception as e:
        print(f"Failed to extract article at {url}: {e}")
        return None

def collect_vogue_links(page, seen_urls, limit=MAX_ARTICLES):
    collected_links = set()
    page.goto("https://www.vogue.com", timeout=60000)
    time.sleep(2)

    cards = page.query_selector_all('a[data-recirc-pattern="summary-item"]')
    for card in cards:
        href = card.get_attribute("href")
        if href and href.startswith("/article"):
            full_url = f"https://www.vogue.com{href}"
            if full_url not in seen_urls:
                collected_links.add(full_url)
        if len(collected_links) >= limit:
            break

    print(f"Collected {len(collected_links)} new article links.")
    return list(collected_links)

def scrape_multiple_articles(limit=MAX_ARTICLES):
    existing_data = []
    seen_urls = set()

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            seen_urls = {a["url"] for a in existing_data}

    producer = create_producer()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Gathering Vogue article links...")
        links = collect_vogue_links(page, seen_urls, limit=limit - len(seen_urls))
        print(f"Found {len(links)} new links.")

        new_articles = []
        for i, link in enumerate(links, 1):
            print(f"[{i}/{len(links)}] Scraping: {link}")
            if link in seen_urls:
                print("Duplicate article found. Stopping.")
                break

            article = scrape_vogue_article(page, link)
            if article:
                send_to_kafka(producer, KAFKA_TOPIC, article)
                new_articles.append(article)
                seen_urls.add(link)

            time.sleep(1)

        browser.close()

    # Save new + existing, capped to MAX_ARTICLES
    all_articles = existing_data + new_articles
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles[:MAX_ARTICLES], f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_articles[:MAX_ARTICLES])} articles to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_multiple_articles()
