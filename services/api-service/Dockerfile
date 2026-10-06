FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY services/api-service/pyproject.toml services/api-service/uv.lock ./

RUN uv sync --frozen --no-dev

COPY services/api-service/app ./app

CMD ["uv", "run", "--no-dev", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
