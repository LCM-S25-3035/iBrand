import requests
import json
import os
import time

# === Configuration ===
API_KEY = "XXXXXXXXXXXXXXXX"  
NEWS_FILE = "filtered_mediastack_articles.json"
MEDIASTACK_URL = "http://api.mediastack.com/v1/news"
PAGE_SIZE = 100  # Max allowed per request
MAX_PAGES = 9   

# Sources to EXCLUDE (lowercase for case-insensitive match)
EXCLUDED_SOURCES = [
    "9to5mac", "appleinsider", "ars technica", "bbc news", "bloomberg", "business insider", "cnet", "cnn",
    "engadget", "espn", "eurogamer", "financial post", "forbes", "fox news", "gamesradar", "gizmodo",
    "gsm arena", "ign", "marketwatch", "mashable", "nbc news", "npr", "polygon", "san francisco chronicle",
    "techcrunch", "techradar", "the verge", "tom’s hardware", "venturebeat", "wired", "yahoo finance",
    "npr.org", "aljazeera.com", "bbc.co.uk", "bbc.com", "reuters.com", "theguardian.com"
]

# === Functions ===

def fetch_mediastack_page(api_key, offset=0):
    params = {
        "access_key": api_key,
        "languages": "en",
        "limit": PAGE_SIZE,
        "offset": offset,
        "sort": "published_desc"
    }

    response = requests.get(MEDIASTACK_URL, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"❌ Error fetching data: {response.status_code}")
        return []

def load_existing_news(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_news(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def merge_articles(existing, new):
    existing_urls = {article['url'] for article in existing}
    merged = existing[:]
    for article in new:
        if article['url'] not in existing_urls:
            merged.append(article)
    return merged

def clean_source(source):
    if source:
        return source.strip().lower()
    return ""

def main():
    print("🔍 Fetching Mediastack news...")
    all_articles = []

    for page in range(MAX_PAGES):
        offset = page * PAGE_SIZE
        articles = fetch_mediastack_page(API_KEY, offset=offset)
        print(f"📄 Page {page+1}: {len(articles)} articles fetched")

        for a in articles:
            source_cleaned = clean_source(a.get("source"))
            if not any(excluded in source_cleaned for excluded in EXCLUDED_SOURCES):
                structured = {
                    "source": a.get("source"),
                    "title": a.get("title"),
                    "summary": a.get("description"),
                    "published_date": a.get("published_at"),
                    "url": a.get("url"),
                    "author": a.get("author"),
                    "content": a.get("content"),
                    "origin": "mediastack"
                }
                all_articles.append(structured)

        time.sleep(1)

    print(f"\n🧠 Total filtered articles: {len(all_articles)}")

    existing_articles = load_existing_news(NEWS_FILE)
    updated_articles = merge_articles(existing_articles, all_articles)
    save_news(NEWS_FILE, updated_articles)

    print(f"💾 Saved {len(updated_articles)} unique articles to '{NEWS_FILE}'.")

if __name__ == "__main__":
    main()
