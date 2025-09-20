#!/bin/bash

echo "🔍 PostgreSQL Authentication Debugging Script"
echo "=============================================="

# Navigate to project directory
cd /opt/mch-backend

echo
echo "📁 Current directory: $(pwd)"
echo

# Check if .env files exist and their contents
echo "📄 Checking .env files..."
echo "Root .env file:"
if [ -f .env ]; then
    echo "✅ /opt/mch-backend/.env exists"
    echo "Contents (passwords masked):"
    sed 's/PASSWORD=.*/PASSWORD=***MASKED***/g' .env
else
    echo "❌ /opt/mch-backend/.env NOT FOUND"
fi

echo
echo "Backend .env file:"
if [ -f backend/.env ]; then
    echo "✅ /opt/mch-backend/backend/.env exists"
    echo "Contents (passwords masked):"
    sed 's/PASSWORD=.*/PASSWORD=***MASKED***/g' backend/.env
else
    echo "❌ /opt/mch-backend/backend/.env NOT FOUND"
fi

echo
echo "🐳 Docker containers status:"
docker ps -a --filter name=mch

echo
echo "🗃️ Docker volumes:"
docker volume ls | grep -E "(postgres|mch)"

echo
echo "🔑 Environment variables from docker-compose:"
echo "Checking PostgreSQL container environment..."

# Get the actual environment variables from the PostgreSQL container
POSTGRES_CONTAINER=$(docker ps --filter name=postgres --format "{{.Names}}" | head -1)
if [ ! -z "$POSTGRES_CONTAINER" ]; then
    echo "PostgreSQL container: $POSTGRES_CONTAINER"
    echo "Environment variables:"
    docker exec $POSTGRES_CONTAINER env | grep -E "(POSTGRES_|DATABASE_)" | sed 's/PASSWORD=.*/PASSWORD=***MASKED***/'
else
    echo "❌ PostgreSQL container not running"
fi

echo
echo "🔗 Backend container environment:"
BACKEND_CONTAINER=$(docker ps --filter name=backend --format "{{.Names}}" | head -1)
if [ ! -z "$BACKEND_CONTAINER" ]; then
    echo "Backend container: $BACKEND_CONTAINER"
    echo "Environment variables:"
    docker exec $BACKEND_CONTAINER env | grep -E "(POSTGRES_|DATABASE_)" | sed 's/PASSWORD=.*/PASSWORD=***MASKED***/'
else
    echo "❌ Backend container not running"
fi

echo
echo "🔬 PostgreSQL connection test:"
if [ ! -z "$POSTGRES_CONTAINER" ]; then
    echo "Testing PostgreSQL connection..."
    echo "Available databases:"
    docker exec $POSTGRES_CONTAINER psql -U backend_user -d backend_db -c "\l"
    echo
    echo "Checking users and roles:"
    docker exec $POSTGRES_CONTAINER psql -U backend_user -d backend_db -c "\du"
    echo
    echo "Testing basic connection:"
    docker exec $POSTGRES_CONTAINER psql -U backend_user -d backend_db -c "SELECT 1 as test_connection;"
    echo
    echo "Checking installed extensions:"
    docker exec $POSTGRES_CONTAINER psql -U backend_user -d backend_db -c "\dx"
else
    echo "❌ Cannot test - PostgreSQL container not running"
fi

echo
echo "📊 Docker logs (last 20 lines):"
echo "PostgreSQL logs:"
if [ ! -z "$POSTGRES_CONTAINER" ]; then
    docker logs $POSTGRES_CONTAINER --tail 20
else
    echo "❌ PostgreSQL container not available"
fi

echo
echo "Backend logs:"
if [ ! -z "$BACKEND_CONTAINER" ]; then
    docker logs $BACKEND_CONTAINER --tail 20
else
    echo "❌ Backend container not available"
fi

echo
echo "🛠️  Recommended actions:"
echo "1. If passwords don't match, run the cleanup and redeploy steps below"
echo "2. If volumes contain old data, remove them and restart"
echo "3. Check that .env files have correct content"

echo
echo "📋 Quick fix commands (run these if needed):"
echo
echo "# Stop all containers:"
echo "cd /opt/mch-backend/backend && docker-compose -f docker-compose.prod.yml down"
echo
echo "# Remove PostgreSQL volume (THIS WILL DELETE DATA!):"
echo "docker volume rm backend_postgres_data"
echo
echo "# Remove all related volumes:"
echo "docker volume prune -f"
echo
echo "# Restart with fresh environment:"
echo "cd /opt/mch-backend/backend"
echo "source /opt/mch-backend/.env"
echo "docker-compose -f docker-compose.prod.yml up -d"

echo
echo "🔍 Debug script completed!"

