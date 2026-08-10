import time
import requests
import xml.etree.ElementTree as ET

def fetch_news(query: str, limit: int = 5) -> list[dict]:
    """Fetches recent news articles from Google News RSS matching a query.
    This replaces GDELT to avoid strict IP rate limits while still providing LIVE data.
    Returns a normalized list: {text, source, location_hint, timestamp}."""
    
    # URL encode the query
    safe_query = requests.utils.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={safe_query}&hl=en-US&gl=US&ceid=US:en"
    
    response = requests.get(rss_url, timeout=15)
    response.raise_for_status()
    
    # Parse the XML response
    root = ET.fromstring(response.text)
    items = root.findall('.//item')
    
    # Get only up to the limit
    items = items[:limit]
    
    return [
        {
            "text": item.find('title').text if item.find('title') is not None else "",
            "source": "live_news_rss",
            "location_hint": None, # Google News doesn't provide structured locations, LLM will extract it
            "timestamp": item.find('pubDate').text if item.find('pubDate') is not None else None,
        }
        for item in items
    ]