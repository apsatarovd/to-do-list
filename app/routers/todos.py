import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models import TodoItem, TodoItemCreate
from app.models import datetime
from app.database import get_db
from app.schemas import TodoSchema

router = APIRouter()


def load_todos():
    with open("storage.json", "r") as file:
        todos_json = json.load(file)
    todos = [TodoItem(**todo_json) for todo_json in todos_json]
    return todos

def save_todos(todos):
    todos_dict = [todo.model_dump() for todo in todos]
    with open("storage.json", "w") as file:
        json.dump(todos_dict, file, indent=2, default=str)

@router.get("/todos")
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoSchema).all()
    return todos

@router.get("/todos/{id}")
def get_todo(id: int):
    todos = load_todos()
    for todo in todos:
        if todo.id == id:
            return todo
    return {"message": f"Задача с id {id} не найдена"}

# Новый POST-запрос, чтобы данные шли от пользователя
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

    return {"message": "success"}



@router.put("/todos/{id}")
def update_todo(id: int, request: CreateTodoRequest):
    todos = load_todos()

    for todo in todos:
        if todo.id == id:
            todo.title = request.title
            todo.description = request.description
            todo.updated_at = datetime.now()

    save_todos(todos)
    return {"message": f"Задача с ID {id} обновлена"}
    

@router.delete("/todos/{id}")
def delete_todo(id: int):
    todos = load_todos()

    for todo in todos:
        if todo.id == id:
            todos.remove(todo)
            save_todos(todos)
            return {"message": f"Задача с ID {id} удалена"}

    return {"message": f"Задача с ID {id} не найдена"}
