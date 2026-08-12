"""
Tests for the FastAPI routes: POST /incidents and POST /incidents/{id}/approve.

Uses FastAPI's TestClient so no server process is needed.
The LangGraph app and DB session are mocked to keep tests fast and isolated.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


# ─── App fixture ──────────────────────────────────────────────────────────────

@pytest.fixture()
def client():
    """Return a TestClient with the DB initialisation patched out."""
    with patch("src.db.session.create_db_and_tables"):
        from src.api.app import create_app
        app = create_app()
        yield TestClient(app)


# ─── Shared mock state ────────────────────────────────────────────────────────

MOCK_PIPELINE_RESULT = {
    "alert_info":      {"is_actionable_sos": True, "disaster_type": "flood", "severity": "high", "location_hint": "Assam", "reason": "Flooding."},
    "image_findings":  {"flooded_zones": True, "notes": "Extensive flooding visible."},
    "response_plan":   {"immediate": "Evacuate.", "short_term": "Shelters.", "recovery": "Rebuild.", "used_context": []},
    "quality_result":  {"passed": True, "issues": []},
    "execution_result": {"executed": True, "timestamp": "2024-01-01T00:00:00", "log": [], "quality_warning": False},
    "location_coords": {"lat": 26.14, "lon": 91.74},
    "retry_count":     1,
    "approved":        None,
}

MOCK_EXECUTION_RESULT = {
    **MOCK_PIPELINE_RESULT,
    "approved": True,
    "execution_result": {
        "executed": True,
        "timestamp": "2024-01-01T00:00:01",
        "log": [{"phase": "immediate", "action": "Evacuate.", "status": "logged"}],
        "quality_warning": False,
    },
}


# ─── POST /incidents ──────────────────────────────────────────────────────────

@patch("src.api.routes.incidents.genesis_app")
def test_create_incident_returns_200(mock_app, client):
    """POST /incidents with a valid situation returns 200 and awaiting_approval=True."""
    mock_app.invoke.return_value = MOCK_PIPELINE_RESULT

    response = client.post("/incidents", json={"situation": "Flooding in Assam, India."})
    assert response.status_code == 200

    data = response.json()
    assert data["awaiting_approval"] is True
    assert "thread_id" in data
    assert data["thread_id"].startswith("incident-")


@patch("src.api.routes.incidents.genesis_app")
def test_create_incident_response_shape(mock_app, client):
    """POST /incidents response includes all expected top-level fields."""
    mock_app.invoke.return_value = MOCK_PIPELINE_RESULT

    data = client.post("/incidents", json={"situation": "Earthquake in Tokyo."}).json()

    for field in ("thread_id", "alert_info", "image_findings", "response_plan", "quality_result", "retry_count"):
        assert field in data, f"Missing field: {field}"


def test_create_incident_missing_situation(client):
    """POST /incidents without a situation body returns 422 Unprocessable Entity."""
    response = client.post("/incidents", json={})
    assert response.status_code == 422


# ─── POST /incidents/{thread_id}/approve ─────────────────────────────────────

@patch("src.api.routes.incidents.genesis_app")
@patch("src.api.routes.incidents.get_session")
def test_approve_incident_authorized(mock_session, mock_app, client):
    """Approving a pending incident returns 200 and execution_result with executed=True."""
    # First, create the incident so it enters _pending_incidents
    mock_app.invoke.return_value = MOCK_PIPELINE_RESULT
    create_resp = client.post("/incidents", json={"situation": "Flood."})
    thread_id = create_resp.json()["thread_id"]

    # Now approve it
    mock_app.invoke.return_value = MOCK_EXECUTION_RESULT

    # Mock DB session
    mock_db = MagicMock()
    mock_session.return_value = iter([mock_db])

    response = client.post(f"/incidents/{thread_id}/approve", json={"approved": True})
    assert response.status_code == 200

    data = response.json()
    assert data["thread_id"] == thread_id
    assert data["execution_result"]["executed"] is True


@patch("src.api.routes.incidents.genesis_app")
@patch("src.api.routes.incidents.get_session")
def test_approve_incident_rejected(mock_session, mock_app, client):
    """Rejecting an incident returns 200 with executed=False."""
    mock_app.invoke.return_value = MOCK_PIPELINE_RESULT
    create_resp = client.post("/incidents", json={"situation": "Flood."})
    thread_id = create_resp.json()["thread_id"]

    rejected_result = {
        **MOCK_EXECUTION_RESULT,
        "approved": False,
        "execution_result": {"executed": False, "log": ["Not approved — no actions taken."]},
    }
    mock_app.invoke.return_value = rejected_result

    mock_db = MagicMock()
    mock_session.return_value = iter([mock_db])

    response = client.post(f"/incidents/{thread_id}/approve", json={"approved": False})
    assert response.status_code == 200
    assert response.json()["execution_result"]["executed"] is False


def test_approve_nonexistent_incident_returns_404(client):
    """Approving a thread_id that doesn't exist returns 404."""
    response = client.post("/incidents/incident-does-not-exist/approve", json={"approved": True})
    assert response.status_code == 404


@patch("src.api.routes.incidents.genesis_app")
@patch("src.api.routes.incidents.get_session")
def test_approve_incident_twice_returns_404(mock_session, mock_app, client):
    """After approval, the same thread_id cannot be approved again (already removed from pending)."""
    mock_app.invoke.return_value = MOCK_PIPELINE_RESULT
    create_resp = client.post("/incidents", json={"situation": "Fire."})
    thread_id = create_resp.json()["thread_id"]

    mock_app.invoke.return_value = MOCK_EXECUTION_RESULT
    mock_db = MagicMock()
    mock_session.return_value = iter([mock_db])

    # First approval succeeds
    client.post(f"/incidents/{thread_id}/approve", json={"approved": True})

    # Second attempt on the same thread_id must 404
    response = client.post(f"/incidents/{thread_id}/approve", json={"approved": True})
    assert response.status_code == 404


# ─── GET /health ──────────────────────────────────────────────────────────────

def test_health_check(client):
    """GET /health returns 200 with a status field."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
