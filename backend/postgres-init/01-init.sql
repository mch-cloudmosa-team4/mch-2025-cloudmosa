-- Initialize database schema
-- This script will be executed when PostgreSQL container starts for the first time

\echo 'Starting database initialization...'

-- Create required extensions
CREATE EXTENSION IF NOT EXISTS "citext";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
-- CREATE EXTENSION IF NOT EXISTS "hstore";

\echo 'Database initialization completed.'