import requests

def geocode(address: str) -> dict:
    """Converts an address/place name to lat/lon via OpenStreetMap Nominatim """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "genesis-ai-disaster-response"}  # Nominatim requires this
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    results = response.json()
    if not results:
        return {"found": False}
    return {"found": True, "lat": float(results[0]["lat"]), "lon": float(results[0]["lon"])}


def get_route(start: tuple, end: tuple) -> dict:
    """Gets a driving route between two (lat, lon) points via OSRM's """
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}"
    response = requests.get(url, params={"overview": "false"}, timeout=10)
    response.raise_for_status()
    route = response.json()["routes"][0]
    return {"distance_km": route["distance"] / 1000, "duration_min": route["duration"] / 60}