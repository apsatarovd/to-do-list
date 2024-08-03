from fastapi import APIRouter
from app.models import TodoItem
from app.models import datetime
import json
from pydantic import BaseModel

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
def get_all_todos():
    todos = load_todos()
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
def create_todo(request: CreateTodoRequest):
    todos = load_todos()

    created_at = datetime.now()
    updated_at = datetime.now()
    new_id = len(todos) + 1
    new_todo = TodoItem(id=new_id, title=request.title, description=request.description, created_at=created_at, updated_at=updated_at)
    todos.append(new_todo)

    save_todos(todos)
    return {"message": f"Задача с ID {new_id} добавлена в список"}



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



    
