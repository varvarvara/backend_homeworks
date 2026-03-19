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

task_service = TaskService()
