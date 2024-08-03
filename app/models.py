from pydantic import BaseModel
from datetime import datetime


class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

