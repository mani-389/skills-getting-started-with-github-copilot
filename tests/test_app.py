import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture()
def client():
    return TestClient(app)


def test_unregister_participant_removes_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/participants/unknown@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
