FROM python:3.11.9

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry

# Проверяем установку Poetry
RUN poetry --version

RUN poetry install --no-dev

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Проверяем наличие файлов и каталогов
RUN ls -l /app
RUN ls -l /app/alembic || echo "Directory /app/alembic does not exist"
RUN cat /app/alembic.ini || echo "File /app/alembic.ini does not exist"

# Проверяем версию alembic
RUN poetry run alembic --version

# Установите ENTRYPOINT для контейнера, чтобы можно было переопределять команды в docker-compose.yml
ENTRYPOINT ["poetry", "run"]
