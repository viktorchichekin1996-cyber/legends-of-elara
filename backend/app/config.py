from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legends of Elara"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7
    VK_APP_ID: str
    VK_APP_SECRET: str
    YANDEX_API_KEY: str
    YANDEX_FOLDER_ID: str
    API_DOMAIN: str = "api.chichekin-tech.ru"
    APP_DOMAIN: str = "app.chichekin-tech.ru"
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
