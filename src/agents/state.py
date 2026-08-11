from typing import TypedDict, Optional

class GenesisState(TypedDict):
    situation: str
    image_path: Optional[str]

    alert_info: dict
    image_findings: dict
    response_plan: dict
    quality_result: dict
    execution_result: dict

    location_coords: Optional[dict]
    approved: Optional[bool]
    retry_count: int
    previous_issues: Optional[list]