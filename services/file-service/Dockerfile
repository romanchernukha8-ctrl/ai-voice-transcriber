FROM python:3.12-slim

WORKDIR /workspace

RUN pip install --no-cache-dir uv

COPY shared ./shared
COPY services/file-service/pyproject.toml services/file-service/uv.lock ./services/file-service/

WORKDIR /workspace/services/file-service

RUN uv sync --frozen --no-dev

COPY services/file-service/app ./app
COPY services/file-service/alembic.ini ./alembic.ini
COPY services/file-service/alembic ./alembic

CMD ["uv", "run", "--no-dev", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
