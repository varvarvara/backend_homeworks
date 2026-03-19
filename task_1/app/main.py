from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.tasks import taskRouter
from app.api.users import userRouter
from app.core.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(title="Task Manager API", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API"}


app.include_router(taskRouter)
app.include_router(userRouter)
