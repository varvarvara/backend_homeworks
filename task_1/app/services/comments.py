from app.core.exceptions import CommentNotFoundException, TaskNotFoundException
from app.repository.comments import CommentRepository
from app.repository.tasks import TaskRepository
from app.schemas.comments import CommentCreate, CommentResponse


class CommentService:
    @classmethod
    async def create_comment(cls, task_id: int, data: CommentCreate) -> CommentResponse:
        task = await TaskRepository.find_one(task_id)
        if task is None:
            raise TaskNotFoundException(task_id)

        return await CommentRepository.add_one(task_id, data)

    @classmethod
    async def get_task_comments(cls, task_id: int) -> list[CommentResponse]:
        task = await TaskRepository.find_one(task_id)
        if task is None:
            raise TaskNotFoundException(task_id)

        return await CommentRepository.find_all_by_task(task_id)

    @classmethod
    async def get_comment(cls, task_id: int, comment_id: int) -> CommentResponse:
        task = await TaskRepository.find_one(task_id)
        if task is None:
            raise TaskNotFoundException(task_id)

        comment = await CommentRepository.find_one(task_id, comment_id)
        if comment is None:
            raise CommentNotFoundException(comment_id)
        return comment


comment_service = CommentService()
