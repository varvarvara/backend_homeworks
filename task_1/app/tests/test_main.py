# интеграционный тест


def test_create_task_endpoint(authorized_client, task_payload) -> None:
    response = authorized_client.post("/v1/tasks", json=task_payload)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert body["title"] == "Integration task"
    assert body["status"] == "pending"
    assert body["priority"] == "medium"

    created_task_id = body["id"]
    get_response = authorized_client.get(f"/v1/tasks/{created_task_id}")
    assert get_response.status_code == 200

    persisted = get_response.json()
    assert persisted["id"] == created_task_id
    assert persisted["title"] == "Integration task"
