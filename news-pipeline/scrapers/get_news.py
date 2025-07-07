#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
from dotenv import load_dotenv
from news_fetcher import fetch_news
from datetime import datetime, timedelta

load_dotenv()  # loads .env file in the same directory

API_KEY = os.getenv("NEWS_API_KEY")  # get key from environment variable

QUERY = "news"
to_date = datetime.utcnow()
from_date = to_date - timedelta(days=30)

df = fetch_news(API_KEY, QUERY, from_date, to_date)
save_path = r"C:\Users\sarita\Downloads\newsapi_articles_last_month.csv"
df.to_csv(save_path, index=False)

print(f"✅ Done! {len(df)} articles saved to:\n{save_path}")
