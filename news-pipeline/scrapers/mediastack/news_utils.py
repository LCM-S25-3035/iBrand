# news_utils.py

import time
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from playwright.sync_api import sync_playwright

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
BASE_URL = 'http://api.mediastack.com/v1/news'

EXCLUDED_SOURCES = [
    "9to5mac", "appleinsider", "ars technica", "bbc news", "bloomberg", "business insider", "cnet", "cnn",
    "engadget", "espn", "eurogamer", "financial post", "forbes", "fox news", "gamesradar", "gizmodo",
    "gsm arena", "ign", "marketwatch", "mashable", "nbc news", "npr", "polygon", "san francisco chronicle",
    "techcrunch", "techradar", "the verge", "tom’s hardware", "venturebeat", "wired", "yahoo finance",
    "npr.org", "aljazeera.com", "bbc.co.uk", "bbc.com", "reuters.com", "theguardian.com"
]

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
