FROM python:3.12-slim AS base

ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

WORKDIR /app
COPY backend /app
RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-root

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
