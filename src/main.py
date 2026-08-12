import argparse
import json
from datetime import datetime
from src.db.session import create_db_and_tables, get_session
from src.db.models import Incident
from src.agents.graph import app
from src.utils.helpers import configure_logging, state_summary, flatten_plan_to_text

configure_logging()
import logging
logger = logging.getLogger("genesis")

def save_incident(thread_id: str, initial_state: dict, result: dict) -> None:
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
    session = next(get_session())
    session.add(incident)
    session.commit()
    print(f"\nSaved incident {thread_id} to database.")

def run_incident(situation: str, image_path: str = None) -> None:
    """Runs one incident through the full Genesis pipeline via CLI, pausing for human approval before dispatch."""
    thread_id = f"incident-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "situation": situation,
        "image_path": image_path,
        "alert_info": {}, "image_findings": {}, "response_plan": {},
        "quality_result": {}, "execution_result": {},
        "approved": None, "retry_count": 0,
        "location_coords": None,
    }

    print(f"\n--- Running incident: {thread_id} ---\n")
    result = app.invoke(initial_state, config=config)

    logger.info("Pipeline complete: %s", state_summary(result))

    print("\nAlert classification:", json.dumps(result["alert_info"], indent=2))
    print("\nImage findings:", json.dumps(result["image_findings"], indent=2))
    print("\nResponse plan:")
    print(flatten_plan_to_text(result["response_plan"]))
    print(f"\nQuality check: passed={result['quality_result'].get('passed')}, retries={result['retry_count']}")
    issues = result["quality_result"].get("issues", [])
    if issues:
        print("Issues found:", issues)

    answer = input("\nApprove and dispatch this plan? (y/n): ").strip().lower()
    approved = answer == "y"

    app.update_state(config, {"approved": approved})
    final_result = app.invoke(None, config=config)

    print("\n--- Execution result ---")
    print("\nLocation coordinates:", result.get("location_coords"))
    print(json.dumps(final_result["execution_result"], indent=2))

    save_incident(thread_id, initial_state, final_result)

create_db_and_tables()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run one disaster incident through Genesis.")
    parser.add_argument("situation", type=str, help="Description of the incident")
    parser.add_argument("--image", type=str, default=None, help="Optional image path or URL")
    args = parser.parse_args()

    run_incident(args.situation, args.image)