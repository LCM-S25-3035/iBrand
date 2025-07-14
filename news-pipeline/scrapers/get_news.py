#!/usr/bin/env python
# coding: utf-8

import os
from dotenv import load_dotenv
from news_fetcher import fetch_news
from datetime import datetime, timedelta
from pymongo import MongoClient

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

# Mongo connection
client = MongoClient(mongo_uri)
db = client["iBrandDB"]
collection = db["articles_last_30_days"]

# Date range
QUERY = "news"
to_date = datetime.utcnow()
from_date = to_date - timedelta(days=30)

# Fetch news
df = fetch_news(API_KEY, QUERY, from_date, to_date)

# Save to MongoDB
records = df.to_dict(orient="records")
if records:
    collection.insert_many(records)
    print(f"✅ Inserted {len(records)} articles into MongoDB.")
else:
    print("⚠️ No articles found to insert.")

# Optional: still save to CSV
save_path = r"C:\Users\sarita\Downloads\newsapi_articles_last_month.csv"
df.to_csv(save_path, index=False)
print(f"✅ Done! {len(df)} articles saved to:\n{save_path}")
