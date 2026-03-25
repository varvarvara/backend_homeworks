from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.comments import commentRouter
from app.api.tasks import taskRouter
from app.api.users import userRouter
from app.core.db import create_tables
from app.core.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(title="Task Manager API", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API"}


register_exception_handlers(app)

app.include_router(taskRouter, prefix="/v1")
app.include_router(commentRouter, prefix="/v1")
app.include_router(userRouter, prefix="/v1")
