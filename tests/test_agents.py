"""
Tests for agent modules: action_executor, alert_monitor, quality_checker,
graph routing logic, and the planner's feedback injection.

All external calls (OpenAI, geocoder, maps) are mocked so tests run
without network access or API keys.
"""

import pytest
from unittest.mock import patch, MagicMock


# ─── action_executor ──────────────────────────────────────────────────────────

from src.agents.action_executor import run_actions

SAMPLE_PLAN = {
    "immediate":  "Deploy rescue teams immediately.",
    "short_term": "Set up temporary shelters within 48 hours.",
    "recovery":   "Rebuild damaged infrastructure over 4 weeks.",
}


def test_run_actions_rejected():
    """When approved=False, nothing is executed and a rejection message is returned."""
    result = run_actions(SAMPLE_PLAN, approved=False)

    assert result["executed"] is False
    assert "no actions taken" in result["log"][0].lower()


def test_run_actions_approved_no_location():
    """Approved with no location → all 3 phases are logged, no hospital info."""
    result = run_actions(SAMPLE_PLAN, approved=True, location_hint=None)

    assert result["executed"] is True
    assert len(result["log"]) == 3
    phases = {entry["phase"] for entry in result["log"]}
    assert phases == {"immediate", "short_term", "recovery"}
    # No hospital data expected when no location was provided
    assert "nearest_hospital" not in result["log"][0]


@patch("src.agents.action_executor.geocode", return_value={"found": True, "lat": 26.1, "lon": 91.7})
@patch("src.agents.action_executor.find_nearest_shelter", return_value={"name": "GMCH", "distance_km": 3.2, "duration_min": 8})
def test_run_actions_approved_with_location(mock_shelter, mock_geocode):
    """Approved with a valid location → nearest_hospital is attached to immediate phase."""
    result = run_actions(SAMPLE_PLAN, approved=True, location_hint="Assam, India")

    assert result["executed"] is True
    immediate_entry = result["log"][0]
    assert immediate_entry["phase"] == "immediate"
    assert immediate_entry["nearest_hospital"]["name"] == "GMCH"


@patch("src.agents.action_executor.geocode", return_value={"found": False})
def test_run_actions_geocode_not_found(mock_geocode):
    """If geocoding returns no result, execution still succeeds without hospital info."""
    result = run_actions(SAMPLE_PLAN, approved=True, location_hint="Nowhere Land")

    assert result["executed"] is True
    assert "nearest_hospital" not in result["log"][0]


def test_run_actions_result_has_timestamp():
    """Execution result always includes a timestamp string."""
    result = run_actions(SAMPLE_PLAN, approved=True)
    assert "timestamp" in result
    assert isinstance(result["timestamp"], str)


# ─── alert_monitor ────────────────────────────────────────────────────────────

from src.agents.alert_monitor import check_alert

FLOOD_RESPONSE = {
    "is_actionable_sos": True,
    "disaster_type": "flood",
    "severity": "high",
    "location_hint": "Assam, India",
    "reason": "Severe flooding with people trapped.",
}


@patch("src.agents.alert_monitor.client")
def test_check_alert_returns_expected_keys(mock_client):
    """check_alert must return a dict with all required classification fields."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"is_actionable_sos": true, "disaster_type": "flood", "severity": "high", "location_hint": "Assam", "reason": "Flooding."}'))]
    )
    result = check_alert("Heavy flooding in Assam.")

    for key in ("is_actionable_sos", "disaster_type", "severity", "location_hint", "reason"):
        assert key in result


@patch("src.agents.alert_monitor.client")
def test_check_alert_sos_true_for_urgent(mock_client):
    """An urgent message should produce is_actionable_sos=True from the LLM."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"is_actionable_sos": true, "disaster_type": "flood", "severity": "critical", "location_hint": null, "reason": "People trapped."}'))]
    )
    result = check_alert("People are trapped in floodwaters, send help!")
    assert result["is_actionable_sos"] is True


@patch("src.agents.alert_monitor.client")
def test_check_alert_non_sos(mock_client):
    """A non-urgent message should produce is_actionable_sos=False."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"is_actionable_sos": false, "disaster_type": "none", "severity": "low", "location_hint": null, "reason": "No emergency detected."}'))]
    )
    result = check_alert("Mild rain expected this weekend.")
    assert result["is_actionable_sos"] is False


# ─── quality_checker ──────────────────────────────────────────────────────────

from src.agents.quality_checker import check_plan

GOOD_PLAN = {
    "immediate":  "Evacuate residents within 1 km of river.",
    "short_term": "Set up relief camps.",
    "recovery":   "Assess infrastructure damage.",
    "used_context": ["Flood protocol: prioritise evacuation of low-lying areas."],
}

BAD_PLAN = {
    "immediate":  "Deploy 12 helicopters immediately.",  # unsupported specific claim
    "short_term": "Build 50 bridges.",
    "recovery":   "Spend $2 billion on reconstruction.",
    "used_context": ["Flood protocol: prioritise evacuation of low-lying areas."],
}


@patch("src.agents.quality_checker.client")
def test_check_plan_passes(mock_client):
    """A grounded plan should receive passed=True and an empty issues list."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"passed": true, "issues": []}'))]
    )
    result = check_plan(GOOD_PLAN, "Flooding near river.")
    assert result["passed"] is True
    assert result["issues"] == []


@patch("src.agents.quality_checker.client")
def test_check_plan_fails_with_issues(mock_client):
    """A plan with unsupported claims should receive passed=False with issue details."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"passed": false, "issues": ["12 helicopters not in context"]}'))]
    )
    result = check_plan(BAD_PLAN, "Flooding near river.")
    assert result["passed"] is False
    assert len(result["issues"]) > 0


# ─── graph routing ────────────────────────────────────────────────────────────

from src.agents.graph import route_after_check


def _state(passed: bool, retry_count: int) -> dict:
    return {"quality_result": {"passed": passed}, "retry_count": retry_count}


def test_route_passes_immediately():
    """If QA passes, route directly to executor regardless of retry count."""
    assert route_after_check(_state(passed=True, retry_count=0)) == "executor"


def test_route_retries_when_failed_under_limit():
    """If QA fails and retry count is below 3, route back to planner."""
    assert route_after_check(_state(passed=False, retry_count=1)) == "planner"
    assert route_after_check(_state(passed=False, retry_count=2)) == "planner"


def test_route_forces_executor_after_max_retries():
    """If QA fails but retry_count >= 3, force-route to executor (safety valve)."""
    assert route_after_check(_state(passed=False, retry_count=3)) == "executor"
    assert route_after_check(_state(passed=False, retry_count=5)) == "executor"


# ─── response_planner (feedback injection) ────────────────────────────────────

from src.agents.response_planner import make_response_plan


@patch("src.agents.response_planner.search_protocols", return_value=["Flood: evacuate low-lying areas."])
@patch("src.agents.response_planner.geocode", return_value={"found": False})
@patch("src.agents.response_planner.client")
def test_make_response_plan_returns_three_phases(mock_client, mock_geocode, mock_search):
    """make_response_plan must return immediate, short_term, and recovery keys."""
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"immediate": "a", "short_term": "b", "recovery": "c", "grounded": true}'))]
    )
    result = make_response_plan("Flood in Assam.", disaster_type="flood")
    for key in ("immediate", "short_term", "recovery"):
        assert key in result


@patch("src.agents.response_planner.search_protocols", return_value=[])
@patch("src.agents.response_planner.geocode", return_value={"found": False})
@patch("src.agents.response_planner.client")
def test_make_response_plan_injects_feedback(mock_client, mock_geocode, mock_search):
    """previous_issues must be appended to the prompt sent to the LLM."""
    captured_prompts = []

    def capture_call(**kwargs):
        captured_prompts.append(kwargs["messages"][0]["content"])
        return MagicMock(
            choices=[MagicMock(message=MagicMock(content='{"immediate":"a","short_term":"b","recovery":"c","grounded":true}'))]
        )

    mock_client.chat.completions.create.side_effect = capture_call

    make_response_plan(
        "Flood in Assam.", disaster_type="flood",
        previous_issues=["Plan mentioned unverified rescue numbers."],
    )

    assert len(captured_prompts) == 1
    assert "IMPORTANT" in captured_prompts[0]
    assert "unverified rescue numbers" in captured_prompts[0]


@patch("src.agents.response_planner.search_protocols", return_value=[])
@patch("src.agents.response_planner.geocode", return_value={"found": False})
@patch("src.agents.response_planner.client")
def test_make_response_plan_no_feedback_when_none(mock_client, mock_geocode, mock_search):
    """When previous_issues=None, the IMPORTANT block must NOT appear in the prompt."""
    captured_prompts = []

    def capture_call(**kwargs):
        captured_prompts.append(kwargs["messages"][0]["content"])
        return MagicMock(
            choices=[MagicMock(message=MagicMock(content='{"immediate":"a","short_term":"b","recovery":"c","grounded":true}'))]
        )

    mock_client.chat.completions.create.side_effect = capture_call

    make_response_plan("Flood in Assam.", disaster_type="flood", previous_issues=None)

    assert "IMPORTANT" not in captured_prompts[0]
