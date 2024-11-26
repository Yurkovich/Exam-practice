
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TaskRead(BaseModel):
    id: int
    name: str
    description: str
    datetime: datetime
    completed: int


class TaskCreate(BaseModel):
    name: str
    description: str
    datetime: datetime
    completed: int = 0


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    datetime: Optional[str] = None
    completed: Optional[int] = None
    