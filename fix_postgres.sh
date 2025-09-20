#!/bin/bash

echo "🔧 PostgreSQL Fix and Recovery Script"
echo "====================================="

# Navigate to project directory
cd /opt/mch-backend

echo
echo "⚠️  This script will:"
echo "1. Stop all containers"
echo "2. Remove PostgreSQL volumes (DATA WILL BE LOST!)"
echo "3. Recreate environment files"
echo "4. Restart containers with fresh configuration"
echo

read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled"
    exit 1
fi

echo
echo "🛑 Step 1: Stopping all containers..."
cd backend
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.local.yml down 2>/dev/null || true

echo
echo "🗑️  Step 2: Removing volumes and cleaning up..."
docker volume rm backend_postgres_data 2>/dev/null || true
docker volume rm backend_minio_data 2>/dev/null || true
docker system prune -f

echo
echo "📁 Step 3: Backing up and recreating environment files..."
# Backup existing files
cp /opt/mch-backend/.env /opt/mch-backend/.env.backup 2>/dev/null || true
cp /opt/mch-backend/backend/.env /opt/mch-backend/backend/.env.backup 2>/dev/null || true

# Get GitHub repository name
cd /opt/mch-backend
REPO_URL=$(git remote get-url origin)
if [[ $REPO_URL == *"github.com"* ]]; then
    GITHUB_REPO=$(echo $REPO_URL | sed 's/.*github\.com[:/]\([^/]*\/[^/]*\)\.git.*/\1/' | sed 's/\.git$//')
else
    GITHUB_REPO="mch-cloudmosa-team4/mch-2025-cloudmosa"
fi

# Generate new random passwords
POSTGRES_PASS=$(openssl rand -base64 32)
MINIO_ACCESS=$(openssl rand -base64 12)
MINIO_SECRET=$(openssl rand -base64 32)

echo "📝 Creating new root .env file..."
cat > /opt/mch-backend/.env << EOF
# Docker Compose 環境變數 (用於容器編排)
GITHUB_REPOSITORY=${GITHUB_REPO}
POSTGRES_PASSWORD=${POSTGRES_PASS}
MINIO_ACCESS_KEY=${MINIO_ACCESS}
MINIO_SECRET_KEY=${MINIO_SECRET}
EOF

echo "📝 Creating new backend .env file..."
cat > /opt/mch-backend/backend/.env << EOF
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

# Set proper permissions
chown ubuntu:ubuntu /opt/mch-backend/.env
chown ubuntu:ubuntu /opt/mch-backend/backend/.env
chmod 600 /opt/mch-backend/.env
chmod 600 /opt/mch-backend/backend/.env

echo "✅ Environment files recreated"

echo
echo "🚀 Step 4: Starting containers with new configuration..."
cd /opt/mch-backend/backend

# Load environment variables
set -a
source /opt/mch-backend/.env
set +a

# Start containers
echo "Starting containers..."
sudo -u ubuntu env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f docker-compose.prod.yml up -d

echo
echo "⏳ Waiting for services to start..."
sleep 60

echo
echo "🔍 Checking container status..."
docker ps --filter name=mch

echo
echo "🏥 Testing PostgreSQL connection..."
sleep 10
POSTGRES_CONTAINER=$(docker ps --filter name=postgres --format "{{.Names}}" | head -1)
if [ ! -z "$POSTGRES_CONTAINER" ]; then
    echo "Testing connection as backend_user..."
    if docker exec $POSTGRES_CONTAINER psql -U backend_user -d backend_db -c "SELECT 1;" >/dev/null 2>&1; then
        echo "✅ PostgreSQL connection test PASSED"
    else
        echo "❌ PostgreSQL connection test FAILED"
        echo "PostgreSQL logs:"
        docker logs $POSTGRES_CONTAINER --tail 20
    fi
else
    echo "❌ PostgreSQL container not found"
fi

echo
echo "🔄 Running database migrations..."
sudo -u ubuntu env GITHUB_REPOSITORY="$GITHUB_REPOSITORY" POSTGRES_PASSWORD="$POSTGRES_PASS" MINIO_ACCESS_KEY="$MINIO_ACCESS" MINIO_SECRET_KEY="$MINIO_SECRET" docker-compose -f docker-compose.prod.yml exec -T backend uv run alembic upgrade head

echo
echo "🏥 Final health check..."
sleep 10
if curl -f http://localhost:8000/api/v1/health >/dev/null 2>&1; then
    echo "✅ Backend health check PASSED"
    echo "🎉 Recovery completed successfully!"
    echo
    echo "📊 Services are running at:"
    echo "   Backend API: http://localhost:8000"
    echo "   MinIO Console: http://localhost:9001"
    echo
    echo "🔑 New credentials saved to:"
    echo "   Root: /opt/mch-backend/.env"
    echo "   Backend: /opt/mch-backend/backend/.env"
    echo "   Backups: /opt/mch-backend/.env.backup"
else
    echo "❌ Backend health check FAILED"
    echo "📋 Backend logs:"
    BACKEND_CONTAINER=$(docker ps --filter name=backend --format "{{.Names}}" | head -1)
    if [ ! -z "$BACKEND_CONTAINER" ]; then
        docker logs $BACKEND_CONTAINER --tail 30
    fi
fi

echo
echo "🔍 Recovery script completed!"
