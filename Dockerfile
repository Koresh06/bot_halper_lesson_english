FROM python:3.11.9

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry

# Проверяем установку Poetry
RUN poetry --version

RUN poetry install --no-dev

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Проверяем наличие каталогов и файлов внутри контейнера
RUN ls -l /app
RUN ls -l /app/alembic || echo "Directory /app/alembic does not exist"
RUN cat /app/alembic.ini || echo "File /app/alembic.ini does not exist"

# Применяем миграции Alembic
RUN poetry run alembic --version
RUN poetry run alembic upgrade head

CMD ["poetry", "run", "python", "app/__main__.py"]
