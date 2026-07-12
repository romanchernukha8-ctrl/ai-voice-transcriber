from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from fastapi.security import HTTPBearer

security = HTTPBearer()

app = FastAPI(
    title="AI Voice Transcriber Auth Service",
    version="0.1.0",
    swagger_ui_parameters={
        "persistAuthentication": "true",
    },
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
