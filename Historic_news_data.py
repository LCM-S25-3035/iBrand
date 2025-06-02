#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# ✅ Replace this with your actual NewsAPI key (in quotes)
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("647fc54de17f444d818a907b032d8ced")

# Use API_KEY in your requests


# Constants
QUERY = 'news'  # You can change this to a specific topic like "technology", "finance", etc.
MAX_RESULTS = 3000
PAGE_SIZE = 100
NUM_PAGES = MAX_RESULTS // PAGE_SIZE

# Date range: last 30 days
to_date = datetime.utcnow()
from_date = to_date - timedelta(days=30)

# Collect results
articles = []

print("Fetching news articles...")

for page in range(1, NUM_PAGES + 1):
    print(f'Fetching page {page} of {NUM_PAGES}...')

    url = (
        f'https://newsapi.org/v2/everything?'
        f'q={QUERY}&'
        f'from={from_date.strftime("%Y-%m-%d")}&'
        f'to={to_date.strftime("%Y-%m-%d")}&'
        f'sortBy=publishedAt&'
        f'pageSize={PAGE_SIZE}&'
        f'page={page}&'
        f'apiKey={API_KEY}'
    )

    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Error on page {page}: {response.status_code}")
        print(response.text)
        break

    data = response.json()
    if 'articles' not in data or not data['articles']:
        print("⚠️ No more articles found.")
        break

    for item in data['articles']:
        articles.append({
            'url': item.get('url'),
            'source': item['source'].get('name') if item.get('source') else None,
            'title': item.get('title'),
            'author': item.get('author'),
            'published_at': item.get('publishedAt'),
            'summary': item.get('description'),
            'content': item.get('content')
        })

    time.sleep(1)  # Prevent hitting API limits

# Convert to DataFrame and save
df = pd.DataFrame(articles)
df = df.head(MAX_RESULTS)

# Save file
save_path = r"C:\Users\sarita\Downloads\newsapi_articles_last_month.csv"
df.to_csv(save_path, index=False)

print(f"\n✅ Done! {len(df)} articles saved to:\n{save_path}")


# In[ ]:




