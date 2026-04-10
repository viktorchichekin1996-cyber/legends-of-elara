from fastapi import FastAPI
from app.config import settings
from sqlalchemy import text
from app.db.session import engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url=None
)

@app.get("/health")
async def health_check():
    """Проверка здоровья сервера и базы данных."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected", "api": "running"}
    except Exception as e:
        return {"status": "error", "db": "disconnected", "detail": str(e)}

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}