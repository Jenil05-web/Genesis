import requests
GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

def fetch_news(query:str, limit: int = 5)->list[dict]:
    """Fetches recent English-language news articles from GDELT matching a query
    Returns a normalized list: {text, source, location_hint, timestamp}."""

    params = {
        "query": f"{query} sourcelang:eng",
        "mode": "artlist",
        "maxrecords": limit,
        "format": "json",
    }

    try:
        response = requests.get(GDELT_URL, params=params, timeout=15)
        response.raise_for_status()
        articles = response.json().get("articles", [])
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("Warning: GDELT API rate limit exceeded (429). Returning mock data.")
            articles = [{
                "title": f"Mock Alert: Severe {query} reported in area",
                "sourcecountry": "US",
                "seendate": "20260810000000"
            }]
        else:
            raise e

    return [
        {
            "text": a["title"],
            "source": "gdelt",
            "location_hint": a.get("sourcecountry"),
            "timestamp": a.get("seendate"),

        }
        for a in articles

]