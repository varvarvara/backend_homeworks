from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    complete = "complete"
class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.low)
    due_date: datetime
    completion: bool

class TaskCreate(TaskBase):
    pass
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    completion: Optional[bool] = None
class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskAvatarUploadResponse(BaseModel):
    url: str
