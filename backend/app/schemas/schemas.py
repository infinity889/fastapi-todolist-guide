from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None
