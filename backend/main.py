from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select

from app.db.session import engine, get_db
from app.models.base import Base
from app.models.task import TaskORM, CategoryORM

from app.schemas.schemas import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

@app.get("/tasks")
def get_tasks(db=Depends(get_db)):
    db_tasks =db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in db_tasks]

@app.post("/tasks", response_model=TaskSchema)
def create_task(payload: TAskCreateSchema, db=Depends(get_db)):
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def update_task(payload: TAskUpdateSchema, task_id: str, db=Depends(get_db)):
    task_for_update = db.get(TaskORM, task_id)
    if task_for_update:
        if payload.title is not None:
            task_for_update.title = payload.title
        if payload.completed is not None:
            task_for_update.completed = payload.completed
        db.commit()
        db.refresh(task_for_update)
        return task_orm_to_model(task_for_update)
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str, db=Depends(get_db)):
    task_to_delete = db.get(TaskORM, task_id)
    if task_to_delete:
        db.delete(task_to_delete)
        db.commit()
        return {"message": "Task deleted"}
    return {"error": "Task not found"}


@app.get("/categories")
def get_categories(db=Depends(get_db)):
    db_categories = db.scalars(select(CategoryORM)).all()
    return [CategorySchema(id=category.id, name=category.name) for category in db_categories]

@app.post("/categories")
def create_category(payload: CategoryCreateSchema, db=Depends(get_db)):
    new_category = CategoryORM(name=payload.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return CategorySchema(id=new_category.id, name=new_category.name)

@app.patch("/categories/{category_id}")
def update_category(payload: CategoryUpdateSchema, category_id: str, db=Depends(get_db)):
    category_for_update = db.get(CategoryORM, category_id)
    if category_for_update:
        if payload.name is not None:
            category_for_update.name = payload.name
        db.commit()
        db.refresh(category_for_update)
        return CategorySchema(id=category_for_update.id, name=category_for_update.name)
    return {"error": "Category not found"}

@app.delete("/categories/{category_id}")
def delete_category(category_id: str, db=Depends(get_db)):
    category_to_delete = db.get(CategoryORM, category_id)
    if category_to_delete:
        db.delete(category_to_delete)
        db.commit()
        return {"message": "Category deleted"}
    return {"error": "Category not found"}