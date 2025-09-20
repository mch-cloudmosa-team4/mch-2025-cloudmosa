#!/bin/bash
# pgAdmin initialization script for production

set -e

echo "🔧 Initializing pgAdmin for production..."

# Create .pgpass file with current PostgreSQL credentials
echo "Creating .pgpass file..."
mkdir -p /var/lib/pgadmin
cat > /var/lib/pgadmin/.pgpass << EOF
postgres:5432:backend_db:backend_user:${POSTGRES_PASSWORD}
postgres:5432:*:backend_user:${POSTGRES_PASSWORD}
EOF

# Set correct permissions for .pgpass
chmod 600 /var/lib/pgadmin/.pgpass

# Copy servers configuration
echo "Setting up server configuration..."
cp /tmp/servers-prod.json /var/lib/pgadmin/servers.json

echo "✅ pgAdmin initialization completed!"

# Start the original pgAdmin entrypoint
exec /entrypoint.sh
