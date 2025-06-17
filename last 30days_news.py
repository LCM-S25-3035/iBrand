#!/usr/bin/env python
# coding: utf-8

# In[1]:

import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('NEWSAPI_API_KEY')  # Read API key from .env

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
    today = datetime.utcnow()
    one_month_ago = today - timedelta(days=30)
    from_date = one_month_ago.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')

    queries = ['technology', 'business', 'health', 'sports']
    max_pages_per_query = 10  # 10 pages * 100 articles = 1000 per query max
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

    # Extract and normalize fields for up to 3000 articles
    data = []
    for art in all_articles[:3000]:
        data.append({
            'url': art.get('url'),
            'source': art.get('source', {}).get('name'),
            'title': art.get('title'),
            'author': art.get('author'),
            'published_at': art.get('publishedAt'),
            'summary': art.get('description'),
            'content': art.get('content'),
        })

    df = pd.DataFrame(data)
    df.to_csv(r'C:\Users\sarita\Downloads\newsapi_last_month_3000.csv', index=False)
    print("Saved 3000 articles to C:\\Users\\sarita\\Downloads\\newsapi_last_month_3000.csv")

if __name__ == "__main__":
    main()
