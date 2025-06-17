import asyncio
import json
import re
import os
from datetime import datetime
from playwright.async_api import async_playwright
from kafka import KafkaProducer
from transformers import pipeline
import torch

# ─── Constants ────────────────────────────────────────────────────────────────
BASE_URL = "https://www.sportingnews.com"
SECTIONS = [
    "nfl", "nba", "mlb", "nhl", "mma", "nascar", "golf",
    "boxing", "tennis", "wwe", "ncaa-football", "ncaa-basketball"
]
MAX_ARTICLES = 10000
CONCURRENT_PAGES = 10
SUMMARY_BATCH_SIZE = 8
MAX_PAGES_PER_SECTION = 50
OUTPUT_FILE = "sportingnews_all_categories_articles.json"
KAFKA_TOPIC = "sportingnews-article"
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

# ─── Kafka Producer ───────────────────────────────────────────────────────────
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

# ─── Summarizer Setup ─────────────────────────────────────────────────────────
device = 0 if torch.cuda.is_available() else -1
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=device)

# ─── Summarize Texts in Batch ─────────────────────────────────────────────────
async def summarize_batch(texts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: [
        summarizer(t[:2000], max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        for t in texts
    ])

# ─── Extract Article Details ──────────────────────────────────────────────────
async def extract_article_data(context, url, retries=3):
    for attempt in range(retries):
        page = await context.new_page()
        try:
            await page.goto(url, timeout=15000)
            await page.wait_for_timeout(1000)

            content_div = await page.query_selector('div[data-testid="article-content-body"]')
            if not content_div:
                return None

            paragraphs = await content_div.query_selector_all("p")
            content = "\n".join([await p.inner_text() for p in paragraphs if await p.inner_text()])
            if not content.strip():
                return None

            title = await page.title()
            published = await page.query_selector("time")
            published_date = await published.get_attribute("datetime") if published else None
            author_el = await page.query_selector('[data-testid="article-author-list--name"]')
            author = await author_el.inner_text() if author_el else None
            if not author:
                meta_author = await page.query_selector('meta[name="author"]')
                author = await meta_author.get_attribute("content") if meta_author else None

            return {
                "source": "SportingNews",
                "title": title.strip(),
                "summary": None,
                "published_date": published_date,
                "author": author.strip() if author else None,
                "url": url,
                "content": content.strip(),
            }

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt == retries - 1:
                return None
        finally:
            await page.close()

# ─── Extract URLs from a Section Page ─────────────────────────────────────────
async def get_article_urls(page):
    await page.wait_for_timeout(1000)
    anchors = await page.query_selector_all("a.group")
    urls = []
    for a in anchors:
        href = await a.get_attribute("href")
        if href and not href.startswith("http"):
            href = BASE_URL + href
        if href and re.match(r"https:\/\/www\.sportingnews\.com\/.+\/news\/.+", href):
            urls.append(href.split("?")[0])
    return list(set(urls))

# ─── Collect Article URLs with Pagination ─────────────────────────────────────
async def collect_all_urls(context, section_url, max_urls):
    collected = set()
    page = await context.new_page()
    await page.goto(section_url, wait_until="domcontentloaded", timeout=30000)
    pages_visited = 0

    while len(collected) < max_urls and pages_visited < MAX_PAGES_PER_SECTION:
        new_urls = await get_article_urls(page)
        collected.update(new_urls)
        print(f"{section_url} → Page {pages_visited + 1}: Collected {len(collected)} URLs")

        next_btn = await page.query_selector("a:has-text('Older')")
        if not next_btn:
            break
        try:
            await next_btn.click()
            await page.wait_for_load_state("networkidle", timeout=10000)
            pages_visited += 1
        except Exception as e:
            print(f"Pagination error on {section_url}: {e}")
            break

    await page.close()
    return list(collected)[:max_urls]

# ─── Scrape Articles Concurrently ─────────────────────────────────────────────
async def process_articles(urls, context, max_concurrent):
    results = []

    async def worker(queue):
        while not queue.empty():
            url = await queue.get()
            data = await extract_article_data(context, url)
            if data and data["content"]:
                results.append(data)
            queue.task_done()

    queue = asyncio.Queue()
    for url in urls:
        await queue.put(url)

    tasks = [worker(queue) for _ in range(max_concurrent)]
    await asyncio.gather(*tasks)
    return results

# ─── Add Summaries to Articles ────────────────────────────────────────────────
async def add_summaries(articles):
    for i in range(0, len(articles), SUMMARY_BATCH_SIZE):
        batch = articles[i:i + SUMMARY_BATCH_SIZE]
        texts = [a["content"] for a in batch]
        summaries = await summarize_batch(texts)
        for j, summary in enumerate(summaries):
            batch[j]["summary"] = summary.strip()

# ─── Helper Functions for Refactoring ─────────────────────────────────────────
def load_existing_articles(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_all_section_urls(sections):
    return [f"{BASE_URL}/ca/{section}/news" for section in sections]

async def collect_urls_for_all_sections(context, section_urls, max_per_section):
    all_urls = set()
    for url in section_urls:
        urls = await collect_all_urls(context, url, max_per_section)
        all_urls.update(urls)
    return all_urls

async def process_new_articles(context, urls, existing_urls):
    new_urls = list(set(urls) - existing_urls)
    print(f"Found {len(urls)} URLs total, {len(new_urls)} are new")
    return await process_articles(new_urls, context, CONCURRENT_PAGES)

# ─── Main Function ────────────────────────────────────────────────────────────
async def main():
    existing_articles = load_existing_articles(OUTPUT_FILE)
    existing_urls = set(article["url"] for article in existing_articles)
    producer = create_producer()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        section_urls = get_all_section_urls(SECTIONS)
        all_urls = await collect_urls_for_all_sections(context, section_urls, MAX_ARTICLES // len(SECTIONS))
        new_articles = await process_new_articles(context, all_urls, existing_urls)

        print("Generating summaries...")
        await add_summaries(new_articles)

        for article in new_articles:
            send_to_kafka(producer, KAFKA_TOPIC, article)

        combined_articles = existing_articles + new_articles
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(combined_articles, f, ensure_ascii=False, indent=2)

        print(f"Done. Total saved articles: {len(combined_articles)}")
        await browser.close()

# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())
