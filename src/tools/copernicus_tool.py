import io
import zipfile
import requests
import numpy as np
import rasterio
from PIL import Image

ACTIVATIONS_URL = "https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations-info/"
DETAILS_URL = "https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations/"


def list_activations(disaster_type: str = None, limit: int = 10) -> list[dict]:
    """Fetches recent Copernicus EMS activations. If disaster_type given, filters
    to that category (flood, wildfire, earthquake, storm, etc). If None, returns all types."""
    response = requests.get(ACTIVATIONS_URL, params={"limit": 50}, timeout=15)
    response.raise_for_status()
    results = response.json()["results"]
    if disaster_type:
        results = [a for a in results if a["category"].lower() == disaster_type.lower()]
    return results[:limit]


def get_activation_details(code: str) -> dict:
    """Fetches full detail for one activation — AOIs, products, download links."""
    response = requests.get(DETAILS_URL, params={"code": code}, timeout=15)
    response.raise_for_status()
    return response.json()["results"][0]


def download_activation_map_image(code: str, save_path: str = "activation_map.png") -> str:
    """Downloads the first product's ZIP, extracts the GeoTIFF, converts it to a viewable PNG.
    Handles nodata pixels (gaps outside the mapped area) so the image doesn't come out blank."""
    details = get_activation_details(code)
    product = details["aois"][0]["products"][0]

    zip_response = requests.get(product["downloadPath"], timeout=60)
    zip_response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(zip_response.content)) as z:
        tif_name = next(n for n in z.namelist() if n.lower().endswith(".tif"))
        tif_bytes = z.read(tif_name)

    with rasterio.open(io.BytesIO(tif_bytes)) as src:
        nodata = src.nodata
        arr = src.read([1, 2, 3]) if src.count >= 3 else src.read(1)
        if src.count >= 3:
            arr = np.transpose(arr, (1, 2, 0))

    arr = arr.astype(np.float32)
    if nodata is not None:
        arr[arr == nodata] = np.nan

    valid_min = np.nanmin(arr)
    valid_max = np.nanmax(arr)
    arr = np.nan_to_num(arr, nan=valid_min)
    arr = 255 * (arr - valid_min) / (valid_max - valid_min + 1e-6)
    arr = np.clip(arr, 0, 255).astype(np.uint8)

    Image.fromarray(arr).save(save_path)
    return save_path