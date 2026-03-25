import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from app.repository.tasks import TaskRepository
from app.schemas.tasks import TaskCreate, TaskPriority, TaskResponse, TaskStatus
from app.services.tasks import TaskService


@pytest.fixture
def task_payload():
    return TaskCreate(
        title="Unit test task",
        description="TaskService.create_task",
        status=TaskStatus.pending,
        priority=TaskPriority.low,
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
        completion=False,
    )


@pytest.fixture
def expected_response(task_payload):
    return TaskResponse(
        id=1,
        title=task_payload.title,
        description=task_payload.description,
        status=task_payload.status,
        priority=task_payload.priority,
        due_date=task_payload.due_date,
        completion=task_payload.completion,
        created_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def repository_add_one_stub(expected_response):
    captured = {}

    async def fake_add_one(data: TaskCreate) -> TaskResponse:
        captured["data"] = data
        return expected_response

    original_add_one = TaskRepository.add_one
    TaskRepository.add_one = fake_add_one
    try:
        yield captured
    finally:
        TaskRepository.add_one = original_add_one


def test_task_service_create_task_uses_repository(
    task_payload,
    expected_response,
    repository_add_one_stub,
):
    result = asyncio.run(TaskService.create_task(task_payload))

    assert result == expected_response
    assert repository_add_one_stub["data"] == task_payload
    assert isinstance(result.id, int)
