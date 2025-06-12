import os
import json
import time
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from playwright.sync_api import sync_playwright

# === 1. API Config ===
API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX' 
BASE_URL = 'http://api.mediastack.com/v1/news'

# === 2. Excluded sources ===
EXCLUDED_SOURCES = [
    "9to5mac", "appleinsider", "ars technica", "bbc news", "bloomberg", "business insider", "cnet", "cnn",
    "engadget", "espn", "eurogamer", "financial post", "forbes", "fox news", "gamesradar", "gizmodo",
    "gsm arena", "ign", "marketwatch", "mashable", "nbc news", "npr", "polygon", "san francisco chronicle",
    "techcrunch", "techradar", "the verge", "tom’s hardware", "venturebeat", "wired", "yahoo finance",
    "npr.org", "aljazeera.com", "bbc.co.uk", "bbc.com", "reuters.com", "theguardian.com"
]

# === 3. Fetch up to 500 articles using pagination ===
def fetch_articles(limit_per_page=100, max_articles=500):
    all_articles = []
    for offset in range(0, max_articles, limit_per_page):
        params = {
            'access_key': API_KEY,
            'languages': 'en',
            'limit': limit_per_page,
            'offset': offset
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            print(f"❌ Error fetching data: {response.status_code}")
            break

        data = response.json()
        batch = data.get('data', [])
        if not batch:
            break
        all_articles.extend(batch)
        print(f"📥 Fetched {len(batch)} articles (Offset: {offset})")
        time.sleep(1)
    return all_articles

# === 4. Fallback content extraction with Playwright ===
def fetch_with_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)
            html = page.content()
            browser.close()
            soup = BeautifulSoup(html, 'html.parser')
            paragraphs = soup.find_all('p')
            text = '\n'.join([p.get_text() for p in paragraphs])
            return text.strip()
    except Exception as e:
        print(f"❌ Playwright failed for {url[:50]}... Error: {e}")
        return ''

# === 5. First try newspaper3k, fallback to Playwright ===
def get_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        if len(article.text) > 200:
            return article.text
        raise ValueError("Article too short, fallback needed")
    except Exception as e:
        if isinstance(e, (SystemExit, KeyboardInterrupt)):
            raise
        print(f"⚠️ Newspaper3k failed for {url} — Error: {e}")
        print(f"🔁 Falling back to Playwright for {url}")
        return fetch_with_playwright(url)

# === 6. Main scraping and saving logic ===
def process_and_save():
    articles = fetch_articles()
    final_data = []

    for article in articles:
        url = article.get('url')
        source = article.get('source', '').lower()

        if not url or source in EXCLUDED_SOURCES:
            continue

        content = get_article_content(url)
        if not content or len(content) < 200:
            continue

        processed = {
            "source": article.get('source'),
            "title": article.get('title'),
            "summary": article.get('description'),
            "published_date": article.get('published_at'),
            "url": url,
            "author": article.get('author'),
            "content": content,
            "origin": "mediastack"
        }

        print(f"✅ Scraped: {processed['title'][:60]}... ({len(content)} chars)")
        final_data.append(processed)
        time.sleep(1)

    # === 7. Save: Append only NEW articles ===
    filename = "newFiltered_mediastack_articles.json"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_urls = {item['url'] for item in existing_data}
    new_articles = [item for item in final_data if item['url'] not in existing_urls]

    combined_data = existing_data + new_articles

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)

    print(f"\n💾 Appended {len(new_articles)} new articles to '{filename}' (Total: {len(combined_data)}).")

# === 8. Run Script ===
if __name__ == "__main__":
    process_and_save()
