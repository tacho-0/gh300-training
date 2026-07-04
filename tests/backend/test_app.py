from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_remove_participant_from_activity():
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_remove_participant_returns_404_when_not_found():
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_returns_400_when_activity_is_full():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        activities[activity_name]["participants"] = [
            f"filled{i}@mergington.edu" for i in range(activities[activity_name]["max_participants"])
        ]

        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
    finally:
        activities[activity_name]["participants"] = original_participants
