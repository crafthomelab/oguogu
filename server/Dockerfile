FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app /app

CMD ["poetry", "run", "fastapi", "run", "main.py"]