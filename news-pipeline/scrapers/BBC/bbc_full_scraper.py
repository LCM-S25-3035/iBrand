import requests
from bs4 import BeautifulSoup
import time, random, json, os
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

OUTPUT_FILE = "scrape/BBC/bbc_all_articles.json"

SECTION_LINKS = [
    "https://www.bbc.com/news/topics/c2vdnvdg6xxt",
    "https://www.bbc.com/news/war-in-ukraine",
    "https://www.bbc.com/news/us-canada",
    "https://www.bbc.com/news/uk",
    "https://www.bbc.com/news/world/africa",
    "https://www.bbc.com/news/world/asia",
    "https://www.bbc.com/news/world/australia",
    "https://www.bbc.com/news/world/europe",
    "https://www.bbc.com/news/world/latin_america",
    "https://www.bbc.com/news/world/middle_east",
    "https://www.bbc.com/news/in_pictures",
    "https://www.bbc.com/news/bbcverify",
    "https://www.bbc.com/sport",
    "https://www.bbc.com/sport/football",
    "https://www.bbc.com/sport/cricket",
    "https://www.bbc.com/sport/formula1",
    "https://www.bbc.com/sport/rugby-union",
    "https://www.bbc.com/sport/tennis",
    "https://www.bbc.com/sport/golf",
    "https://www.bbc.com/sport/athletics",
    "https://www.bbc.com/sport/cycling",
    "https://www.bbc.com/business/executive-lounge",
    "https://www.bbc.com/business/technology-of-business",
    "https://www.bbc.com/business/future-of-business",
    "https://www.bbc.com/innovation/technology",
    "https://www.bbc.com/innovation/science",
    "https://www.bbc.com/innovation/artificial-intelligence",
    "https://www.bbc.com/innovation/ai-v-the-mind",
    "https://www.bbc.com/culture/film-tv",
    "https://www.bbc.com/culture/music",
    "https://www.bbc.com/culture/art",
    "https://www.bbc.com/culture/style",
    "https://www.bbc.com/culture/books",
    "https://www.bbc.com/culture/entertainment-news",
    "https://www.bbc.com/arts/arts-in-motion",
    "https://www.bbc.com/travel/destinations",
    "https://www.bbc.com/travel/worlds-table",
    "https://www.bbc.com/travel/cultural-experiences",
    "https://www.bbc.com/travel/adventures",
    "https://www.bbc.com/future-planet/natural-wonders",
    "https://www.bbc.com/future-planet/weather-science",
    "https://www.bbc.com/future-planet/solutions",
    "https://www.bbc.com/future-planet/sustainable-business",
    "https://www.bbc.com/future-planet/green-living"
]

def get_article_links(section_url, pages=25):
    all_links = set()
    for page in range(1, pages + 1):
        url = section_url if page == 1 else f"{section_url}?page={page}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith("/news") or href.startswith("/sport"):
                    full_url = urljoin("https://www.bbc.com", href)
                    all_links.add(full_url)
        except Exception as e:
            print(f"Error accessing {url}: {e}")
    return list(all_links)

def extract_article(url):
    try:
        res = fetch_html(url)
        if not res:
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        print(f"Debugging author for: {url}")

        return {
            "source": "BBC",
            "title": extract_title(soup),
            "summary": extract_summary(soup),
            "published_date": extract_date(soup),
            "author": extract_author(soup, url),
            "url": url,
            "content": extract_content(soup)
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def fetch_html(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=10)
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return None

def extract_title(soup):
    return soup.find('h1').get_text(strip=True) if soup.find('h1') else None

def extract_date(soup):
    time_tag = soup.find('time')
    return time_tag.get('datetime') if time_tag else None

def extract_content(soup):
    body = soup.find('article') or soup.find('main')
    paragraphs = body.find_all('p') if body else []
    return "\n".join(p.get_text(strip=True) for p in paragraphs)

def extract_summary(soup):
    content = extract_content(soup)
    return content[:200] if content else None

def extract_author(soup, url):
    meta_author = soup.find("meta", {"name": "byl"})
    if meta_author and meta_author.get("content"):
        author = meta_author["content"].replace("By", "").strip()
        print(f"[meta] Author: {author}")
        return author

    possible_selectors = [
        '.byline__name', '[rel="author"]',
        'span.ssrcss-1pjc44v-Contributor',
        'span.sc-801dd632-7.lasLGY'
    ]
    for selector in possible_selectors:
        tag = soup.select_one(selector)
        if tag and tag.get_text(strip=True):
            author = tag.get_text(strip=True)
            print(f"[selector: {selector}] Author: {author}")
            return author

    for tag in soup.find_all(['span', 'div', 'p']):
        text = tag.get_text(strip=True)
        if "By " in text or (text and text.istitle() and len(text.split()) <= 3):
            print(f"Possible author span: {text}")
            return text

    print(f"Author missing for: {url}")
    return None

def load_existing_data():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def scrape_bbc_all():
    existing_articles = load_existing_data()
    existing_urls = set(article['url'] for article in existing_articles if 'url' in article)
    all_articles = existing_articles.copy()

    for section in SECTION_LINKS:
        print(f"Crawling section: {section}")
        links = get_article_links(section, pages=25)
        for link in links:
            if link in existing_urls:
                continue
            article = extract_article(link)
            if article:
                all_articles.append(article)
                existing_urls.add(link)
            time.sleep(random.uniform(1.5, 3.5))
    return all_articles

def save_to_json(data):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    articles = scrape_bbc_all()
    save_to_json(articles)
    print(f"Done! Scraped {len(articles)} total articles (including previous ones).")
