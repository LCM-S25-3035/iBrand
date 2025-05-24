import requests
import json
import os
import time
from urllib.parse import urlparse
from newspaper import Article

# === CONFIGURATION ===
API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"
NEWS_FILE = "all_news.json"

COUNTRIES = ["us", "gb", "in", "ca"]
CATEGORIES = ["technology", "business", "sports", "health"]

EXCLUDED_DOMAINS = [
    "npr.org", "aljazeera.com", "bbc.com", "bbc.co.uk",
    "reuters.com", "techcrunch.com", "theguardian.com"
]

# === HELPERS ===
def load_existing_news(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_news(path, data):
    with open(path, "w", encoding="utf-8") as f:
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

def fetch_articles(country, category):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": 100,
        "page": 1
    }
    response = requests.get(NEWSAPI_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print(f"❌ Error fetching {category} ({country}): {response.status_code}")
        return []

# === MAIN ===
def main():
    existing_articles = load_existing_news(NEWS_FILE)
    existing_urls = {a["url"] for a in existing_articles}
    new_articles = []

    for country in COUNTRIES:
        for category in CATEGORIES:
            print(f"🌍 Fetching {category} news from {country}")
            articles = fetch_articles(country, category)
            print(f"✅ Got {len(articles)} articles")

            for a in articles:
                url = a.get("url")
                domain = get_domain(url)

                if not url or url in existing_urls or domain in EXCLUDED_DOMAINS:
                    continue

                full_content = extract_full_text(url)
                if not full_content:
                    continue

                new_articles.append({
                    "source": a.get("source", {}).get("name"),
                    "title": a.get("title"),
                    "summary": a.get("description"),
                    "published_date": a.get("publishedAt"),
                    "author": a.get("author"),
                    "url": url,
                    "content": full_content
                })

                existing_urls.add(url)
                time.sleep(1)  # prevent IP blocks

    print(f"\n🧠 Total new articles fetched: {len(new_articles)}")
    all_articles = existing_articles + new_articles
    save_news(NEWS_FILE, all_articles)
    print(f"💾 Saved {len(all_articles)} total unique articles to '{NEWS_FILE}'.")

if __name__ == "__main__":
    main()
