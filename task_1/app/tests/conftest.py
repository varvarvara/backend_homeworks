import asyncio
from datetime import datetime, timezone
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import app.main as main_module
from app.core.auth import get_current_user
from app.core.db import create_tables, delete_tables, engine
from app.repository.tasks import TaskRepository

@pytest.fixture
def client():
    async def _reset_schema():
        await delete_tables()
        await create_tables()
        await engine.dispose()

    asyncio.run(_reset_schema())
    with TestClient(main_module.app) as test_client:
        yield test_client
    main_module.app.dependency_overrides.clear()

@pytest.fixture
def authorized_client(client):
    main_module.app.dependency_overrides[get_current_user] = lambda: {"sub": "1"}
    yield client
    main_module.app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def task_payload():
    return {
        "title": "Integration task",
        "description": "Create through API",
        "status": "pending",
        "priority": "medium",
        "due_date": datetime.now(timezone.utc).isoformat(),
        "completion": False,
    }

@pytest.fixture
def get_test_user():
    suffix = datetime.now().strftime("%H%M%S")
    return {
        "username": f"User{suffix}",
        "email": f"User{suffix}@example.com",
        "password": "1234566436",
    }

@pytest.fixture
def get_test_db():
    async def _get_task(task_id: int):
        return await TaskRepository.find_one(task_id)

    def _reader(task_id: int):
        return asyncio.run(_get_task(task_id))

    return _reader