from sqlalchemy.orm import Session

from backend.app.models.task import TaskORM
from backend.app.repositories.task import TaskRepository
from backend.app.schemas.schemas import TaskCreateSchema, TaskUpdateSchema


class TaskService:
    def __init__(self, db: Session):
        self.repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskORM]:
        return self.repository.list()

    def create_task(self, payload: TaskCreateSchema) -> TaskORM:
        return self.repository.create(payload.title)

    def update_task(self, task_id: str, payload: TaskUpdateSchema) -> TaskORM | None:
        task = self.repository.get(task_id)
        if task is None:
            return None
        if payload.title is not None:
            task.title = payload.title
        if payload.completed is not None:
            task.completed = payload.completed
        return self.repository.save(task)

    def delete_task(self, task_id: str) -> bool:
        task = self.repository.get(task_id)
        if task is None:
            return False
        self.repository.delete(task)
        return True