from pymongo import MongoClient
from transformers import pipeline
from keybert import KeyBERT
from datetime import datetime
import logging
from dotenv import load_dotenv
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

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
bias_classifier = pipeline("zero-shot-classification", model="./models/facebook-bart-large-mnli")
logging.info("Models loaded.")

LABEL_MAP = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "POSITIVE"
}

def get_sentiment(text):
    result = sentiment_pipeline(text[:512])[0]
    label = LABEL_MAP.get(result["label"], result["label"])  # maps LABEL_1 → POSITIVE
    score = round(result["score"], 4)
    if 0.48 <= score <= 0.52:
        label = "NEUTRAL"
    return {
        "label": label,
        "score": score
    }

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

def enrich_articles():
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

    articles = list(collection.find(query))

    if not articles:
        logging.info("No articles found to enrich. Exiting.")
        return

    logging.info(f"Found {len(articles)} articles to enrich.")

    for article in articles:
        content = article.get("content", "")
        if not content.strip():
            logging.warning(f"Skipping article with no content: {article.get('_id')}")
            continue

        try:
            sentiment = get_sentiment(content)
            tags = extract_tags(content)
            bias = detect_bias(content)

            collection.update_one(
                {"_id": article["_id"]},
                {"$set": {
                    "sentiment": sentiment,
                    "tags": tags,
                    "bias": bias,
                    "enriched_at": datetime.utcnow()
                }}
            )
            logging.info(f"Enriched article: {article['_id']}")

        except Exception as e:
            logging.error(f"Error enriching article {article.get('_id')}: {str(e)}")

if __name__ == "__main__":
    enrich_articles()
