import pytest


@pytest.mark.integration
def test_create_task_endpoint(authorized_client, task_payload):
    response = authorized_client.post("/v1/tasks", json=task_payload)

    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["title"] == task_payload["title"]
    assert data["status"] == task_payload["status"]
    assert data["priority"] == task_payload["priority"]

    created_task_id = data["id"]
    get_response = authorized_client.get(f"/v1/tasks/{created_task_id}")
    assert get_response.status_code == 200

    persisted = get_response.json()
    assert persisted["id"] == created_task_id
    assert persisted["title"] == task_payload["title"]
