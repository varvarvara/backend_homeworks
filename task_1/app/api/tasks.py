from fastapi import APIRouter, File, UploadFile, status

from app.core.exceptions import TaskNotFoundException
from app.schemas.tasks import TaskAvatarUploadResponse, TaskCreate, TaskResponse, TaskUpdate
from app.services.tasks import TaskService


task_service = TaskService()
taskRouter = APIRouter(prefix="/v1/tasks", tags=["Tasks"])


@taskRouter.get("", response_model=list[TaskResponse], status_code=200)
async def get_tasks():
    return await task_service.get_tasks()


@taskRouter.post("", response_model=TaskResponse, status_code=201)
async def create_task(payload: TaskCreate):
    return await task_service.create_task(payload)


@taskRouter.get("/{task_id}", response_model=TaskResponse, status_code=200)
async def get_task(task_id: int):
    task = await task_service.get_task(task_id)
    if task is None:
        raise TaskNotFoundException(task_id)
    return task


@taskRouter.put("/{task_id}", response_model=TaskResponse, status_code=200)
async def update_task(task_id: int, payload: TaskUpdate):
    task = await task_service.update_task(task_id, payload)
    if task is None:
        raise TaskNotFoundException(task_id)
    return task


@taskRouter.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    deleted = await task_service.delete_task(task_id)
    if deleted is False:
        raise TaskNotFoundException(task_id)
    return


@taskRouter.post(
    "/{id}/upload-avatar",
    response_model=TaskAvatarUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_task_avatar(id: int, file: UploadFile = File(...)):
    url = await task_service.upload_avatar(task_id=id, file=file)
    return TaskAvatarUploadResponse(url=url)
