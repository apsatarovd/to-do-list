from fastapi import FastAPI
from app.routers.todos import router
app = FastAPI()

@app.get("/")
def welcome():
    return "Welcome to To-Do List API!"

app.include_router(router)