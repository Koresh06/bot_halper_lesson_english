# Используем официальный образ Python
FROM python:3.11.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости из poetry.lock и pyproject.toml
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости
RUN poetry install --no-dev

# Копируем файлы проекта
COPY . .

# Экспортируем переменные среды
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Применяем миграции Alembic перед запуском
RUN poetry run alembic upgrade head

# Команда для запуска FastAPI и бота
CMD ["poetry", "run", "python", "app/__main__.py"]
