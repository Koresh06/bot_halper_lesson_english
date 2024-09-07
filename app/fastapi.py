from fastapi import FastAPI
from app.tgbot.api.router import router as lessons_router
from app.tgbot.config import configure_static

app = FastAPI()

configure_static(app)

# Включение роутеров FastAPI
app.include_router(lessons_router)
