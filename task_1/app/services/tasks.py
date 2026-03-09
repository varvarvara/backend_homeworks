from app.repository.repository import TaskRepository
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate


class TaskService:
    async def get_tasks(self) -> list[TaskResponse]:
        return await TaskRepository.find_all()

    async def get_task(self, task_id: int) -> TaskResponse | None:
        return await TaskRepository.find_one(task_id)

    async def create_task(self, data: TaskCreate) -> TaskResponse:
        return await TaskRepository.add_one(data)

    async def update_task(self, task_id: int, data: TaskUpdate) -> TaskResponse | None:
        return await TaskRepository.update_one(task_id, data)

    async def delete_task(self, task_id: int) -> bool:
        return await TaskRepository.delete_one(task_id)
