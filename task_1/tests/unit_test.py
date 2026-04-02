import pytest
from datetime import datetime, timezone
from app.services.tasks import TaskService
from app.schemas.tasks import TaskCreate, TaskResponse
from app.models.tasks import TaskPriority, TaskStatus

def make_task_response(**kwargs) -> TaskResponse:
    defaults = dict(
        id=1,
        title="Test task",
        status=TaskStatus.pending,
        priority=TaskPriority.low,
        description=None,
        created_at=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc),
        completion=False,
        owner_id=None,
    )
    defaults.update(kwargs)
    return TaskResponse(**defaults)

@pytest.fixture
def task_data():
    return TaskCreate(
        title="Test task",
        priority=TaskPriority.low,
        due_date=datetime.now(timezone.utc),
    )

@pytest.mark.asyncio
async def test_create_task_calls_repository(mocker, task_data):
    expected = make_task_response(title=task_data.title)

    mock_add = mocker.patch(
        "app.repository.tasks.TaskRepository.add_one",
        new_callable=mocker.AsyncMock,
        return_value=expected,
    )

    result = await TaskService.create_task(task_data)

    mock_add.assert_called_once_with(task_data)
    assert result == expected
    assert result.title == task_data.title

@pytest.mark.asyncio
async def test_create_task_propagates_exception(mocker, task_data):
    mocker.patch(
        "app.repository.tasks.TaskRepository.add_one",
        new_callable=mocker.AsyncMock,
        side_effect=RuntimeError("db error"),
    )

    with pytest.raises(RuntimeError, match="db error"):
        await TaskService.create_task(task_data)