FROM python:3.11.9

WORKDIR /project

COPY pyproject.toml poetry.lock ./
RUN pip install poetry

# Проверяем установку Poetry
RUN poetry --version

RUN poetry install --no-dev

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Проверяем содержимое директорий
RUN ls -l /app
RUN ls -l /app/alembic

# Применяем миграции Alembic
RUN poetry run alembic upgrade head

CMD ["poetry", "run", "python", "app/__main__.py"]
