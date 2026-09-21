import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "LEAVE_REQUESTS": []})
    return app.test_client()


def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_list_employees(client):
    response = client.get("/api/employees")

    assert response.status_code == 200
    assert len(response.get_json()["employees"]) == 3


def test_create_leave_request(client):
    response = client.post(
        "/api/leaves",
        json={
            "employee_id": 1,
            "start_date": "2026-10-01",
            "end_date": "2026-10-03",
            "reason": "Family event",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["status"] == "pending"
    assert client.get("/api/leaves").get_json()["leaves"] == [response.get_json()]


def test_rejects_invalid_date_range(client):
    response = client.post(
        "/api/leaves",
        json={
            "employee_id": 1,
            "start_date": "2026-10-03",
            "end_date": "2026-10-01",
            "reason": "Family event",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "End date cannot be before start date"
