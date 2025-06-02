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

load_dotenv()  # Load from .env file

API_KEY = os.getenv("83653b40af184cd1ad6ae2394fd1026b")


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


# In[4]:


import requests
import pandas as pd
from datetime import datetime, timedelta
import time

API_KEY = '83653b40af184cd1ad6ae2394fd1026b'  # 🔑 Replace with your actual key
QUERY = 'news'  # 🔍 Can be changed to e.g., "finance", "climate", etc.
PAGE_SIZE = 100
MAX_PAGES_PER_DAY = 2
DAYS_PER_CHUNK = 1

# 🕒 Date range: 15 to 30 days ago
today = datetime.utcnow()
from_date = today - timedelta(days=30)
to_date = today - timedelta(days=15)

articles = []
date_pointer = from_date

print(f"Fetching news from {from_date.date()} to {to_date.date()}...")

while date_pointer < to_date:
    chunk_start = date_pointer
    chunk_end = min(chunk_start + timedelta(days=DAYS_PER_CHUNK), to_date)

    for page in range(1, MAX_PAGES_PER_DAY + 1):
        print(f"Getting {chunk_start.date()} to {chunk_end.date()}, page {page}")

        url = (
            f'https://newsapi.org/v2/everything?'
            f'q={QUERY}&'
            f'from={chunk_start.strftime("%Y-%m-%d")}&'
            f'to={chunk_end.strftime("%Y-%m-%d")}&'
            f'sortBy=publishedAt&'
            f'pageSize={PAGE_SIZE}&'
            f'page={page}&'
            f'apiKey={API_KEY}'
        )

        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            break

        data = response.json()
        if 'articles' not in data or not data['articles']:
            print("⚠️ No articles returned.")
            break

        for item in data['articles']:
            articles.append({
                'url': item.get('url'),
                'source': item['source'].get('name'),
                'title': item.get('title'),
                'author': item.get('author'),
                'published_at': item.get('publishedAt'),
                'summary': item.get('description'),
                'content': item.get('content')
            })

        time.sleep(1)

    date_pointer += timedelta(days=DAYS_PER_CHUNK)

# Save as CSV
df = pd.DataFrame(articles)
save_path = r"C:\Users\sarita\Downloads\news_15_to_30_days_ago.csv"
df.to_csv(save_path, index=False)

print(f"\n✅ Done! {len(df)} articles saved to:\n{save_path}")


# In[ ]:




