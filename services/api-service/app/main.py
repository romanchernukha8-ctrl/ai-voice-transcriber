from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.config import settings
from app.api.v1.database import router as database_router


app = FastAPI(
    title=settings.project_name,
    version=settings.version,
)

app.include_router(health_router)
app.include_router(database_router)


@app.get("/")
async def root():
    return {
        "service": settings.project_name,
        "version": settings.version,
        "status": "running",
    }
