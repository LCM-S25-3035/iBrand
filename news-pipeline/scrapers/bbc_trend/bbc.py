from playwright.sync_api import sync_playwright
from datetime import datetime
import uuid


def scrape_article_detail(page, article_url):
    page.goto(article_url, timeout=20000)
    page.wait_for_timeout(2000)

    # Extract title
    title = page.locator('[data-component="headline-block"] h1').inner_text()

    # Extract timestamp
    timestamp = page.locator('time[datetime]').first.get_attribute("datetime")

    # Extract author (if present)
    author_el = page.locator('div[data-testid="byline-new-contributors"] span')
    author = author_el.first.inner_text() if author_el.count() > 0 else "BBC News"

    # Extract image URL (if available)
    img_el = page.locator('div[data-testid="hero-image"] img')
    image_url = img_el.first.get_attribute("src") if img_el.count() > 0 else None

    # Extract article body text
    paragraphs = page.locator('div[data-component="text-block"] p')
    content = "\n".join([p.inner_text() for p in paragraphs.all()])

    # Extract tags
    tags = [tag.inner_text() for tag in page.locator('div[data-component="tags"] a').all()]

    return {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "author": author.strip(),
        "published_at": timestamp,
        "content": content.strip(),
        "tags": tags,
        "image_url": image_url,
        "url": article_url,
        "source": "BBC",
        "scraped_at": datetime.utcnow().isoformat()
    }


def scrape_bbc_full_articles():
    all_articles = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Step 1: Get article links
        page.goto("https://www.bbc.com/news", timeout=15000)
        page.wait_for_timeout(3000)

        cards = page.locator('div[data-testid="cambridge-card"]').all()
        article_links = []

        for card in cards:
            try:
                url = card.locator('a[data-testid="internal-link"]').get_attribute("href")
                if url and url.startswith("/news/articles/"):
                    full_url = f"https://www.bbc.com{url}"
                    article_links.append(full_url)
            except Exception as e:
                print(f"Error extracting article link: {e}")

        # Remove duplicates
        article_links = list(dict.fromkeys(article_links))[:10]

        # Step 2: Scrape full content from each article
        for url in article_links:
            try:
                print(f"Scraping {url}")
                article_data = scrape_article_detail(page, url)
                all_articles.append(article_data)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue

        browser.close()

    return all_articles


if __name__ == "__main__":
    articles = scrape_bbc_full_articles()
    for art in articles:
        print("\n--- ARTICLE ---")
        for k, v in art.items():
            print(f"{k}: {v}")
