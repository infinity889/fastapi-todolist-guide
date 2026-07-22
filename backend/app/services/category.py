from sqlalchemy.orm import Session

from backend.app.models.task import CategoryORM
from backend.app.repositories.category import CategoryRepository
from backend.app.schemas.schemas import CategoryCreateSchema, CategoryUpdateSchema


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def list_categories(self) -> list[CategoryORM]:
        return self.repository.list()

    def create_category(self, payload: CategoryCreateSchema) -> CategoryORM:
        return self.repository.create(payload.name)

    def update_category(
        self, category_id: str, payload: CategoryUpdateSchema
    ) -> CategoryORM | None:
        category = self.repository.get(category_id)
        if category is None:
            return None
        if payload.name is not None:
            category.name = payload.name
        return self.repository.save(category)

    def delete_category(self, category_id: str) -> bool:
        category = self.repository.get(category_id)
        if category is None:
            return False
        self.repository.delete(category)
        return True