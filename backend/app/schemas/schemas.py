from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TAskCreateSchema(BaseModel):
    title: str

class TAskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class CategorySchema(BaseModel):
    id: str
    name: str

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None
