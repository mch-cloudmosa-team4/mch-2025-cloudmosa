
# [Project name] Backend

A FastAPI-based backend server with SQLAlchemy database integration for the [Project name] project.

## Quick Start

### Requirements
- Python 3.12 or above
- [uv](https://github.com/astral-sh/uv) package manager

### Install Dependencies

```bash
uv sync
```

### Initialize Database

Database tables will be created automatically on first startup.

### Start the Server

```bash
uv run fastapi dev main.py
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

- **Root**: `http://127.0.0.1:8000/` - Basic API information
- **API Documentation**: `http://127.0.0.1:8000/docs` - Interactive Swagger UI
- **Health Check**: `http://127.0.0.1:8000/api/v1/health` - Service health status
- **Items CRUD**: `http://127.0.0.1:8000/api/v1/items` - Complete CRUD operations

### Items API Examples

- `GET /api/v1/items` - List all items (with pagination)
- `POST /api/v1/items` - Create new item
- `GET /api/v1/items/{item_id}` - Get specific item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## Database Configuration

The application uses SQLite by default for development. For production, you can configure PostgreSQL:

### Environment Variables

```bash
DATABASE_URL=postgresql://user:password@localhost/[Project name]
```

### Database Migration (TODO)

>[!WARNING]
> This section has not been refined. I just leave some files but not tested.

Alembic is configured for database migrations:

```bash
# Generate migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head
```

## Project Architecture

### Directory Structure

```
backend/
├── main.py              # FastAPI application entry point
├── alembic.ini          # Database migration configuration
├── migrations/          # Alembic migration files
├── app/
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection & session
│   ├── models/          # SQLAlchemy database models
│   │   └── database.py  # Item model definition
│   ├── crud/            # Database operations
│   │   └── item.py      # Item CRUD operations
│   ├── router/          # API routes
│   │   └── items.py     # Items API endpoints
│   ├── schemas/         # Pydantic schemas
│   │   └── item.py      # Item request/response schemas
│   └── utils/           # Utility functions
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

## Expansion Suggestions

Future development considerations:

- **Authentication & Authorization**: JWT tokens, user management
- **Caching**: Redis integration for performance
- **Testing Framework**: pytest configuration with database testing
- **Deployment**: Docker containerization and production setup
- **Monitoring**: Application logging and health monitoring

## Tech Stack

- **Framework**: FastAPI[standard]
- **Database**: SQLAlchemy 2.0 + SQLite/PostgreSQL
- **Migration**: Alembic
- **Python**: 3.12+
- **Package Manager**: uv
- **Configuration**: Pydantic Settings
- **Validation**: Pydantic models

This architecture provides a solid foundation with complete database integration, ready for production deployment and further feature development.
