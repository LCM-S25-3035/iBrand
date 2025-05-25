import feedparser
import json
import os
import time

def scrape_feeds():
    # Path to previous JSON file (optional external backup or record)
    previous_json_path = r"C:\Users\raman\Desktop\AlJazeera\aljazeera_all_categories_news.json"

    # ✅ Output directory and file path inside 'scrape/Al Jazeera/output'
    output_dir = os.path.join("scrape", "Al Jazeera", "output")
    output_file = os.path.join(output_dir, "news_data.json")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Load previous data
    if os.path.exists(previous_json_path):
        with open(previous_json_path, "r", encoding="utf-8") as f:
            all_news = json.load(f)
        print(f"✅ Loaded {len(all_news)} articles from previous JSON.")
    else:
        print("⚠️ Previous JSON file not found. Starting fresh.")
        all_news = []

    # Create a set of existing article links to prevent duplicates
    existing_links = set(item['link'] for item in all_news)

    # Step 2: Define Al Jazeera RSS feeds by category
    rss_feeds = {
        "Africa": "https://www.aljazeera.com/xml/rss/all.xml?category=africa",
        "Asia": "https://www.aljazeera.com/xml/rss/all.xml?category=asia",
        "Middle East": "https://www.aljazeera.com/xml/rss/all.xml?category=middle-east",
        "Europe": "https://www.aljazeera.com/xml/rss/all.xml?category=europe",
        "US & Canada": "https://www.aljazeera.com/xml/rss/all.xml?category=us-canada",
        "Latin America": "https://www.aljazeera.com/xml/rss/all.xml?category=latin-america",
        "Economy": "https://www.aljazeera.com/xml/rss/all.xml?category=economy",
        "Opinion": "https://www.aljazeera.com/xml/rss/all.xml?category=opinion",
        "Features": "https://www.aljazeera.com/xml/rss/all.xml?category=features",
        "In Pictures": "https://www.aljazeera.com/xml/rss/all.xml?category=in-pictures",
        "Video": "https://www.aljazeera.com/xml/rss/all.xml?category=video",
        "Coronavirus Pandemic": "https://www.aljazeera.com/xml/rss/all.xml?category=coronavirus-pandemic",
        "Investigations": "https://www.aljazeera.com/xml/rss/all.xml?category=investigations"
    }

    # Step 3: Fetch and add new articles
    new_count = 0
    for category, url in rss_feeds.items():
        print(f"🔍 Fetching: {category}")
        feed = feedparser.parse(url)

        for entry in feed.entries:
            if entry.link not in existing_links:
                news_item = {
                    "category": category,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "N/A"),
                    "summary": entry.get("summary", "No summary available.")
                }
                all_news.append(news_item)
                existing_links.add(entry.link)
                new_count += 1

    # Step 4: Save updated data to new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)

    print(f"\n✅ {new_count} new articles added.")
    print(f"📦 Total articles stored: {len(all_news)}")
    print(f"📁 Output saved to: {output_file}")
    print("-" * 50)

# ============================
# 🔁 Run Continuously
# ============================
if __name__ == "__main__":
    while True:
        try:
            print("\n⏱️ Starting Al Jazeera RSS scrape cycle...\n")
            scrape_feeds()
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        print("⏳ Waiting 2 minutes before next run...\n")
        time.sleep(120)  # Wait 1800 seconds (30 minutes)

