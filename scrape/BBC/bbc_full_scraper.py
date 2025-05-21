import requests
from bs4 import BeautifulSoup
import time, random, json
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

OUTPUT_FILE = "bbc_all_articles.json"

SECTION_LINKS = [
    # NEWS
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

    # SPORTS
    "https://www.bbc.com/sport",
    "https://www.bbc.com/sport/football",
    "https://www.bbc.com/sport/cricket",
    "https://www.bbc.com/sport/formula1",
    "https://www.bbc.com/sport/rugby-union",
    "https://www.bbc.com/sport/tennis",
    "https://www.bbc.com/sport/golf",
    "https://www.bbc.com/sport/athletics",
    "https://www.bbc.com/sport/cycling",

    # BUSINESS
    "https://www.bbc.com/business/executive-lounge",
    "https://www.bbc.com/business/technology-of-business",
    "https://www.bbc.com/business/future-of-business",

    # INNOVATION
    "https://www.bbc.com/innovation/technology",
    "https://www.bbc.com/innovation/science",
    "https://www.bbc.com/innovation/artificial-intelligence",
    "https://www.bbc.com/innovation/ai-v-the-mind",

    # CULTURE
    "https://www.bbc.com/culture/film-tv",
    "https://www.bbc.com/culture/music",
    "https://www.bbc.com/culture/art",
    "https://www.bbc.com/culture/style",
    "https://www.bbc.com/culture/books",
    "https://www.bbc.com/culture/entertainment-news",

    # ARTS
    "https://www.bbc.com/arts/arts-in-motion",

    # TRAVEL
    "https://www.bbc.com/travel/destinations",
    "https://www.bbc.com/travel/worlds-table",
    "https://www.bbc.com/travel/cultural-experiences",
    "https://www.bbc.com/travel/adventures",

    # EARTH
    "https://www.bbc.com/future-planet/natural-wonders",
    "https://www.bbc.com/future-planet/weather-science",
    "https://www.bbc.com/future-planet/solutions",
    "https://www.bbc.com/future-planet/sustainable-business",
    "https://www.bbc.com/future-planet/green-living"
]

def get_article_links(section_url, pages=3):
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
            print(f"❌ Error accessing {url}: {e}")
    return list(all_links)

def extract_article(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else None
        time_tag = soup.find('time')
        published_date = time_tag.get('datetime') if time_tag else None
        body = soup.find('article') or soup.find('main')
        paragraphs = body.find_all('p') if body else []
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        summary = content[:200] if content else None
        author_tag = soup.select_one('.byline__name')
        author = author_tag.get_text(strip=True) if author_tag else None
        return {
            "source": "BBC",
            "title": title,
            "summary": summary,
            "published_date": published_date,
            "author": author,
            "url": url,
            "content": content
        }
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

def scrape_bbc_all():
    all_articles = []
    for section in SECTION_LINKS:
        print(f"🔍 Crawling section: {section}")
        links = get_article_links(section, pages=5)
        for link in links:
            article = extract_article(link)
            if article:
                all_articles.append(article)
            time.sleep(random.uniform(1.5, 2.5))
    return all_articles

def save_to_json(data):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    articles = scrape_bbc_all()
    save_to_json(articles)
    print(f"✅ Done! Scraped {len(articles)} articles.")