import requests
import json
from kafka import KafkaProducer
from time import sleep

# === CONFIGURATION ===
NEWSAPI_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GNEWS_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
KAFKA_TOPIC = "news-stream"
KAFKA_BROKER = "localhost:9092"

CATEGORIES = ["technology", "business", "sports", "health"]
COUNTRIES = ["us"]
MAX_ARTICLES = 50  # per category

sent_urls = set()

# === KAFKA PRODUCER ===
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# === UTILS ===
def send_to_kafka(article):
    if article["url"] in sent_urls:
        return
    sent_urls.add(article["url"])
    producer.send(KAFKA_TOPIC, value=article)
    print(f"✅ Sent: {article['title'][:60]}")

# === FETCH FROM NEWSAPI ===
def fetch_newsapi(category, country):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWSAPI_KEY,
        "category": category,
        "country": country,
        "pageSize": MAX_ARTICLES,
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        for article in data.get("articles", []):
            payload = {
                "title": article.get("title"),
                "url": article.get("url"),
                "source": article.get("source", {}).get("name"),
                "author": article.get("author"),
                "published_date": article.get("publishedAt"),
                "summary": article.get("description"),
                "content": article.get("content")
            }
            send_to_kafka(payload)
            sleep(0.1)
    except Exception as e:
        print(f"❌ NewsAPI Error for {category}: {e}")

# === FETCH FROM GNEWS ===
def fetch_gnews(keyword):
    for page in range(1, 4):
        url = f"https://gnews.io/api/v4/search?q={keyword}&lang=en&max=10&page={page}&apikey={GNEWS_API_KEY}"
        try:
            response = requests.get(url)
            data = response.json()
            for article in data.get("articles", []):
                payload = {
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "source": article.get("source", {}).get("name"),
                    "author": None,
                    "published_date": article.get("publishedAt"),
                    "summary": article.get("description"),
                    "content": article.get("content") or article.get("description")
                }
                send_to_kafka(payload)
                sleep(0.1)
        except Exception as e:
            print(f"❌ GNews Error (page {page}): {e}")

# === MAIN ===
if __name__ == "__main__":
    for country in COUNTRIES:
        for category in CATEGORIES:
            print(f"🌍 Fetching {category} news from NewsAPI ({country})...")
            fetch_newsapi(category, country)

    keywords = ["technology", "business", "sports", "health", "science", "startup"]
    for kw in keywords:
        print(f"🔍 Fetching GNews for keyword: {kw}")
        fetch_gnews(kw)

    producer.flush()
    print("🧠 Done streaming news from NewsAPI & GNews.")
