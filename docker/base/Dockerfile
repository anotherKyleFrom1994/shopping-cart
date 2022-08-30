FROM python:3.7-slim as base-runtime

RUN pip install poetry

WORKDIR /home/app
COPY ["./pyproject.toml", "./poetry.lock", "./"]

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
