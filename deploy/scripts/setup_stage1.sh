#!/usr/bin/env bash
set -euo pipefail

echo "🚀 ЭТАП 1: Подготовка инфраструктуры и окружения"
echo "=============================================="

# ==========================================
# 📦 ПОДЭТАП 1.1: Сервер и безопасность
# ==========================================
echo "📦 [1.1] Обновление системы и настройка безопасности..."
export DEBIAN_FRONTEND=noninteractive
apt update -y && apt upgrade -y -q

# 1. Создание пользователя deploy
echo "👤 Создание пользователя deploy..."
if ! id -u deploy &>/dev/null; then
    useradd -m -s /bin/bash deploy
    usermod -aG sudo deploy
    echo "   Пользователь deploy создан и добавлен в sudo."
else
    echo "   Пользователь deploy уже существует."
fi

# 2. Настройка UFW
echo "🛡️ Настройка Firewall (UFW)..."
apt install -y ufw > /dev/null 2>&1
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
if ! ufw status | grep -q "Status: active"; then
    echo "y" | ufw enable
    echo "   UFW включён. Открыты порты: 22, 80, 443."
else
    echo "   UFW уже активен."
fi

# 3. Настройка SSH (вход по паролю разрешён)
echo "🔐 Настройка SSH (сохранён вход по паролю)..."
mkdir -p /etc/ssh/sshd_config.d
cat > /etc/ssh/sshd_config.d/99-auth-password.conf <<'EOF'
PermitRootLogin yes
PasswordAuthentication yes
PubkeyAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
EOF
systemctl restart sshd
echo "   SSH настроен: вход по паролю разрешён для root и всех пользователей."

echo "✅ Подэтап 1.1 завершён."

# ==========================================
# 🐳 ПОДЭТАП 1.2: Docker и Docker Compose
# ==========================================
echo "🐳 [1.2] Установка Docker и Docker Compose..."

echo "📦 Установка зависимостей..."
apt install -y ca-certificates curl gnupg > /dev/null 2>&1

echo "🔑 Добавление GPG ключа Docker..."
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "📂 Настройка репозитория Docker..."
CODENAME=$(. /etc/os-release && echo "$VERSION_CODENAME")
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $CODENAME stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "🐋 Установка Docker Engine и Docker Compose Plugin..."
apt update -y > /dev/null 2>&1
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin > /dev/null 2>&1

systemctl enable --now docker
echo "   Docker сервис запущен и добавлен в автозагрузку."

echo "🧪 Тестовый запуск контейнера..."
if docker run --rm hello-world > /dev/null 2>&1; then
    echo "   ✅ Docker работает корректно."
else
    echo "   ⚠️  Проверьте лог: journalctl -u docker"
fi

usermod -aG docker deploy
echo "   Пользователь deploy добавлен в группу docker."

echo "✅ Подэтап 1.2 завершён."
echo "=============================================="
echo "🎉 ЭТАП 1 успешно выполнен!"
echo "💡 Примечание: Для применения прав группы docker к пользователю deploy потребуется перелогиниться в сервер."