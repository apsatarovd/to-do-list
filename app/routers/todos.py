from fastapi import APIRouter
from app.models import TodoItem
from app.models import datetime
import json
from pydantic import BaseModel
router = APIRouter()


@router.get("/todos")
def get_all_todos():
    with open("storage.json", "r") as file:
        todos_json = json.load(file)
    todos = []
    for todo_json in todos_json:
        todo = TodoItem(**todo_json)
        todos.append(todo)
    return todos

@router.get("/todos/{id}")
def get_todo(id: int):
    with open("storage.json", "r") as file:
        todos_json = json.load(file)
    todos = []
    for todo_json in todos_json:
        todo = TodoItem(**todo_json)
        todos.append(todo)
    for todo in todos:
        if todo.id == id:
            return todo
    return {"message": f"Задача с id {id} не найдена"}



#новый post запрос чтобы данные шли от пользователя 
class CreateTodoRequest(BaseModel):
    title: str
    description: str


@router.post("/todos")
def create_todo(request:CreateTodoRequest):
    with open("storage.json", "r") as file:
        todos_json = json.load(file)
    todos = []
    for todo_json in todos_json:
        todo = TodoItem(**todo_json)
        todos.append(todo)

    created_at = datetime.now()
    updated_at = datetime.now()
    new_id = len(todos) + 1
    new_todo = TodoItem(id=new_id, title=request.title, description=request.description, created_at=created_at, updated_at=updated_at)
    todos.append(new_todo)

   
    todos_dict = []
    for todo in todos:
        todo_dict = todo.model_dump()
        todos_dict.append(todo_dict)

    with open("storage.json", "w") as file:
        json.dump(todos_dict, file, indent=2, default=str)

    return {"message": f"Задача с ID {new_id} добавлена в список"}

"-----------------------------------------------------------------------------------------------------------------------------------------------"


@router.put("/todos/{id}")
def update_todo(id: int, request: CreateTodoRequest):
    with open("storage.json", "r") as file:
        todos_json = json.load(file)

    for todo in todos_json:
        if todo["id"] == id:
            todo["title"] = request.title
            todo["description"] = request.description
            todo["updated_at"] = str(datetime.now())
            

    with open("storage.json", "w") as file:
        json.dump(todos_json, file, indent=2, default=str)
    return {"message": f"Задача с ID {id} обновлена"}




@router.delete("/todos/{id}")
def delete_todo(id: int):
    with open("storage.json", "r") as file:
        todos_json = json.load(file)
    todos = []
    for todo_json in todos_json:
        todo = TodoItem(**todo_json)
        todos.append(todo)

    for todo in todos:
        if todo.id == id:
            todos.remove(todo)
            todos_dict = []
            for todo in todos:
                todo_dict = todo.model_dump()
                todos_dict.append(todo_dict)

            with open("storage.json", "w") as file:
                json.dump(todos_dict, file, indent=2, default=str)
            return {"message": f"Задача с ID {id} удалена"}
    
    return {"message": f"Задача с ID {id} не найдена"}



    
