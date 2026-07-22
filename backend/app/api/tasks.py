from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.schemas import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from backend.app.services.task import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)


@router.get("", response_model=list[TaskSchema])
def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.list_tasks()


@router.post("", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema,
    service: TaskService = Depends(get_task_service),
):
    return service.create_task(payload)


@router.patch("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    service: TaskService = Depends(get_task_service),
):
    task = service.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", response_model=dict[str, str])
def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}