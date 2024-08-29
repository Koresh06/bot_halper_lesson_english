from environs import Env

env = Env()
env.read_env()


class TgBot:
    token = env('BOT_TOKEN')



class DbConfig:
    user: str = env("DB_USER")
    password: str = env("DB_PASSWORD")
    host: str = env("DB_HOST")
    port: str = env("DB_PORT")
    name: str = env("DB_NAME")
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings:
    bot = TgBot()
    db = DbConfig()


settings = Settings()