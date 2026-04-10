#!/usr/bin/env bash
set -euo pipefail

echo "📂 Подэтап 1.3: Создание структуры репозитория"
echo "=================================================="

# 1. Инициализация Git
echo "🔧 Инициализация Git репозитория..."
if [ ! -d ".git" ]; then
    git init
    echo "   Репозиторий инициализирован."
else
    echo "   Git уже инициализирован."
fi

# 2. Создание структуры папок (согласно Структура проекта.txt)
echo "📁 Создание структуры папок..."
mkdir -p backend frontend nginx deploy/scripts docs

# Пустые маркеры для Git
touch backend/.gitkeep frontend/.gitkeep nginx/.gitkeep deploy/.gitkeep docs/.gitkeep
echo "   Структура папок создана."

# 3. Создание .gitignore
echo "🙈 Создание .gitignore..."
cat > .gitignore <<'EOF'
# --- Секреты и переменные окружения ---
.env
.env.*.local
.env.production
*.pem
*.key

# --- Python (Backend) ---
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/
.mypy_cache/
.pytest_cache/
.venv/
venv/
env/

# --- Node.js / React / Vite (Frontend) ---
frontend/node_modules/
frontend/dist/
frontend/.vite/
frontend/tsconfig.tsbuildinfo

# --- Docker ---
.docker/
docker-compose.override.yml
deploy/backups/

# --- IDE ---
.vscode/
.idea/
*.swp
*.swo
*~

# --- OS ---
.DS_Store
Thumbs.db

# --- Logs ---
*.log
logs/
EOF
echo "   .gitignore настроен."

# 4. Создание .env.example
echo "📝 Создание .env.example..."
cat > .env.example <<'EOF'
# Общие
PROJECT_NAME=legends-of-elara
ENVIRONMENT=development

# База данных
POSTGRES_USER=elara_user
POSTGRES_PASSWORD=change_me_strong_password
POSTGRES_DB=elara_db
DATABASE_URL=postgresql+asyncpg://elara_user:change_me_strong_password@postgres:5432/elara_db

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET_KEY=change_me_to_64_random_chars_or_more
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7

# VK Mini App
VK_APP_ID=your_vk_app_id
VK_APP_SECRET=your_vk_app_secret

# Yandex Cloud
YANDEX_API_KEY=your_yandex_cloud_api_key
YANDEX_FOLDER_ID=your_yandex_folder_id

# Домены
API_DOMAIN=api.chichekin-tech.ru
APP_DOMAIN=app.chichekin-tech.ru
FRONTEND_URL=http://localhost:5173
EOF
echo "   .env.example создан."

# 5. Создание базового README.md
echo "📖 Создание README.md..."
cat > README.md <<'EOF'
# 🐉 Легенды Элары
Браузерная текстовая RPG с ИИ-генерацией событий, интегрированная с VK Mini Apps.

## 🚀 Быстрый старт
1. `cp .env.example .env` и заполните секреты.
2. `docker compose up -d --build`
3. Backend Swagger: `http://localhost:8000/docs`
4. Frontend (dev): `cd frontend && npm run dev`

## 🛠️ Стек
Python 3.11 | FastAPI | SQLAlchemy 2.0 | PostgreSQL 15 | Redis 7 | React 18 | VKUI | Docker Compose
EOF
echo "   README.md создан."

# 6. Первый коммит
echo "💾 Фиксация начальной структуры..."
git add .
git commit -m "chore: init project structure, gitignore, env template" || echo "   ⚠️  Нечего коммитить."

echo "=================================================="
echo "✅ Подэтап 1.3 успешно выполнен!"
echo "📂 Структура проекта готова к разработке."