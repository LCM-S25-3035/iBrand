from pymongo import MongoClient
from transformers import pipeline
from keybert import KeyBERT
from datetime import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import logging
import os
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s"
)

# MongoDB connection
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["articles-db"]
collection = db["articles"]

# Load models once
logging.info("Loading models...")
sentiment_pipeline = pipeline("sentiment-analysis", model="./models/distilbert-base-uncased")
kw_model = KeyBERT(model="./models/all-MiniLM-L6-v2")
bias_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
logging.info("Models loaded.")

# Thread-safe lock for MongoDB writes
mongo_lock = Lock()

LABEL_MAP = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "POSITIVE"
}

def get_sentiment(text):
    result = sentiment_pipeline(text[:512])[0]
    label = LABEL_MAP.get(result["label"], result["label"])
    score = round(result["score"], 4)
    if 0.48 <= score <= 0.52:
        label = "NEUTRAL"
    return {"label": label, "score": score}

def detect_bias(text):
    labels = ["left-leaning", "right-leaning", "neutral", "sensational", "factual"]
    result = bias_classifier(text[:512], labels)
    label = result["labels"][0]
    score = round(result["scores"][0], 4)
    if score < 0.4:
        label = "uncertain"
    return {"label": label, "score": score}

def extract_tags(text, top_n=5):
    keywords = kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 2),
        stop_words='english', top_n=top_n
    )
    seen = set()
    tags = []
    for kw, _ in keywords:
        clean_kw = kw.strip().lower()
        if clean_kw not in seen:
            seen.add(clean_kw)
            tags.append(clean_kw)
    return tags

def enrich_and_store(article):
    content = article.get("content", "")
    if not content.strip():
        logging.warning(f"Skipping article with no content: {article.get('_id')}")
        return

    try:
        sentiment = get_sentiment(content)
        tags = extract_tags(content)
        bias = detect_bias(content)

        enriched_data = {
            "sentiment": sentiment,
            "tags": tags,
            "bias": bias,
            "enriched_at": datetime.utcnow()
        }

        with mongo_lock:
            collection.update_one(
                {"_id": article["_id"]},
                {"$set": enriched_data}
            )
        logging.info(f"Enriched article: {article['_id']}")

    except Exception as e:
        logging.error(f"Error enriching article {article.get('_id')}: {str(e)}")

def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def enrich_articles_parallel(batch_size=100, max_workers=10):
    query = {
        "$or": [
            {"sentiment": {"$exists": False}},
            {"sentiment": None},
            {"tags": {"$exists": False}},
            {"tags": None},
            {"bias": {"$exists": False}},
            {"bias": None}
        ]
    }

    articles = list(collection.find(query).limit(1000))  # cap for testing speed

    if not articles:
        logging.info("No articles found to enrich. Exiting.")
        return

    logging.info(f"Total articles to enrich: {len(articles)}")
    
    for batch_num, batch in enumerate(chunked(articles, batch_size), start=1):
        logging.info(f"Starting batch {batch_num} with {len(batch)} articles...")

        start = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(enrich_and_store, article) for article in batch]
            for future in as_completed(futures):
                future.result()
        end = time.time()

        logging.info(f"Completed batch {batch_num} in {end - start:.2f} seconds.")

if __name__ == "__main__":
    # Test various batch sizes
    for size in [50, 100, 500]:
        logging.info(f"\n=== Running with batch size: {size} ===")
        enrich_articles_parallel(batch_size=size, max_workers=10)
