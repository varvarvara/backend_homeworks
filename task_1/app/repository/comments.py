from sqlalchemy import select
from app.core.db import SessionLocal
from app.models.comments import Comment
from app.schemas.comments import CommentCreate, CommentResponse

class CommentRepository:
    @classmethod
    async def add_one(cls, task_id: int, data: CommentCreate) -> CommentResponse:
        async with SessionLocal() as session:
            db_comment = Comment(task_id=task_id, text=data.comment)
            session.add(db_comment)
            await session.commit()
            await session.refresh(db_comment)
            return CommentResponse(
                id=db_comment.id,
                task_id=db_comment.task_id,
                comment=db_comment.text,
                created_at=db_comment.created_at,
            )

    @classmethod
    async def find_all_by_task(cls, task_id: int) -> list[CommentResponse]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Comment).where(Comment.task_id == task_id).order_by(Comment.id)
            )
            comments = result.scalars().all()
            return [
                CommentResponse(
                    id=comment.id,
                    task_id=comment.task_id,
                    comment=comment.text,
                    created_at=comment.created_at,
                )
                for comment in comments
            ]

    @classmethod
    async def find_one(cls, task_id: int, comment_id: int) -> CommentResponse | None:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Comment).where(
                    Comment.task_id == task_id,
                    Comment.id == comment_id,
                )
            )
            db_comment = result.scalar_one_or_none()
            if db_comment is None:
                return None

            return CommentResponse(
                id=db_comment.id,
                task_id=db_comment.task_id,
                comment=db_comment.text,
                created_at=db_comment.created_at,
            )

    @classmethod
    async def delete_one(cls, task_id: int, comment_id: int) -> bool:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Comment).where(
                    Comment.task_id == task_id,
                    Comment.id == comment_id,
                )
            )
            db_comment = result.scalar_one_or_none()
            if db_comment is None:
                return False

            await session.delete(db_comment)
            await session.commit()
            return True
