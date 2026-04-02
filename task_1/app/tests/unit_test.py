import pytest
from fastapi import HTTPException
import asyncio
from datetime import datetime, timedelta, timezone

from app.repository.tasks import TaskRepository
from app.schemas.tasks import TaskCreate, TaskPriority, TaskResponse, TaskStatus
from app.services.tasks import TaskService

def test_task_service_create_task_uses_repository(monkeypatch):
    due_date = datetime.now(timezone.utc) + timedelta(days=1)
    created_at = datetime.now(timezone.utc)

    payload = TaskCreate(
        title="Unit test task",
        description="TaskService.create_task",
        status=TaskStatus.pending,
        priority=TaskPriority.low,
        due_date=due_date,
        completion=False,
    )

    expected = TaskResponse(
        id=1,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
        completion=payload.completion,
        created_at=created_at,
    )

    captured = {}

    async def fake_add_one(data: TaskCreate) -> TaskResponse:
        captured["data"] = data
        return expected

    monkeypatch.setattr(TaskRepository, "add_one", fake_add_one)

    result = asyncio.run(TaskService.create_task(payload))

    assert result == expected
    assert captured["data"] == payload
