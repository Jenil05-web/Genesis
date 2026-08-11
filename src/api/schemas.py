from pydantic import BaseModel
from typing import Optional


class IncidentCreateRequest(BaseModel):
    situation: str
    image_path: Optional[str] = None


class IncidentResponse(BaseModel):
    thread_id: str
    alert_info: dict
    image_findings: dict
    response_plan: dict
    quality_result: dict
    retry_count: int
    awaiting_approval: bool
    location_coords: Optional[dict] = None


class ApprovalRequest(BaseModel):
    approved: bool


class ExecutionResponse(BaseModel):
    thread_id: str
    execution_result: dict

    """In short: these define the exact shape of what the API accepts/returns — separate from GenesisState,
      since an API contract shouldn't change just because you tweak internal graph fields later."""