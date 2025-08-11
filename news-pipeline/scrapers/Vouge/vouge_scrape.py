import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

OUTPUT_FILE = "vogue_fashion_full.json"
RESET_FLAG_FILE = ".vogue_scrape_reset_done"
MAX_PAGES = 50

async def scrape_vogue():
    articles = []
    seen_urls = set()
    current_page = 1

    # ✅ ONE-TIME RESET: only delete output if marker file doesn't exist
    if not os.path.exists(RESET_FLAG_FILE):
        print("🔁 First run: Resetting JSON and creating marker...")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        with open(RESET_FLAG_FILE, "w") as f:
            f.write("reset done")
        existing_articles = []
    else:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_articles = json.load(f)

    seen_urls = {a["url"] for a in existing_articles}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.vogue.com", timeout=60000)

        while current_page <= MAX_PAGES:
            await page.wait_for_timeout(2000)
            print(f"\n--- Scraping Page {current_page} ---")

            article_cards = await page.query_selector_all('a[data-recirc-pattern="summary-item"]')
            print(f"Found {len(article_cards)} articles on page {current_page}")

            new_on_page = 0

            for card in article_cards:
                article_page = None
                try:
                    url = await card.get_attribute("href")
                    if not url or not url.startswith("/article"):
                        continue
                    full_url = f"https://www.vogue.com{url}"

                    if full_url in seen_urls:
                        continue  # skip duplicates
                    seen_urls.add(full_url)

                    title_el = await card.query_selector(".summary-item__hed")
                    title = await title_el.inner_text() if title_el else ""

                    summary_el = await card.query_selector("p")
                    summary = await summary_el.inner_text() if summary_el else ""

                    article_page = await context.new_page()
                    await article_page.goto(full_url, timeout=30000)

                    title_el = await article_page.query_selector('h1[data-testid="ContentHeaderHed"]')
                    title = await title_el.inner_text() if title_el else title

                    author_el = await article_page.query_selector('a.byline__name-link')
                    author = await author_el.inner_text() if author_el else "Vogue"

                    date_el = await article_page.query_selector("time")
                    date_val = await date_el.get_attribute("datetime") if date_el else None
                    published_at = (
                        datetime.fromisoformat(date_val.replace("Z", "+00:00")).isoformat()
                        if date_val else datetime.utcnow().isoformat() + "Z"
                    )

                    content_tags = await article_page.query_selector_all("article p")
                    content = "\n".join([await p.inner_text() for p in content_tags if await p.inner_text() != ""])

                    articles.append({
                        "url": full_url,
                        "source": "Vogue",
                        "title": title.strip(),
                        "author": author.strip(),
                        "published_at": published_at,
                        "summary": summary.strip(),
                        "content": content.strip()
                    })

                    new_on_page += 1
                    print(f"✅ Scraped: {title.strip()}")

                except Exception as e:
                    print(f"⚠️ Error scraping article: {e}")
                finally:
                    if article_page:
                        await article_page.close()

            if new_on_page == 0:
                print("🛑 No new articles found on this page. Stopping.")
                break

            try:
                next_button = await page.locator('span.button__label', has_text="Next Page").element_handle()
                if next_button:
                    await next_button.click()
                    current_page += 1
                    await page.wait_for_timeout(3000)
                else:
                    print("🚫 'Next Page' button not found. Ending.")
                    break
            except Exception as e:
                print(f"⚠️ Pagination failed: {e}")
                break

        await browser.close()
        save_articles(existing_articles, articles)

def save_articles(existing_articles, new_articles):
    final = existing_articles + new_articles
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=4)
    print(f"\n💾 Saved {len(final)} total articles ({len(new_articles)} new)")

if __name__ == "__main__":
    asyncio.run(scrape_vogue())
