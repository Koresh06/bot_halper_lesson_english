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

# Экспортируем переменные среды (на случай если будет нужна база данных)
ENV BOT_TOKEN=${BOT_TOKEN}
ENV ADMIN_ID=${ADMIN_ID}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_NAME=${DB_NAME}
ENV API_HOST=${API_HOST}
ENV API_PORT=${API_PORT}
ENV WEB_SERVER_ADMIN=${WEB_SERVER_ADMIN}

# Открываем порт для FastAPI
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "-m", "app.__main__"]
