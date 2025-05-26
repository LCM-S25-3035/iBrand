import requests
import json
import os
import time
from urllib.parse import urlparse
from newspaper import Article

# === Configuration ===
GNEWS_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
GNEWS_SEARCH_URL = "https://gnews.io/api/v4/search"
NEWS_FILE = "all_news.json"

TOPICS = [
    "technology", "sports", "finance", "elections",
    "ai", "education", "health", "startup", "climate"
]

EXCLUDED_DOMAINS = [
    "npr.org", "aljazeera.com", "bbc.com", "bbc.co.uk",
    "reuters.com", "techcrunch.com", "theguardian.com"
]

# === Utility Functions ===
def load_existing_news(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_news(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ""

def extract_full_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.strip()
    except:
        return None

def fetch_articles_for_topic(topic, pages=5):
    all_articles = []
    for page in range(1, pages + 1):
        params = {
            "q": topic,
            "lang": "en",
            "token": GNEWS_API_KEY,
            "max": 10,
            "page": page
        }
        response = requests.get(GNEWS_SEARCH_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            print(f"🔎 {topic} - Page {page}: {len(articles)} articles")
            all_articles.extend(articles)
        else:
            print(f"❌ Error fetching {topic} page {page}: {response.status_code}")
        time.sleep(1)
    return all_articles

# === Main Scraper ===
def main():
    existing_articles = load_existing_news(NEWS_FILE)
    existing_urls = {a["url"] for a in existing_articles}
    new_articles = []

    for topic in TOPICS:
        articles = fetch_articles_for_topic(topic, pages=10)

        for a in articles:
            url = a.get("url")
            domain = get_domain(url)

            if not url or url in existing_urls or domain in EXCLUDED_DOMAINS:
                continue

            full_content = extract_full_text(url)
            if not full_content:
                continue

            new_article = {
                "source": a.get("source", {}).get("name", "Unknown"),
                "title": a.get("title") or "No Title",
                "summary": a.get("description") or "No Summary",
                "published_date": a.get("publishedAt") or "Unknown",
                "author": a.get("author") or "Unknown",
                "url": url,
                "content": full_content
            }

            new_articles.append(new_article)
            existing_urls.add(url)
            time.sleep(1)  # polite pause to avoid being blocked

    print(f"\n🧠 Total new articles fetched: {len(new_articles)}")
    all_articles = existing_articles + new_articles
    save_news(NEWS_FILE, all_articles)
    print(f"💾 Saved {len(all_articles)} total unique articles to '{NEWS_FILE}'.")

if __name__ == "__main__":
    main()
