
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
    id: int
    name: str
    description: str
    datetime: str
    completed: int
