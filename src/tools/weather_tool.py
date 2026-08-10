import requests

def get_weather(lat: float, lon:float)->dict:
    """Fetches current weather via OpenMeteo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current": "temperature_2m,precipitation,wind_speed_10m"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()["current"]
    return {
        "temperature_c": data["temperature_2m"],
        "precipitation_mm": data["precipitation"],
        "wind_speed_kmh": data["wind_speed_10m"],
    }