from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    comment: str = Field(min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    created_at: datetime
