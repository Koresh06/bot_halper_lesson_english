FROM python:3.11.9

WORKDIR /app

# Копируем только файлы, необходимые для миграций
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry install --no-dev

# Копируем все файлы приложения
COPY . .

# Убедитесь, что alembic доступен
RUN poetry run alembic --version

# Команда по умолчанию (она переопределяется в docker-compose.yml)
CMD ["poetry", "run", "alembic", "upgrade", "head"]
