FROM python:3.12-slim

WORKDIR /workspace

RUN pip install --no-cache-dir uv

COPY shared ./shared
COPY services/auth-service/pyproject.toml services/auth-service/uv.lock ./services/auth-service/

WORKDIR /workspace/services/auth-service

RUN uv sync --frozen --no-dev

COPY services/auth-service/app ./app
COPY services/auth-service/alembic.ini ./alembic.ini
COPY services/auth-service/alembic ./alembic

CMD ["uv", "run", "--no-dev", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
