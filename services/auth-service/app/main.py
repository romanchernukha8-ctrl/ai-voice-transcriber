from fastapi import FastAPI
from app.api.v1.auth import router as auth_router

app = FastAPI(
    title="AI Voice Transcriber Auth Service",
    version="0.1.0",
)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "service": "auth-service",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }
