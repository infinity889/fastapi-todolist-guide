
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)

class CategoryORM(Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(nullable=False)
