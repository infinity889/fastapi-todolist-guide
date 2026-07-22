from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.categories import router as categories_router
from backend.app.api.tasks import router as tasks_router
from backend.app.db.session import engine
from backend.app.models.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

app.include_router(tasks_router)
app.include_router(categories_router)