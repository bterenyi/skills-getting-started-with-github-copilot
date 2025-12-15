from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def setup_function():
    # Reset participants to known state before each test
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_unregister_existing_participant():
    resp = client.delete(
        "/activities/Chess%20Club/participants?email=michael@mergington.edu"
    )
    assert resp.status_code == 200
    assert "Unregistered michael@mergington.edu" in resp.json()["message"]

    # Verify the participant is removed
    activities_resp = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities_resp["Chess Club"]["participants"]


def test_unregister_nonexistent_participant_returns_404():
    resp = client.delete(
        "/activities/Chess%20Club/participants?email=notfound@example.com"
    )
    assert resp.status_code == 404


def test_unregister_nonexistent_activity_returns_404():
    resp = client.delete("/activities/Nope/participants?email=someone@example.com")
    assert resp.status_code == 404
