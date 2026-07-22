from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.schemas import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema
from backend.app.services.category import CategoryService


router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)


@router.get("", response_model=list[CategorySchema])
def get_categories(service: CategoryService = Depends(get_category_service)):
    return service.list_categories()


@router.post("", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    service: CategoryService = Depends(get_category_service),
):
    return service.create_category(payload)


@router.patch("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    service: CategoryService = Depends(get_category_service),
):
    category = service.update_category(category_id, payload)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", response_model=dict[str, str])
def delete_category(
    category_id: str,
    service: CategoryService = Depends(get_category_service),
):
    if not service.delete_category(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}