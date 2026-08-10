from datetime import datetime

def run_actions(plan:dict , approved : bool)-> dict:
    """Logs the actions that would be dispatched """
    if not approved:
        return {"executed": False, "log": ["Not approved — no actions taken."]}


    log = []
    for phase in ["immediate", "short_term", "recovery"]:
        action_text = plan.get(phase, "")
        log.append({"phase": phase, "action": action_text, "status": "logged"})

    return {"executed": True, "timestamp": datetime.now().isoformat(), "log": log}
