FROM python:3.12-slim

WORKDIR /workspace

RUN pip install --no-cache-dir uv

COPY services/speech-worker/pyproject.toml services/speech-worker/uv.lock ./services/speech-worker/

WORKDIR /workspace/services/speech-worker

RUN uv sync --frozen --no-dev

COPY services/speech-worker/app ./app

CMD ["uv", "run", "--no-dev", "python", "-m", "app.main"]
