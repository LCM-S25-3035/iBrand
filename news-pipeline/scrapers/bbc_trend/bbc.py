from datetime import datetime, timezone
import uuid
from playwright.sync_api import sync_playwright

def scrape_article_detail(page, article_url):
    page.goto(article_url, timeout=20000)
    page.wait_for_timeout(2000)

    title = page.locator('[data-component="headline-block"] h1').inner_text()
    timestamp = page.locator('time[datetime]').first.get_attribute("datetime")

    author_el = page.locator('div[data-testid="byline-new-contributors"] span')
    author = author_el.first.inner_text() if author_el.count() > 0 else "BBC News"

    img_el = page.locator('div[data-testid="hero-image"] img')
    image_url = img_el.first.get_attribute("src") if img_el.count() > 0 else None

    paragraphs = page.locator('div[data-component="text-block"] p')
    content = "\n".join([p.inner_text() for p in paragraphs.all()])

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
        "scraped_at": datetime.now(timezone.utc).isoformat()
    }
