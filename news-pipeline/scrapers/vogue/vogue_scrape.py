import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

def scrape_vogue_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        author_tag = soup.find("span", class_="byline__name")
        author = author_tag.get_text(strip=True).replace("By ", "") if author_tag else "Unknown"

        date_tag = soup.find("time")
        date_val = date_tag.get("datetime") if date_tag else None
        published_at = (
            datetime.fromisoformat(date_val.replace("Z", "+00:00")).isoformat()
            if date_val else datetime.now(timezone.utc).isoformat()
        )

        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

        return {
            "url": url,
            "source": "Vogue",
            "title": title,
            "author": author,
            "published_at": published_at,
            "summary": "",  # optional: fill if summary is available
            "content": content,
        }

    except Exception as e:
        logger.error(f"Error scraping article from {url}: {e}")
        return None
