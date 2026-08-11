from fastapi import APIRouter , HTTPException
from datetime import datetime

from src.api.schemas import IncidentCreateRequest, IncidentResponse, ApprovalRequest, ExecutionResponse
from src.agents.graph import app as genesis_app
from src.db.session import get_session
from src.db.models import Incident

router = APIRouter()

_pending_incidents: dict = {}

@router.post("/incidents", response_model=IncidentResponse)
def create_incident(payload: IncidentCreateRequest):
    """Starts a new incident, runs it up to the human-approval pause."""
    thread_id = f"incident-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "situation": payload.situation,
        "image_path": payload.image_path,
        "alert_info": {}, "image_findings": {}, "response_plan": {},
        "quality_result": {}, "execution_result": {},
        "location_coords": None, "approved": None, "retry_count": 0,
    }
    _pending_incidents[thread_id] = (initial_state, config)
    result = genesis_app.invoke(initial_state, config=config)

    return IncidentResponse(
        thread_id=thread_id,
        alert_info=result["alert_info"],
        image_findings=result["image_findings"],
        response_plan=result["response_plan"],
        quality_result=result["quality_result"],
        retry_count=result["retry_count"],
        awaiting_approval=True,
    )

@router.post("/incidents/{thread_id}/approve", response_model=ExecutionResponse)
def approve_incident(thread_id:str, payload: ApprovalRequest):
    """Resumes a paused incident after a human approval decision, saves to DB."""
    if thread_id not in _pending_incidents:
        raise HTTPException(status_code=404, detail="Incident not found or already completed.")

    initial_state, config = _pending_incidents.pop(thread_id)
    genesis_app.update_state(config, {"approved": payload.approved})
    result = genesis_app.invoke(None, config=config)

    session = next(get_session())
    incident = Incident(
        thread_id=thread_id,
        situation=initial_state["situation"],
        image_path=initial_state["image_path"],
        alert_info=result["alert_info"],
        image_findings=result["image_findings"],
        response_plan=result["response_plan"],
        quality_result=result["quality_result"],
        execution_result=result["execution_result"],
        location_lat=result["location_coords"]["lat"] if result.get("location_coords") else None,
        location_lon=result["location_coords"]["lon"] if result.get("location_coords") else None,
        approved=result["approved"],
        retry_count=result["retry_count"],
    )

    session.add(incident)
    session.commit()
    return ExecutionResponse(thread_id=thread_id, execution_result=result["execution_result"])