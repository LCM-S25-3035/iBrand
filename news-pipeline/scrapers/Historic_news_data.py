#!/usr/bin/env python
# coding: utf-8

import os
from dotenv import load_dotenv
from news_fetcher import fetch_news
from datetime import datetime, timedelta
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Get API key and MongoDB URI from .env
API_KEY = os.getenv("HISTORIC_NEWS_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(mongo_uri)
db = client["iBrandDB"]
collection = db["historic_articles"]

# Define date range
QUERY = "news"
to_date = datetime.utcnow()
from_date = to_date - timedelta(days=30)

# Fetch and save articles
df = fetch_news(API_KEY, QUERY, from_date, to_date)
save_path = r"C:\Users\sarita\Downloads\historic_newsapi_articles_last_month.csv"
df.to_csv(save_path, index=False)
print(f"✅ Saved CSV with {len(df)} articles to:\n{save_path}")

# Insert into MongoDB
records = df.to_dict(orient="records")
if records:
    collection.insert_many(records)
    print(f"✅ Inserted {len(records)} records into MongoDB 'historic_articles'")
else:
    print("⚠️ No articles to insert into MongoDB")




