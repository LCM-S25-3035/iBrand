import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json
import os

CATEGORIES = [
    "world", "business", "legal", "markets", "breakingviews",
    "technology", "investigates", "lifestyle", "sports"
]

BASE_URL = "https://www.reuters.com"

async def scrape_category(context, category):
    url = f"{BASE_URL}/{category}/"
    page = await context.new_page()
    await page.goto(url, timeout=60000, wait_until='networkidle')

    # Accept cookies
    try:
        await page.click("button:has-text('Accept All')", timeout=5000)
    except:
        pass

    # Scroll to load content
    for _ in range(5):
        await page.mouse.wheel(0, 1500)
        await asyncio.sleep(2)

    # Screenshot for debugging (optional)
    await page.screenshot(path=f"scrape/Reuters/output/{category}_page.png")

    links = await page.query_selector_all("a[data-testid='Heading']")
    articles = []

    for link in links[:10]:
        try:
            title = await link.inner_text()
            href = await link.get_attribute("href")
            if href and not href.startswith("http"):
                href = BASE_URL + href

            # Visit full article
            new_page = await context.new_page()
            await new_page.goto(href, timeout=60000, wait_until='networkidle')

            # Wait for article body
            await new_page.wait_for_selector("div[data-testid='BodyWrapper'] p", timeout=10000)

            # Extract article content
            paras = await new_page.query_selector_all("div[data-testid='BodyWrapper'] p")
            body = "\n".join([await p.inner_text() for p in paras]) if paras else ""

            articles.append({
                "category": category,
                "title": title.strip(),
                "url": href,
                "scraped_at": datetime.utcnow().isoformat(),
                "content": body.strip()
            })

            await new_page.close()
        except Exception as e:
            print(f"❌ Error in article from {category}: {e}")

    await page.close()
    return articles

async def scrape_reuters():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Set to False for debugging
            slow_mo=50       # Slow down interaction to mimic real user
        )
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ))

        all_articles = []

        os.makedirs("output", exist_ok=True)

        for cat in CATEGORIES:
            print(f"🔍 Scraping category: {cat}")
            try:
                articles = await scrape_category(context, cat)
                print(f"✅ {len(articles)} articles scraped from {cat}")
                all_articles.extend(articles)
            except Exception as e:
                print(f"❌ Failed scraping {cat}: {e}")

        await browser.close()

        # Save as JSON
        with open("scrape/Reuters/output/reuters_articles.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=4)

        print(f"\n✅ Done! Scraped {len(all_articles)} articles across {len(CATEGORIES)} categories.")

# Run the script
asyncio.run(scrape_reuters())
