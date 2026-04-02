import pytest


@pytest.mark.integration
def test_task(authorized_client, task_payload, get_test_db):
    response = authorized_client.post("/v1/tasks", json=task_payload)
    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["title"] == task_payload["title"]
    assert data["status"] == task_payload["status"]
    assert data["priority"] == task_payload["priority"]
    assert data["description"] == task_payload["description"]
    assert data["completion"] is False
    assert data["created_at"] is not None
    assert data["due_date"] == task_payload["due_date"]

    db_task = get_test_db(data["id"])

    assert db_task is not None
    assert db_task.title == task_payload["title"]
    assert db_task.status.value == task_payload["status"]
    assert db_task.priority.value == task_payload["priority"]
    assert db_task.description == task_payload["description"]
    assert db_task.completion is False
    assert db_task.created_at is not None
    assert db_task.due_date.isoformat() == task_payload["due_date"]
