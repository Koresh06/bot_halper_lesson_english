from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles



# Настраиваем пути к шаблонам
templates = Jinja2Templates(directory="app/tgbot/templates")


# Функция для настройки статики
def configure_static(app):
    app.mount("/static", StaticFiles(directory="app/app/tgbot/static"), name="static")