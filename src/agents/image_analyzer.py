from src.tools.vision_tool import analyze_image


def check_image(image_path_or_url: str = None) -> dict:
    """Runs image analysis if an image was given. If not, returns empty findings instead of crashing."""
    if not image_path_or_url:
        return {
            "flooded_zones": None,
            "blocked_roads": None,
            "collapsed_structures": None,
            "severity_estimate": None,
            "notes": "no image provided",
        }
    return analyze_image(image_path_or_url)

