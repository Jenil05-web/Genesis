"""
Tests for tool modules: maps_tool, weather_tool, gdelt_tool, dataset_tool.

All HTTP calls are mocked — tests run entirely offline.
"""

import pytest
from unittest.mock import patch, MagicMock


# ─── maps_tool ────────────────────────────────────────────────────────────────

from src.tools.maps_tool import geocode, get_route, find_nearby_hospitals, find_nearest_shelter


@patch("src.tools.maps_tool.requests.get")
def test_geocode_found(mock_get):
    """geocode returns lat/lon when Nominatim returns a result."""
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: [{"lat": "26.1445", "lon": "91.7362"}],
    )
    mock_get.return_value.raise_for_status = lambda: None

    result = geocode("Assam, India")
    assert result["found"] is True
    assert abs(result["lat"] - 26.1445) < 0.001
    assert abs(result["lon"] - 91.7362) < 0.001


@patch("src.tools.maps_tool.requests.get")
def test_geocode_not_found(mock_get):
    """geocode returns found=False when Nominatim returns an empty list."""
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: [],
    )
    mock_get.return_value.raise_for_status = lambda: None

    result = geocode("xyzzy-nonexistent-place")
    assert result["found"] is False
    assert "lat" not in result


@patch("src.tools.maps_tool.requests.get")
def test_get_route_returns_distance_and_duration(mock_get):
    """get_route converts OSRM metres→km and seconds→minutes correctly."""
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"routes": [{"distance": 5000, "duration": 600}]},
    )
    mock_get.return_value.raise_for_status = lambda: None

    result = get_route((26.1, 91.7), (26.2, 91.8))
    assert result["distance_km"] == pytest.approx(5.0)
    assert result["duration_min"] == pytest.approx(10.0)


@patch("src.tools.maps_tool.requests.post")
def test_find_nearby_hospitals_returns_list(mock_post):
    """find_nearby_hospitals parses Overpass elements into a list of dicts."""
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "elements": [
                {"lat": 26.15, "lon": 91.74, "tags": {"name": "GMCH"}},
                {"lat": 26.18, "lon": 91.78, "tags": {"name": "Downtown Hospital"}},
            ]
        },
    )
    mock_post.return_value.raise_for_status = lambda: None

    results = find_nearby_hospitals(26.1, 91.7)
    assert len(results) == 2
    assert results[0]["name"] == "GMCH"
    assert "lat" in results[0] and "lon" in results[0]


@patch("src.tools.maps_tool.requests.post")
def test_find_nearby_hospitals_empty(mock_post):
    """find_nearby_hospitals returns an empty list when no hospitals are found."""
    mock_post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"elements": []},
    )
    mock_post.return_value.raise_for_status = lambda: None

    results = find_nearby_hospitals(0.0, 0.0)
    assert results == []


@patch("src.tools.maps_tool.find_nearby_hospitals", return_value=[
    {"name": "City Hospital", "lat": 26.12, "lon": 91.73},
    {"name": "District Hospital", "lat": 26.20, "lon": 91.80},
])
@patch("src.tools.maps_tool.get_route", side_effect=[
    {"distance_km": 3.5, "duration_min": 8},
    {"distance_km": 9.1, "duration_min": 22},
])
def test_find_nearest_shelter_picks_closest(mock_route, mock_hospitals):
    """find_nearest_shelter returns the hospital with the shortest driving distance."""
    result = find_nearest_shelter(26.1, 91.7)
    assert result["name"] == "City Hospital"
    assert result["distance_km"] == pytest.approx(3.5)


@patch("src.tools.maps_tool.find_nearby_hospitals", return_value=[])
def test_find_nearest_shelter_no_hospitals(mock_hospitals):
    """find_nearest_shelter returns None when no hospitals exist nearby."""
    result = find_nearest_shelter(0.0, 0.0)
    assert result is None


# ─── weather_tool ─────────────────────────────────────────────────────────────

from src.tools.weather_tool import get_weather


@patch("src.tools.weather_tool.requests.get")
def test_get_weather_returns_expected_keys(mock_get):
    """get_weather parses Open-Meteo response into temperature, precipitation, wind."""
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "current": {
                "temperature_2m": 28.5,
                "precipitation": 12.3,
                "wind_speed_10m": 45.0,
            }
        },
    )
    mock_get.return_value.raise_for_status = lambda: None

    result = get_weather(26.1, 91.7)
    assert result["temperature_c"] == pytest.approx(28.5)
    assert result["precipitation_mm"] == pytest.approx(12.3)
    assert result["wind_speed_kmh"] == pytest.approx(45.0)


# ─── gdelt_tool ───────────────────────────────────────────────────────────────

from src.tools.gdelt_tool import fetch_news


@patch("src.tools.gdelt_tool.requests.get")
def test_fetch_news_returns_list_of_dicts(mock_get):
    """fetch_news returns a list of dicts, each with a 'text' key."""
    rss_xml = """<?xml version="1.0"?>
    <rss version="2.0">
      <channel>
        <item><title>Flood hits Assam</title><link>http://example.com/1</link><pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate></item>
        <item><title>Earthquake in Japan</title><link>http://example.com/2</link><pubDate>Mon, 01 Jan 2024 01:00:00 GMT</pubDate></item>
      </channel>
    </rss>"""
    mock_get.return_value = MagicMock(status_code=200, text=rss_xml)
    mock_get.return_value.raise_for_status = lambda: None

    results = fetch_news("flood", limit=2)
    assert isinstance(results, list)
    assert len(results) == 2
    assert "text" in results[0]
    assert "Flood hits Assam" in results[0]["text"]


@patch("src.tools.gdelt_tool.requests.get")
def test_fetch_news_respects_limit(mock_get):
    """fetch_news returns at most `limit` items."""
    items = "\n".join(
        f"<item><title>Story {i}</title><link>http://x.com/{i}</link></item>"
        for i in range(10)
    )
    rss_xml = f"<rss><channel>{items}</channel></rss>"
    mock_get.return_value = MagicMock(status_code=200, text=rss_xml)
    mock_get.return_value.raise_for_status = lambda: None

    results = fetch_news("flood", limit=3)
    assert len(results) <= 3


@patch("src.tools.gdelt_tool.requests.get", side_effect=Exception("network error"))
def test_fetch_news_handles_error_gracefully(mock_get):
    """fetch_news returns an empty list on any network failure."""
    results = fetch_news("flood")
    assert results == []


# ─── dataset_tool ─────────────────────────────────────────────────────────────

from src.tools.dataset_tool import load_sample_messages


@patch("src.tools.dataset_tool._dataset", None)
@patch("src.tools.dataset_tool.load_dataset")
def test_load_sample_messages_returns_correct_count(mock_load):
    """load_sample_messages returns exactly `limit` messages."""
    rows = [{"text": f"message {i}"} for i in range(20)]
    mock_dataset = MagicMock()
    mock_dataset.__iter__ = MagicMock(return_value=iter(rows))
    # Simulate shuffle returning a sliceable mock
    mock_dataset.shuffle.return_value = rows
    mock_load.return_value = {"train": mock_dataset}

    # Re-import to pick up the patched load_dataset
    import importlib
    import src.tools.dataset_tool as dt_module
    dt_module._dataset = None       # force reload of the dataset
    dt_module._dataset = mock_dataset

    results = dt_module.load_sample_messages(limit=5)
    assert len(results) == 5


def test_load_sample_messages_returns_list_of_dicts():
    """Each message returned by load_sample_messages must have a 'text' key."""
    with patch("src.tools.dataset_tool._dataset") as mock_ds:
        rows = [{"text": f"emergency {i}"} for i in range(10)]
        mock_ds.shuffle.return_value = rows

        import src.tools.dataset_tool as dt_module
        dt_module._dataset = mock_ds

        results = dt_module.load_sample_messages(limit=3)
        for item in results:
            assert "text" in item
