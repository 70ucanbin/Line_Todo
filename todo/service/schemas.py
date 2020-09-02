from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class Task(TaskBase):
    id: int
    time_limit: datetime
    to_user: str
    details: str
    by_user: str
    class Config:
        orm_mode = True

class TaskCreate(Task):
    pass