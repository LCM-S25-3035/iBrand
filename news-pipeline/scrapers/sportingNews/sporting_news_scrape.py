import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright
from transformers import pipeline
import torch

# ─── Constants ────────────────────────────────────────────────────────────────
BASE_URL = "https://www.sportingnews.com"
SECTIONS = [
    "nfl", "nba", "mlb", "nhl", "mma", "nascar", "golf", "boxing", "tennis", "wwe", "ncaa-football", "ncaa-basketball"
]
MAX_ARTICLES = 10000
CONCURRENT_PAGES = 10
SUMMARY_BATCH_SIZE = 8
MAX_PAGES_PER_SECTION = 50
OUTPUT_FILE = "sportingnews_all_categories_articles.json"

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
            if author_el:
                author = await author_el.inner_text()
            else:
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

# ─── Extract URLs from a Section Page ────────────────────────────────────────
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

# ─── Main Function ────────────────────────────────────────────────────────────
import os

# ─── Main Function ────────────────────────────────────────────────────────────
async def main():
    # Load existing data if present
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_articles = json.load(f)
    else:
        existing_articles = []

    existing_urls = set(article["url"] for article in existing_articles)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        all_urls = set()
        for section in SECTIONS:
            section_url = f"{BASE_URL}/ca/{section}/news"
            urls = await collect_all_urls(context, section_url, MAX_ARTICLES // len(SECTIONS))
            all_urls.update(urls)

        # Remove already processed URLs
        new_urls = list(set(all_urls) - existing_urls)
        print(f"Found {len(all_urls)} URLs total, {len(new_urls)} are new")

        # Process only new URLs
        new_articles = await process_articles(new_urls, context, CONCURRENT_PAGES)

        print("Generating summaries...")
        await add_summaries(new_articles)

        combined_articles = existing_articles + new_articles

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(combined_articles, f, ensure_ascii=False, indent=2)

        print(f"Done. Total saved articles: {len(combined_articles)}")
        await browser.close()


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main())
