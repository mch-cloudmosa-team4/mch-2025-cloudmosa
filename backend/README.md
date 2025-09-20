
# [Project name] Backend

A FastAPI-based backend server with PostgreSQL database integration for the [Project name] project.

## Quick Start

### Requirements
- Python 3.12 or above
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose

### 1. Setup PostgreSQL + MinIO

Start the PostgreSQL database using Docker:

```bash
# Start PostgreSQL, MinIO and pgAdmin containers
docker-compose up -d

# Check container status
docker-compose ps
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Environment Configuration

Copy the environment example and configure as needed:

```bash
cp .env.example .env
```

### 4. Initialize Database Tables

```bash
# Using Alembic migrations
alembic upgrade head

# Or create tables directly (development only)
python -c "from app.database import create_tables; create_tables()"
```

### 5. Start the Server

```bash
uv run fastapi dev main.py
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

MinIO Console is available at [http://localhost:9001](http://localhost:9001) (default creds: `minioadmin`/`minioadmin`).

## API Endpoints

- **Root**: `http://127.0.0.1:8000/` - Basic API information
- **API Documentation**: `http://127.0.0.1:8000/docs` - Interactive Swagger UI
- **Health Check**: `http://127.0.0.1:8000/api/v1/health` - Service health status
- **Items CRUD**: `http://127.0.0.1:8000/api/v1/items` - Complete CRUD operations
- **Files**: `http://127.0.0.1:8000/api/v1/files`
  - `POST /upload` - Upload a file (form-data key: `file`, optional `folder` query)
  - `GET /presign?id=...` - Get presigned download URL
  - `DELETE /?id=...` - Delete an object

### Items API Examples

- `GET /api/v1/items` - List all items (with pagination)
- `POST /api/v1/items` - Create new item
- `GET /api/v1/items/{item_id}` - Get specific item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## Database Configuration

The application uses PostgreSQL as the primary database with Docker for local development.

### Database Services

- **PostgreSQL**: `localhost:5432`
  - Database: `backend_db`
  - Username: `backend_user`
  - Password: `backend_password`
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)
  - Email: `admin@example.com`
  - Password: `admin123`

### Environment Variables

Key environment variables (see `.env.example` for complete list):

```bash
# Database connection
DATABASE_URL=postgresql://backend_user:backend_password@localhost:5432/backend_db

# Application settings
DEBUG=False
SECRET_KEY=your-secret-key-change-this-in-production
HOST=127.0.0.1
PORT=8000

# MinIO (S3-compatible) settings
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_REGION=us-east-1
MINIO_SECURE=False
MINIO_BUCKET=files
```

### Docker Commands

```bash
# Start database services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs postgres
docker-compose logs pgadmin
docker-compose logs minio

# Reset database (removes all data)
docker-compose down -v && docker-compose up -d
```

### Database Migration

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1
```

## Project Architecture

### Directory Structure

```
backend/
├── main.py                      # FastAPI application entry point
├── pyproject.toml               # Project dependencies and configuration
├── alembic.ini                  # Database migration configuration
├── docker-compose.yml           # Docker services configuration
├── .env.example                 # Environment variables template
├── alembic/                     # Alembic migration files
├── postgres-init/               # PostgreSQL initialization scripts
├── pgadmin-config/              # pgAdmin auto-configuration
├── app/
│   ├── config.py                # Configuration management
│   ├── database.py              # Database connection & session
│   ├── dependencies.py          # FastAPI dependencies
│   ├── models/                  # SQLAlchemy database models
│   │   └── items.py
│   ├── crud/                    # Database operations
│   │   └── item.py
│   ├── router/                  # API routes
│   │   ├── health.py            # Health check endpoints
│   │   └── items.py
│   ├── schemas/                 # Pydantic schemas for HTTP request/response
│   │   └── item.py
│   └── utils/                   # Utility functions
└── scripts/                     # Utility scripts
```

### Architecture Features

- **Modular Design**: Functional separation across modules
- **Database Integration**: SQLAlchemy ORM with automatic table creation
- **Configuration Management**: Pydantic Settings with environment variable support
- **RESTful API**: Standard REST endpoints with auto-generated documentation  
- **Dependency Injection**: FastAPI native system for reusable components
- **Error Handling**: Global exception handling with standardized responses
- **Data Validation**: Pydantic models for request/response validation
- **Database Migrations**: Alembic for version-controlled schema changes

## Development Features

- **Hot Reload**: Automatic server restart on code changes
- **Interactive Documentation**: Swagger UI at `/docs`
- **Database Session Management**: Automatic session handling with dependency injection
- **Type Safety**: Full type hints with Pydantic validation
- **Error Handling**: Comprehensive error responses with proper HTTP status codes

## Troubleshooting

### Common Issues

**Database connection failed:**
```bash
# Check if containers are running
docker-compose ps

# Check database logs
docker-compose logs postgres

# Test database connection
docker-compose exec postgres pg_isready -U backend_user
```

**Dependencies installation failed:**
```bash
# Clear cache and reinstall
pip cache purge
uv sync --reinstall
```

**Tables don't exist:**
```bash
# Run migrations
alembic upgrade head
```

## Expansion Suggestions

Future development considerations:

- **Authentication & Authorization**: JWT tokens, user management
- **Caching**: Redis integration for performance
- **Testing Framework**: pytest configuration with database testing
- **Deployment**: Docker containerization and production setup
- **Monitoring**: Application logging and health monitoring

## Tech Stack

- **Framework**: FastAPI[standard]
- **Database**: PostgreSQL 15 + SQLAlchemy 2.0
- **Database Driver**: psycopg2-binary
- **Migration**: Alembic
- **Python**: 3.12+
- **Package Manager**: uv
- **Configuration**: Pydantic Settings
- **Validation**: Pydantic models
- **Development Database**: Docker + PostgreSQL
- **Database Management**: pgAdmin 4

This architecture provides a solid foundation with complete database integration, ready for production deployment and further feature development.
