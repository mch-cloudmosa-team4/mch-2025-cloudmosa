#!/bin/bash

# Production deployment script for Ubuntu server
# 請以 root 或有 sudo 權限的用戶運行此腳本

set -e

echo "🚀 開始部署 MCH Backend 到生產環境..."

# 設定變數
PROJECT_DIR="/opt/mch-backend"
SERVICE_USER="ubuntu"
DOMAIN="hackathon-7h5wir.puffin.app"  # 請替換為你的域名

# 檢查是否為 root 用戶
if [ "$EUID" -ne 0 ]; then
    echo "請以 root 用戶運行此腳本"
    exit 1
fi

# 更新系統
echo "📦 更新系統套件..."
apt update && apt upgrade -y

# 安裝必要套件
echo "🔧 安裝必要套件..."
apt install -y \
    curl \
    git \
    ufw \
    fail2ban \
    docker.io \
    docker-compose \

# 啟動並啟用 Docker
systemctl start docker
systemctl enable docker

# 創建服務用戶
echo "👤 創建服務用戶..."
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --shell /bin/bash --home-dir /home/$SERVICE_USER --create-home $SERVICE_USER
    usermod -aG docker $SERVICE_USER
fi

# 創建項目目錄
echo "📁 設置項目目錄..."
mkdir -p $PROJECT_DIR
chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# 克隆或更新代碼庫
echo "📥 設置代碼庫..."
if [ ! -d "$PROJECT_DIR/.git" ]; then
    sudo -u $SERVICE_USER git clone https://github.com/Sean20405/mch-2025-cloudmosa.git $PROJECT_DIR
else
    cd $PROJECT_DIR
    sudo -u $SERVICE_USER git pull origin main
fi

# 設置環境變數文件
echo "⚙️  設置環境變數..."
cat > $PROJECT_DIR/.env << EOF
# 資料庫設定
POSTGRES_PASSWORD=$(openssl rand -base64 32)

# MinIO 設定
MINIO_ACCESS_KEY=$(openssl rand -base64 12)
MINIO_SECRET_KEY=$(openssl rand -base64 32)

# 其他設定
DOMAIN=$DOMAIN
EOF

chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR/.env
chmod 600 $PROJECT_DIR/.env

# 設置防火牆
echo "🔒 設置防火牆..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 設置 fail2ban
echo "🛡️  設置 fail2ban..."
systemctl start fail2ban
systemctl enable fail2ban

# 注意: Nginx 已被移除，請確保你的前端服務器有以下配置：
# - 反向代理到 localhost:8000 (FastAPI)
# - 反向代理到 localhost:9000 (MinIO)
# - 反向代理到 localhost:9001 (MinIO Console)
echo "📝 Nginx 已移除，請在你的前端服務器配置反向代理"

# 啟動服務
echo "🚀 啟動服務..."
cd $PROJECT_DIR/backend
sudo -u $SERVICE_USER docker-compose -f docker-compose.prod.yml up -d

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 30

# 運行資料庫遷移
echo "🗄️  運行資料庫遷移..."
sudo -u $SERVICE_USER docker-compose -f docker-compose.prod.yml exec -T backend uv run alembic upgrade head


# 健康檢查
echo "🏥 執行健康檢查..."
if curl -f http://localhost:8000/api/v1/health; then
    echo "✅ 部署成功！"
    echo "🌐 FastAPI 運行在: http://localhost:8000"
    echo "📊 MinIO API: http://localhost:9000"
    echo "📊 MinIO 控制台: http://localhost:9001"
    echo "⚠️  請在你的前端服務器配置反向代理到這些端口"
else
    echo "❌ 健康檢查失敗，請檢查日誌"
    exit 1
fi

# 設置自動更新腳本
cat > /etc/cron.d/mch-backend-update << EOF
# 每天凌晨 2 點自動更新
0 2 * * * $SERVICE_USER cd $PROJECT_DIR && git pull origin main && docker-compose -f backend/docker-compose.prod.yml up -d
EOF

echo "
🎉 部署完成！

下一步:
1. 設定你的域名 DNS 指向此服務器的 IP
2. 在 GitHub repository 中設定以下 Secrets:
   - SERVER_HOST: 你的服務器 IP
   - SERVER_USER: $SERVICE_USER
   - SERVER_SSH_KEY: SSH 私鑰
   - POSTGRES_PASSWORD: 從 $PROJECT_DIR/.env 複製
   - MINIO_ACCESS_KEY: 從 $PROJECT_DIR/.env 複製
   - MINIO_SECRET_KEY: 從 $PROJECT_DIR/.env 複製
3. 推送代碼到 main 分支即可自動部署

環境變數文件位置: $PROJECT_DIR/.env
日誌查看: docker-compose -f $PROJECT_DIR/backend/docker-compose.prod.yml logs -f
"
