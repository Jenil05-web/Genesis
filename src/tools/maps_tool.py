import requests
import logging
from src.utils.helpers import with_retry

logger = logging.getLogger("genesis")


def geocode(address: str) -> dict:
    """Converts an address/place name to lat/lon via OpenStreetMap Nominatim """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "genesis-ai-disaster-response"}  # Nominatim requires this
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    results = response.json()
    if not results:
        logger.warning("geocode: no result for %r", address)
        return {"found": False}
    logger.info("geocode: %r → (%.4f, %.4f)", address, float(results[0]["lat"]), float(results[0]["lon"]))
    return {"found": True, "lat": float(results[0]["lat"]), "lon": float(results[0]["lon"])}


def get_route(start: tuple, end: tuple) -> dict:
    """Gets a driving route between two (lat, lon) points via OSRM's """
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}"
    response = requests.get(url, params={"overview": "false"}, timeout=10)
    response.raise_for_status()
    route = response.json()["routes"][0]
    return {"distance_km": route["distance"] / 1000, "duration_min": route["duration"] / 60}

@with_retry(max_attempts=3, delay_seconds=1.0, backoff=2.0, exceptions=(requests.exceptions.RequestException,))
def find_nearby_hospitals(lat: float, lon: float, radius_km: int = 20, limit: int = 5) -> list[dict]:
    """Queries Overpass API for real hospitals near any coordinate. Retried automatically on failure."""
    radius_m = radius_km * 1000
    query = f"""
    [out:json];
    node["amenity"="hospital"](around:{radius_m},{lat},{lon});
    out;
    """
    headers = {"User-Agent": "genesis-ai-disaster-response"}
    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query, headers=headers, timeout=30,
    )
    response.raise_for_status()
    elements = response.json()["elements"][:limit]
    logger.info("find_nearby_hospitals: found %d hospitals within %dkm of (%.4f, %.4f)", len(elements), radius_km, lat, lon)
    return [
        {"name": e.get("tags", {}).get("name", "Unnamed hospital"), "lat": e["lat"], "lon": e["lon"]}
        for e in elements
    ]

def find_nearest_shelter(lat: float, lon: float) -> dict:
    """Finds real nearby hospitals for any location, routes to each, returns the closest."""
    hospitals = find_nearby_hospitals(lat, lon)
    best = None
    for h in hospitals:
        route = get_route((lat, lon), (h["lat"], h["lon"]))
        if best is None or route["distance_km"] < best["distance_km"]:
            best = {**h, **route}
    return best