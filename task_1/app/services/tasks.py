from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.core.adapters import get_storage_adapter
from app.core.exceptions import TaskNotFoundException
from app.repository.tasks import TaskRepository
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    @classmethod
    async def create_task(cls, data: TaskCreate) -> TaskResponse:
        return await TaskRepository.add_one(data)

    @classmethod
    async def get_tasks(cls) -> list[TaskResponse]:
        return await TaskRepository.find_all()

    @classmethod
    async def get_task(cls, task_id: int) -> TaskResponse | None:
        return await TaskRepository.find_one(task_id)

    @classmethod
    async def update_task(cls, task_id: int, data: TaskUpdate) -> TaskResponse | None:
        return await TaskRepository.update_one(task_id, data)

    @classmethod
    async def delete_task(cls, task_id: int) -> bool:
        return await TaskRepository.delete_one(task_id)

    @classmethod
    async def upload_avatar(cls, task_id: int, file: UploadFile) -> str:
        task = await TaskRepository.find_one(task_id)
        if task is None:
            raise TaskNotFoundException(task_id)

        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")

        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed")

        original_name = Path(file.filename or "avatar.bin").name
        key = f"tasks/{task_id}/avatars/{uuid4().hex}_{original_name}"
        storage = get_storage_adapter()
        return await storage.upload(
            content=content,
            key=key,
            content_type=file.content_type or "application/octet-stream",
        )


task_service = TaskService()
