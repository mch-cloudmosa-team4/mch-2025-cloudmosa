# 生產環境部署指南

本文檔詳細說明如何將 MCH Backend 部署到 Ubuntu 生產服務器。

## 🏗️ 架構概覽

生產環境使用以下技術棧：
- **容器化**: Docker & Docker Compose
- **反向代理**: 由你的前端服務器處理 (Nginx/Apache)
- **資料庫**: PostgreSQL 15
- **文件存儲**: MinIO
- **CI/CD**: GitHub Actions
- **安全**: UFW 防火牆 + Fail2ban

**注意**: 此配置假設你已有前端服務器處理 SSL 和反向代理。

## 📋 前置需求

### 服務器要求
- Ubuntu 20.04 LTS 或更高版本
- 最少 2GB RAM, 20GB 存儲空間
- Root 或 sudo 權限
- 固定 IP 地址

### 域名設定
- 已註冊的域名
- DNS A 記錄指向服務器 IP

## 🚀 快速部署

### 步驟 1: 服務器初始設置

在你的 Ubuntu 服務器上執行：

```bash
# 下載部署腳本
curl -O https://raw.githubusercontent.com/your-username/mch-2025-cloudmosa/main/backend/deploy.sh

# 編輯腳本，設定你的域名
nano deploy.sh
# 修改: DOMAIN="your-domain.com"

# 執行部署
sudo bash deploy.sh
```

### 步驟 2: GitHub Repository 設定

在你的 GitHub repository 中設定以下 Secrets：

1. 前往 `Settings` > `Secrets and variables` > `Actions`
2. 添加以下 secrets：

```
SERVER_HOST: 你的服務器 IP 地址
SERVER_USER: mch
SERVER_SSH_KEY: SSH 私鑰內容
POSTGRES_PASSWORD: 從服務器 /opt/mch-backend/.env 複製
MINIO_ACCESS_KEY: 從服務器 /opt/mch-backend/.env 複製  
MINIO_SECRET_KEY: 從服務器 /opt/mch-backend/.env 複製
```

### 步驟 3: SSH 金鑰設定

```bash
# 在你的本地機器生成 SSH 金鑰對
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/mch_deploy

# 將公鑰添加到服務器
ssh-copy-id -i ~/.ssh/mch_deploy.pub mch@your-server-ip

# 將私鑰內容添加到 GitHub Secrets (SERVER_SSH_KEY)
cat ~/.ssh/mch_deploy
```

### 步驟 4: 觸發自動部署

推送代碼到 main 分支：

```bash
git add .
git commit -m "Initial production deployment"
git push origin main
```

## 🔧 手動部署指令

如果需要手動部署或調試：

```bash
# 登入服務器
ssh mch@your-server-ip

# 進入項目目錄
cd /opt/mch-backend

# 拉取最新代碼
git pull origin main

# 更新容器
docker-compose -f backend/docker-compose.prod.yml pull
docker-compose -f backend/docker-compose.prod.yml up -d

# 運行資料庫遷移
docker-compose -f backend/docker-compose.prod.yml exec backend uv run alembic upgrade head
```

## 📊 監控和日誌

### 查看服務狀態
```bash
# 查看所有容器狀態
docker-compose -f backend/docker-compose.prod.yml ps

# 查看實時日誌
docker-compose -f backend/docker-compose.prod.yml logs -f

# 查看特定服務日誌
docker-compose -f backend/docker-compose.prod.yml logs -f backend
```

### 健康檢查
```bash
# 直接檢查 backend 服務
curl http://localhost:8000/api/v1/health

# 數據庫連接測試
docker-compose -f backend/docker-compose.prod.yml exec postgres pg_isready -U backend_user

# MinIO 健康檢查
curl https://your-domain.com/storage/minio/health/live
```

## 🔐 安全設定

### 防火牆狀態
```bash
# 查看防火牆狀態
sudo ufw status

# 查看 fail2ban 狀態
sudo fail2ban-client status
```

### SSL 證書更新
```bash
# 檢查證書狀態
sudo certbot certificates

# 測試自動更新
sudo certbot renew --dry-run
```

## 🔄 備份和恢復

### 資料庫備份
```bash
# 創建備份
docker-compose -f backend/docker-compose.prod.yml exec postgres \
  pg_dump -U backend_user backend_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢復備份
docker-compose -f backend/docker-compose.prod.yml exec -T postgres \
  psql -U backend_user backend_db < backup_file.sql
```

### MinIO 數據備份
```bash
# 備份 MinIO 數據
sudo tar -czf minio_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  -C /var/lib/docker/volumes mch-backend_minio_data
```

## 🚨 故障排除

### 常見問題

1. **容器無法啟動**
   ```bash
   # 檢查日誌
   docker-compose -f backend/docker-compose.prod.yml logs
   
   # 重建容器
   docker-compose -f backend/docker-compose.prod.yml up -d --force-recreate
   ```

2. **資料庫連接失敗**
   ```bash
   # 檢查資料庫狀態
   docker-compose -f backend/docker-compose.prod.yml exec postgres pg_isready
   
   # 重啟資料庫
   docker-compose -f backend/docker-compose.prod.yml restart postgres
   ```

3. **Nginx 502 錯誤**
   ```bash
   # 檢查 Nginx 配置
   sudo nginx -t
   
   # 重啟 Nginx
   sudo systemctl restart nginx
   ```

4. **SSL 證書問題**
   ```bash
   # 重新獲取證書
   sudo certbot --nginx -d your-domain.com --force-renewal
   ```

## 📈 性能優化

### 資料庫優化
在 `docker-compose.prod.yml` 中添加 PostgreSQL 調優參數：

```yaml
postgres:
  environment:
    - POSTGRES_SHARED_PRELOAD_LIBRARIES=pg_stat_statements
  command: >
    postgres
    -c shared_buffers=256MB
    -c effective_cache_size=1GB
    -c maintenance_work_mem=64MB
    -c checkpoint_completion_target=0.9
```

### Nginx 快取設定
在 `nginx.conf` 中添加快取配置：

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## 🔧 環境變數

完整的環境變數列表：

```bash
# 資料庫
DATABASE_URL=postgresql://backend_user:password@postgres:5432/backend_db
DATABASE_ECHO=false
DATABASE_AUTO_CREATE=false

# 應用程式
DEBUG=false
APP_NAME=MCH Backend
VERSION=1.0.0

# MinIO
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_SECURE=false
MINIO_BUCKET=files

# 安全
SECRET_KEY=your-secret-key
```

## 📞 支援

如有問題，請：
1. 查看日誌文件
2. 檢查 GitHub Issues
3. 聯繫開發團隊

---

**注意**: 請確保定期更新系統套件和 Docker 映像以保持安全性。
