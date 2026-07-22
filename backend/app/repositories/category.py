from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.task import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())

    def get(self, category_id: str) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        category = CategoryORM(name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def save(self, category: CategoryORM) -> CategoryORM:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: CategoryORM) -> None:
        self.db.delete(category)
        self.db.commit()