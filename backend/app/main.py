from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.router import api_router
from sqlalchemy import text
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

# CORS Middleware (разрешаем VK и фронтенд)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "https://vk.com", "https://*.vk.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    print(f"{request.method} {request.url.path} -> {response.status_code}")
    return response

# Глобальный обработчик исключений
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# Подключение API роутеров (ЗДЕСЬ ОШИБКА БЫЛА РАНЕЕ: роутер не был подключен)
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected", "api": "running"}
    except Exception as e:
        return {"status": "error", "db": "disconnected", "detail": str(e)}
