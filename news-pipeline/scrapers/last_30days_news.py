#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables
load_dotenv()

API_KEY = os.getenv('NEWSAPI_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')

def fetch_newsapi_articles(page=1, page_size=100, from_date=None, to_date=None, query='news'):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': API_KEY,
        'pageSize': page_size,
        'page': page,
        'from': from_date,
        'to': to_date,
        'language': 'en',
        'q': query,
        'sortBy': 'publishedAt'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code != 200 or 'articles' not in data:
        print(f"Error fetching page {page} for query '{query}': {data.get('message', 'Unknown error')}")
        return []
    return data['articles']

def main():
    # Set up MongoDB connection
    client = MongoClient(MONGO_URI)
    db = client["iBrandDB"]
    collection = db["news_articles"]

    today = datetime.utcnow()
    one_month_ago = today - timedelta(days=30)
    from_date = one_month_ago.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    queries = ['technology', 'business', 'health', 'sports']
    max_pages_per_query = 10
    all_articles = []

    for q in queries:
        print(f"Starting query '{q}'")
        for page in range(1, max_pages_per_query + 1):
            print(f"Fetching page {page} for query '{q}'")
            articles = fetch_newsapi_articles(page=page, page_size=100, from_date=from_date, to_date=to_date, query=q)
            if not articles:
                print(f"No more articles for query '{q}' at page {page}")
                break
            all_articles.extend(articles)
            if len(all_articles) >= 3000:
                print("Reached 3000 articles, stopping.")
                break
        if len(all_articles) >= 3000:
            break

    # Normalize and insert into MongoDB
    inserted_count = 0
    for art in all_articles[:3000]:
        doc = {
            'url': art.get('url'),
            'source': art.get('source', {}).get('name'),
            'title': art.get('title'),
            'author': art.get('author'),
            'published_at': art.get('publishedAt'),
            'summary': art.get('description'),
            'content': art.get('content'),
        }
        collection.insert_one(doc)
        inserted_count += 1

    print(f"✅ Inserted {inserted_count} articles into MongoDB collection 'news_articles'.")

if __name__ == "__main__":
    main()
