from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from kafka import KafkaProducer
import json
import time
import os

OUTPUT_FILE = "techcrunch_articles.json"
MAX_ARTICLES = 200
KAFKA_TOPIC = "techcrunch-articles"
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

# Setup Kafka producer
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

# Load already-scraped URLs
def get_existing_urls():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return {a["url"] for a in json.load(f)}
    return set()

def get_article_links(page, target_count, seen_urls):
    collected_links = set()
    last_page_links = None
    page_number = 1

    # Step 1: Scrape homepage
    print("--- Scraping Homepage: https://techcrunch.com ---")
    page.goto("https://techcrunch.com", timeout=60000)
    try:
        page.wait_for_selector("h3.loop-card__title a", timeout=10000)
        anchors = page.query_selector_all("h3.loop-card__title a")
        homepage_links = {
            a.get_attribute("href")
            for a in anchors
            if a.get_attribute("href") and
               "techcrunch.com" in a.get_attribute("href") and
               "/video/" not in a.get_attribute("href") and
               "/gallery/" not in a.get_attribute("href")
        }
        new_home_links = homepage_links - seen_urls
        collected_links.update(new_home_links)
        print(f"Homepage articles collected: {len(new_home_links)}")
    except Exception as e:
        print(f"Failed to scrape homepage: {e}")

    # Step 2: Visit /latest/ and paginate
    current_url = "https://techcrunch.com/latest/"

    while len(collected_links) < target_count:
        print(f"\n--- Scraping Page {page_number}: {current_url} ---")
        page.goto(current_url, timeout=60000)

        try:
            page.wait_for_selector("h3.loop-card__title a", timeout=10000)
            anchors = page.query_selector_all("h3.loop-card__title a")
            page_links = {
                a.get_attribute("href")
                for a in anchors
                if a.get_attribute("href") and
                   "techcrunch.com" in a.get_attribute("href") and
                   "/video/" not in a.get_attribute("href") and
                   "/gallery/" not in a.get_attribute("href")
            }

            # Stop if page content is same as previous
            if page_links == last_page_links:
                print("No new links found on this page, stopping.")
                break
            last_page_links = page_links

            new_links = page_links - seen_urls - collected_links
            if not new_links:
                print("All links on this page already seen, stopping.")
                break

            collected_links.update(new_links)
            print(f"Total articles collected so far: {len(collected_links)}")

        except Exception as e:
            print(f"Error scraping links: {e}")
            break

        # Scroll to load pagination
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)

        next_button = page.query_selector("a.wp-block-query-pagination-next")
        next_href = next_button.get_attribute("href") if next_button else None
        if not next_href or next_href == current_url:
            print("No next page found or loop detected, stopping.")
            break

        current_url = next_href
        page_number += 1

    return list(collected_links)[:target_count]


def scrape_single_article(page, url):
    try:
        page.goto(url, timeout=60000)

        title = page.query_selector("h1")
        author = (page.query_selector(".wp-block-tc23-author-card-name") or
                  page.query_selector(".article__byline a") or
                  page.query_selector(".river-byline__authors a"))
        date = page.query_selector("time[datetime]")
        summary = page.query_selector("p#speakable-summary")
        paragraphs = page.query_selector_all("div.entry-content p.wp-block-paragraph")

        content = "\n".join([
            page.evaluate("(el) => el.textContent", p)
            for p in paragraphs if page.evaluate("(el) => el.textContent.trim()", p)
        ])

        return {
            "url": url,
            "source": urlparse(url).hostname.replace("www.", ""),
            "title": title.inner_text().strip() if title else "Unknown",
            "author": author.inner_text().strip() if author else "Unknown",
            "published_at": date.get_attribute("datetime") if date else "Unknown",
            "summary": summary.inner_text().strip() if summary else "Not found",
            "content": content
        }

    except Exception as e:
        print(f"Failed to extract article at {url}: {e}")
        return None

# Scrape multiple articles and send to Kafka
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
        page = browser.new_page(user_agent="Mozilla/5.0")

        print("Collecting article links...")
        new_links = get_article_links(page, target_count=limit - len(seen_urls), seen_urls=seen_urls)
        print(f"Found {len(new_links)} new articles.")

        new_articles = []
        for i, link in enumerate(new_links, 1):
            print(f"[{i}/{len(new_links)}] Scraping: {link}")
            article = scrape_single_article(page, link)
            if article and article["url"] not in seen_urls:
                send_to_kafka(producer, KAFKA_TOPIC, article)
                new_articles.append(article)
                seen_urls.add(article["url"])
            time.sleep(1)

        browser.close()

    all_articles = existing_data + new_articles
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_articles[:MAX_ARTICLES], f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_articles[:MAX_ARTICLES])} articles to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_multiple_articles()
