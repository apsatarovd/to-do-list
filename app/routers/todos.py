
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import TodoItem, TodoItemCreate
from app.models import datetime
from app.database import get_db
from app.schemas import TodoSchema

router = APIRouter()


@router.get("/todos")
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoSchema).all()
    return todos

@router.get("/todos/{id}")
def get_todo(id: int ,db: Session = Depends(get_db)):
    todo = db.query(TodoSchema).filter_by(id=id).first()
    if todo:
        return todo
    
    return {"message": f"Задача с id {id} не найдена"}


class CreateTodoRequest(BaseModel):
    title: str
    description: str

@router.post("/todos")
def create_todo(request: CreateTodoRequest, db: Session = Depends(get_db)):
    now = datetime.now()

    todo = TodoSchema(
        title=request.title,
        description=request.description,
        created_at=now,
        updated_at=now,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    todo = db.query(TodoSchema).filter_by(created_at=now).first()
    return {"message": f"Задача с ID {todo.id} добавлена"}


@router.put("/todos/{id}")
def update_todo(id: int, request: CreateTodoRequest, db: Session = Depends(get_db)):
    todo = db.query(TodoSchema).filter_by(id=id).first()
    now = datetime.now()
   
    if todo == None:
            return  {"message": f"Задача с ID {id} не найдена!"}

    todo.title = request.title
    todo.description = request.description
    todo.updated_at = now
    
    db.commit()
    db.refresh(todo)
    return {"message": f"Задача с ID {id} обновлена"}
    

@router.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoSchema).filter_by(id=id).first()
        
    if todo == None:
        return  {"message": f"Задача с ID {id} не найдена!"}
    db.add(todo)  
    db.delete(todo)
    db.commit()

    return {"message": f"Задача с ID {id} удалена"}
    
    
