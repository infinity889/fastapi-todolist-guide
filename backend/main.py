from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TAskCreateSchema(BaseModel):
    title: str


tasks: list[TaskSchema] = []

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: TAskCreateSchema):
    new_task = TaskSchema(id=str(uuid4()), title=task.title, completed=False)
    tasks.append(new_task)
    return new_task




