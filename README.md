<h1 align="center">CloudNest</h1>
<div align="center">
  <h4>Bridging Communities, Creating Opportunities</h4>
</div>
<p align="center">
  <a href="#project-info">Project Info</a>&nbsp;&nbsp;•&nbsp;
  <a href="#development-team">Development Team</a>&nbsp;&nbsp;•&nbsp;
  <a href="#core-features">Core Features</a>&nbsp;&nbsp;•&nbsp;
  <a href="#tech-stack">Tech Stack</a>&nbsp;&nbsp;•&nbsp;
  <a href="#requirements">Requirements</a>&nbsp;&nbsp;•&nbsp;
  <a href="#installation">Installation</a>&nbsp;&nbsp;•&nbsp;
  <a href="#usage">Usage</a>
  <a href="#project-structure">Project Structure</a>
</p>

> [!NOTE]
> <h3>CloudNest - "Bridging Communities, Creating Opportunities"</h3>
> 
> In regions with poor information flow, finding work becomes extremely challenging - you might not even know when others are in need of workers. CloudNest targets these underserved areas with a comprehensive workforce matching platform where not only companies, but everyone can post job opportunities and recruit talent. Compensation isn't limited to money - it's entirely up to your mutual agreement! We aim to solve problems for both employers and job seekers, creating a win-win platform for all.

## Project Info
> [!Tip]
> - [http://localhost:8000/docs](http://localhost:8000/docs) - Interactive Swagger UI 
> - [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health) - System Health Status
> - [http://localhost:5050](http://localhost:5050) - pgAdmin Console
> - [http://localhost:9001](http://localhost:9001) - MinIO Console

## Development Team
| Name | Role |
| --- | --- |
| 朱驛庭 | Backend  |
| 何義翔 | Backend  |
| 葉峻誠 | Backend  |
| 蔡昀錚 | Frontend |
| 邱振源 | Frontend |

### Contributors
<a href="https://github.com/mch-cloudmosa-team4/mch-2025-cloudmosa/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mch-cloudmosa-team4/mch-2025-cloudmosa" />
</a>

## Core Features

The platform provides the following key features:
- **User Management**: Complete registration, login, and profile management system
- **Job Posting**: Employers can post job opportunities with skill requirements and compensation details
- **Smart Search**: Semantic job search engine powered by pgVector
- **Application Management**: Job application tracking and employer review mechanism
- **File Management**: Support for resume, portfolio, and other file uploads
- **Skill System**: Skill tagging and matching recommendations
// - **Location-based**: Job recommendations based on geographical location

## Tech Stack
<div align="center">
  <img width="2618" height="1238" alt="CleanShot 2025-09-21 at 12 19 22@2x" src="https://github.com/user-attachments/assets/172fa456-fe44-48f1-880d-1aaeee1f4fc9" />
</div>

### Core Technologies
- **Frontend**: Vue
- **Backend**: FastAPI
- **Database**: PostgreSQL 15 + pgVector Extension
- **File Storage**: MinIO (S3-compatible)
- **Database Migration**: Alembic
- **Vector Search**: pgVector + sentence-transformers
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Package Management**: uv


## Requirements
> [!Caution]
> **Please ensure the following environments are successfully set up**
> - Python 3.12 or higher
> - [uv](https://github.com/astral-sh/uv) package manager
> - Docker and Docker Compose
> - PostgreSQL 15+ (can use Docker for development)
> - MinIO (or S3-compatible storage service)
> 
> Please refer to [.env.example](./backend/.env.example) for required environment variables

## Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd backend
```

### 2. Set Up Environment Variables
```bash
cp .env.example .env
# Edit the .env file and fill in the necessary environment variables
```

### 3. Start Infrastructure Services (PostgreSQL + MinIO)
```bash
docker-compose up -d
```

### 4. Install Python Dependencies
```bash
uv sync
```

### 5. Initialize Database
```bash
# Run database migrations
uv run alembic upgrade head

# Check database connection
docker-compose ps
```

### 6. Start Development Server
```bash
uv run fastapi dev main.py
```

The service will start at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

### API Endpoints Overview
- **Root**: `http://127.0.0.1:8000/` - Basic API information
- **API Documentation**: `http://127.0.0.1:8000/docs` - Interactive Swagger UI
- **Health Check**: `http://127.0.0.1:8000/api/v1/health` - Service health status

### Main Feature Modules

#### 🔐 Authentication System (`/api/v1/auth`)
- `POST /login` - User login
- `POST /register` - User registration
- `POST /refresh` - Token refresh
- `POST /logout` - User logout

#### 👤 Profile Management (`/api/v1/profile`)
- `GET /me` - Get current user data
- `PUT /me` - Update profile
- `GET /` - Batch query user profiles

#### 💼 Job Management (`/api/v1/jobs`)
- `GET /` - Job list (with pagination and search)
- `POST /` - Post new job
- `GET /{job_id}` - Job details
- `PUT /{job_id}` - Update job information
- `DELETE /{job_id}` - Delete job

#### 📄 Application Management (`/api/v1/applications`)
- `POST /` - Submit application
- `GET /` - Query application records
- `PUT /{application_id}` - Update application status

#### 📁 File Management (`/api/v1/files`)
- `POST /upload` - File upload
- `GET /presign` - Get download link
- `DELETE /` - Delete file

#### 🔍 Search Functionality (`/api/v1/search`)
- `GET /jobs` - Semantic job search

### Database Management

#### Alembic Migration Commands
```bash
# Generate new migration file
uv run alembic revision --autogenerate -m "description"

# Execute migration
uv run alembic upgrade head

# Check current version
uv run alembic current

# Rollback migration
uv run alembic downgrade -1
```

#### Docker Database Operations
```bash
# Check service status
docker-compose ps

# View database logs
docker-compose logs postgres

# Reset database (⚠️ will delete all data)
docker-compose down -v && docker-compose up -d
```

### Development Tools

#### MinIO Management Console
- Access: [http://localhost:9001](http://localhost:9001)
- Default credentials: `minioadmin` / `minioadmin`

#### pgAdmin Database Management
- Access: [http://localhost:5050](http://localhost:5050)
- Credentials: `admin@example.com` / `admin123`

## Project Structure

```
backend/
├── main.py                      # FastAPI application entry point
├── pyproject.toml              # Project dependencies and configuration
├── alembic.ini                 # Database migration configuration
├── docker-compose.yml          # Development Docker services
├── docker-compose.prod.yml     # Production Docker services
├── Dockerfile                  # Application Docker image
├── .env.example               # Environment variables template
├── alembic/                   # Alembic migration files
├── app/
│   ├── config.py              # Application configuration management
│   ├── database.py            # Database connection and session management
│   ├── dependencies.py        # FastAPI dependency injection
│   ├── minio.py              # MinIO client configuration
│   ├── models/               # SQLAlchemy data models
│   │   ├── users.py          # User model
│   │   ├── jobs.py           # Job model
│   │   ├── profiles.py       # Profile model
│   │   ├── applications.py   # Application model
│   │   ├── conversations.py  # Conversation model
│   │   └── ...
│   ├── crud/                 # Database operation layer
│   │   ├── user.py          # User CRUD operations
│   │   ├── jobs.py          # Job CRUD operations
│   │   └── ...
│   ├── router/               # API routing layer
│   │   ├── auth.py          # Authentication routes
│   │   ├── jobs.py          # Job-related routes
│   │   ├── profile.py       # Profile routes
│   │   ├── files.py         # File management routes
│   │   └── ...
│   ├── schemas/              # Pydantic data validation models
│   │   ├── auth.py          # Authentication request/response models
│   │   ├── jobs.py          # Job-related models
│   │   └── ...
│   └── utils/                # Utility functions
│       ├── auth.py          # Authentication utilities
│       ├── embedding_model.py # Vector embedding model
│       └── helpers.py       # Common utilities
├── deploy-scripts/           # Deployment scripts
├── test/                    # Test files
└── .github/
    └── workflows/           # GitHub Actions CI/CD
        └── deploy.yml
```
