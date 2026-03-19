from fastapi import APIRouter, HTTPException, status

from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from app.services.tasks import TaskService
from app.core.db import SessionLocal

task_service = TaskService()
taskRouter = APIRouter(prefix="/tasks", tags=["Tasks"])

@taskRouter.get("", response_model=list[TaskResponse], status_code=200)
async def get_tasks():
    return await task_service.get_tasks()


@taskRouter.post("", response_model=TaskResponse, status_code=201)
async def create_task(payload: TaskCreate):
    return await task_service.create_task(payload)


@taskRouter.get("/{task_id}", response_model=TaskResponse, status_code=200)
async def get_task(task_id: int):
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@taskRouter.put("/{task_id}", response_model=TaskResponse, status_code=200)
async def update_task(task_id: int, payload: TaskUpdate):
    task = await task_service.update_task(task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@taskRouter.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    deleted = await task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return
