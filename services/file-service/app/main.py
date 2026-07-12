from fastapi import FastAPI

from app.api.v1.files import router as files_router

app = FastAPI(
    title="AI Voice Transcriber File Service",
    version="0.1.0",
)

app.include_router(files_router)


@app.get("/")
async def root():
    return {
        "service": "file-service",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }