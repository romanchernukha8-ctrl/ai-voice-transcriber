from fastapi import FastAPI
from pydantic import BaseModel

from app.config import settings
from app.ollama_client import OllamaClient


app = FastAPI(
    title="AI Worker",
    version="1.0.0",
)

ollama = OllamaClient(
    base_url=settings.ollama_url,
    model=settings.ollama_model,
)


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def generate(request: GenerateRequest):
    result = ollama.generate(request.prompt)

    return {
        "response": result,
    }
