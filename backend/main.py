from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from uuid import uuid4

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, sessionmaker


DATABASE_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid4()))

class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)

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

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TAskCreateSchema(BaseModel):
    title: str

class TAskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


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
    for task in db.scalars(select(TaskORM)).all():
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            db.commit()
            db.refresh(task)
            return task_orm_to_model(task)
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: str, db=Depends(get_db)):
    for task in db.scalars(select(TaskORM)).all():
        if task.id == task_id:
            db.delete(task)
            db.commit()
            return {"message": "Task deleted"}
    return {"error": "Task not found"}


