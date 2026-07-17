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

class TAskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

tasks: list[TaskSchema] = []

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks", response_model=TaskSchema)
def create_task(payload: TAskCreateSchema):
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def update_task(payload: TAskUpdateSchema, task_id: str):
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    return {"error": "Task not found"}


