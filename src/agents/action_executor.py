from datetime import datetime
from src.tools.maps_tool import geocode, find_nearest_shelter


def run_actions(plan: dict, approved: bool, location_hint: str = None) -> dict:
    """Logs the actions that would be dispatched. Attaches a real nearest-hospital
    suggestion to the immediate-phase action if a location is available."""
    if not approved:
        return {"executed": False, "log": ["Not approved — no actions taken."]}
    nearest_hospital = None

    if location_hint:
        try:
            geo = geocode(location_hint)
            if geo["found"]:
                nearest_hospital = find_nearest_shelter(geo["lat"], geo["lon"])

        except Exception:
            nearest_hospital = None

    log = []
    for phase in ["immediate", "short_term", "recovery"]:
        entry = {"phase": phase, "action": plan.get(phase, ""), "status": "logged"}
        if phase == "immediate" and nearest_hospital:
            entry["nearest_hospital"] = nearest_hospital
        log.append(entry)

    return {"executed": True, "timestamp": datetime.now().isoformat(), "log": log}