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

# 檢查是否需要重啟
if [ -f /var/run/reboot-required ]; then
    echo "⚠️  系統更新需要重啟才能生效"
    echo "建議執行: sudo reboot"
    echo "重啟後再次運行此腳本繼續安裝"
    read -p "是否現在重啟？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔄 正在重啟系統..."
        reboot
        exit 0
    else
        echo "⏭️  跳過重啟，繼續安裝 (可能會有警告)"
    fi
fi

# 安裝必要套件
echo "🔧 安裝必要套件..."

# 先安裝基本套件
apt install -y \
    curl \
    git \
    ufw \
    fail2ban \
    ca-certificates \
    gnupg \
    lsb-release

# 處理 Docker 安裝 (解決 containerd 衝突)
echo "🐳 安裝 Docker..."

# 移除可能衝突的舊版本
apt remove -y docker docker-engine docker.io containerd runc || true

# 添加 Docker 官方 GPG 金鑰
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 添加 Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新套件清單並安裝 Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 安裝 docker-compose (standalone)
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

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
    sudo -u $SERVICE_USER git clone git@github.com:mch-cloudmosa-team4/mch-2025-cloudmosa.git -b feat/cicd $PROJECT_DIR
else
    cd $PROJECT_DIR
    sudo -u $SERVICE_USER git pull origin main
fi

# 設置環境變數文件
echo "⚙️  設置環境變數..."

# 檢測 GitHub repository 名稱
REPO_URL=$(cd $PROJECT_DIR && git remote get-url origin)
if [[ $REPO_URL == *"github.com"* ]]; then
    # 從 git remote URL 提取 repository 名稱
    GITHUB_REPO=$(echo $REPO_URL | sed 's/.*github\.com[:/]\([^/]*\/[^/]*\)\.git.*/\1/' | sed 's/\.git$//')
else
    # 如果無法檢測，使用預設值
    GITHUB_REPO="your-username/mch-2025-cloudmosa"
fi

# 生成隨機密碼
POSTGRES_PASS=$(openssl rand -base64 32)
MINIO_ACCESS=$(openssl rand -base64 12) 
MINIO_SECRET=$(openssl rand -base64 32)

cat > $PROJECT_DIR/.env << EOF
# Docker Compose 環境變數 (用於容器編排)
GITHUB_REPOSITORY=${GITHUB_REPO}
POSTGRES_PASSWORD=${POSTGRES_PASS}
MINIO_ACCESS_KEY=${MINIO_ACCESS}
MINIO_SECRET_KEY=${MINIO_SECRET}
EOF

# 為應用程式創建單獨的配置文件
cat > $PROJECT_DIR/backend/.env << EOF
# FastAPI 應用程式環境變數
DATABASE_URL=postgresql://backend_user:${POSTGRES_PASS}@postgres:5432/backend_db
DATABASE_ECHO=false
DATABASE_AUTO_CREATE=false
DEBUG=false
POSTGRES_PASSWORD=${POSTGRES_PASS}
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=${MINIO_ACCESS}
MINIO_SECRET_KEY=${MINIO_SECRET}
MINIO_SECURE=false
MINIO_BUCKET=files
SECRET_KEY=$(openssl rand -base64 32)
EOF

chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR/.env
chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR/backend/.env
chmod 600 $PROJECT_DIR/.env
chmod 600 $PROJECT_DIR/backend/.env

# 設置防火牆
echo "🔒 設置防火牆..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 5173/tcp
ufw --force enable

# 設置 fail2ban
echo "🛡️  設置 fail2ban..."
systemctl start fail2ban
systemctl enable fail2ban

# 啟動服務
echo "🚀 啟動服務..."
cd $PROJECT_DIR/backend

# 載入並導出環境變數
echo "📋 載入環境變數..."
set -a  # 自動導出所有變數
source $PROJECT_DIR/.env
set +a  # 停止自動導出

echo "使用的 GitHub Repository: $GITHUB_REPOSITORY"
echo "PostgreSQL 密碼已設定: ${POSTGRES_PASS:0:8}..."

# .env 文件已經分別創建在正確的位置

# 檢查是否有預構建的映像，如果沒有就在本地構建
if docker pull ghcr.io/$GITHUB_REPOSITORY/backend:latest 2>/dev/null; then
    echo "✅ 使用預構建的映像"
    sudo -u $SERVICE_USER env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f docker-compose.prod.yml up -d
else
    echo "⚠️  預構建映像不存在，使用本地構建..."
    # 暫時修改 docker-compose 使用本地構建
    sed 's|image: ghcr.io/${GITHUB_REPOSITORY}/backend:latest|build: .|' docker-compose.prod.yml > docker-compose.local.yml
    chown $SERVICE_USER:$SERVICE_USER docker-compose.local.yml
    sudo -u $SERVICE_USER env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f docker-compose.local.yml up -d --build
fi

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 30

# 等待 PostgreSQL 準備就緒
echo "⏳ 等待 PostgreSQL 準備就緒..."
COMPOSE_FILE="docker-compose.prod.yml"
if [ -f docker-compose.local.yml ]; then
    COMPOSE_FILE="docker-compose.local.yml"
fi

for i in {1..30}; do
    if sudo -u $SERVICE_USER env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f $COMPOSE_FILE exec -T postgres pg_isready -U backend_user -d backend_db >/dev/null 2>&1; then
        # 測試實際連接和認證
        if sudo -u $SERVICE_USER env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f $COMPOSE_FILE exec -T postgres psql -U backend_user -d backend_db -c "SELECT 1;" >/dev/null 2>&1; then
            echo "✅ PostgreSQL 準備就緒且連接測試成功"
            break
        else
            echo "⏳ PostgreSQL 服務就緒但連接測試失敗，繼續等待..."
        fi
    fi
    if [ $i -eq 30 ]; then
        echo "❌ PostgreSQL 準備逾時"
        exit 1
    fi
    echo "⏳ 等待 PostgreSQL 準備就緒... ($i/30)"
    sleep 2
done

# 運行資料庫遷移
echo "🗄️  運行資料庫遷移..."
if [ -f docker-compose.local.yml ]; then
    sudo -u $SERVICE_USER env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f docker-compose.local.yml exec -T backend uv run alembic upgrade head
else
    sudo -u $SERVICE_USER env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f docker-compose.prod.yml exec -T backend uv run alembic upgrade head
fi


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
