# Используем базовый образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей (Poetry для управления зависимостями)
COPY poetry.lock pyproject.toml /app/

# Устанавливаем Poetry и зависимости
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Копируем все файлы проекта в контейнер
COPY . /app


# Открываем порт для FastAPI
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "-m", "app.__main__"]
