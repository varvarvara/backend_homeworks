from fastapi import APIRouter

from app.schemas.comments import CommentCreate, CommentResponse
from app.services.comments import CommentService

commentRouter = APIRouter(prefix="/v1/tasks/{task_id}/comments", tags=["Comments"])
comment_service = CommentService()

@commentRouter.post("", response_model=CommentResponse, status_code=201)
async def create_comment(task_id: int, payload: CommentCreate):
    return await comment_service.create_comment(task_id, payload)


@commentRouter.get("", response_model=list[CommentResponse], status_code=200)
async def get_task_comments(task_id: int):
    return await comment_service.get_task_comments(task_id)


@commentRouter.get("/{comment_id}", response_model=CommentResponse, status_code=200)
async def get_comment(task_id: int, comment_id: int):
    return await comment_service.get_comment(task_id, comment_id)
