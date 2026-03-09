from sqlalchemy import select

from app.db.db import SessionLocal, TaskOrm
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse


class TaskRepository:
    @classmethod
    async def add_one(cls, data: TaskCreate) -> TaskResponse:
        async with SessionLocal() as session:
            task = TaskOrm(**data.model_dump())
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return TaskResponse.model_validate(task, from_attributes=True)

    @classmethod
    async def find_all(cls) -> list[TaskResponse]:
        async with SessionLocal() as session:
            result = await session.execute(select(TaskOrm))
            tasks = result.scalars().all()
            return [TaskResponse.model_validate(task, from_attributes=True) for task in tasks]

    @classmethod
    async def find_one(cls, task_id: int) -> TaskResponse | None:
        async with SessionLocal() as session:
            result = await session.execute(select(TaskOrm).where(TaskOrm.id == task_id))
            task = result.scalar_one_or_none()
            if task is None:
                return None
            return TaskResponse.model_validate(task, from_attributes=True)

    @classmethod
    async def update_one(cls, task_id: int, data: TaskUpdate) -> TaskResponse | None:
        async with SessionLocal() as session:
            result = await session.execute(select(TaskOrm).where(TaskOrm.id == task_id))
            task = result.scalar_one_or_none()
            if task is None:
                return None

            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(task, key, value)

            await session.commit()
            await session.refresh(task)
            return TaskResponse.model_validate(task, from_attributes=True)

    @classmethod
    async def delete_one(cls, task_id: int) -> bool:
        async with SessionLocal() as session:
            result = await session.execute(select(TaskOrm).where(TaskOrm.id == task_id))
            task = result.scalar_one_or_none()
            if task is None:
                return False

            await session.delete(task)
            await session.commit()
            return True
