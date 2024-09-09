FROM python:3.11.9

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry

# Проверяем установку Poetry
RUN poetry --version

RUN poetry install --no-dev

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"


# Применяем миграции Alembic
RUN alembic upgrade head

CMD ["poetry", "run", "python", "app/__main__.py"]
