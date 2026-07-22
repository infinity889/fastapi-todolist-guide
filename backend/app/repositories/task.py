


from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.task import TaskORM


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[TaskORM]:
        return list(self.db.scalars(select(TaskORM)).all())

    def get(self, task_id: str) -> TaskORM | None:
        return self.db.get(TaskORM, task_id)

    def create(self, title: str) -> TaskORM:
        task = TaskORM(title=title, completed=False)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def save(self, task: TaskORM) -> TaskORM:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: TaskORM) -> None:
        self.db.delete(task)
        self.db.commit()

