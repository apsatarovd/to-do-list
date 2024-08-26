from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class TodoSchema(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
class CreateTodoRequest(BaseModel):
    title: str
    description: str