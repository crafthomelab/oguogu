FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY src ./src

EXPOSE 8000

ENTRYPOINT ["python", "-m", "uvicorn", "src.app:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
