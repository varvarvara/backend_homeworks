from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.comments import commentRouter
from app.api.tasks import taskRouter
from app.api.users import userRouter
from app.core.adapters import get_storage_adapter
from app.core.config import settings
from app.core.db import create_tables, engine
from app.core.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(title="Task Manager API", lifespan=lifespan)
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Task Manager API"}


@app.get("/health")
async def health():
    checks = {
        "database": {"status": "ok"},
        "minio": {"status": "ok"},
    }

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception as exc:
        checks["database"] = {"status": "error", "detail": str(exc)}

    try:
        storage = get_storage_adapter()
        await storage.check()
    except Exception as exc:
        checks["minio"] = {"status": "error", "detail": str(exc)}

    is_ok = all(item["status"] == "ok" for item in checks.values())
    response = {"status": "ok" if is_ok else "degraded", "checks": checks}
    return JSONResponse(status_code=200 if is_ok else 503, content=response)


@app.get("/info")
async def info():
    return {
        "service": "Task Manager API",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


app.include_router(taskRouter)
app.include_router(userRouter)
app.include_router(commentRouter)
