# FastAPI Boilerplate

Production-ready FastAPI boilerplate với authentication (đăng ký, đăng nhập, lấy thông tin người dùng) theo best practices.

## 🏗️ Kiến trúc

Clean Architecture với các layers:

- **API Layer** (`app/api/v1/routes/`): Controllers/Routers
- **Service Layer** (`app/services/`): Business logic
- **Repository Layer** (`app/repositories/`): Data access
- **Models** (`app/models/`): SQLAlchemy ORM models
- **Schemas** (`app/schemas/`): Pydantic validation
- **Core** (`app/core/`): Config, security, dependencies, exceptions
- **Infrastructure** (`app/infra/`): Database setup

## 🚀 Quick Start

### 1. Install dependencies

```bash
make install
# hoặc
uv sync
```

### 2. Setup environment

```bash
cp env.example .env
# Cập nhật các biến môi trường trong .env
```

### 3. Development

```bash
# Start DB và run server locally
make dev
```

Hoặc từng bước:

```bash
make dev-up              # Start PostgreSQL
uv run uvicorn app.main:app --reload  # Run server (terminal khác)
```

### 4. Production

```bash
make prod-build          # Build Docker image
make prod-up             # Start all services (DB + App)
```

### 5. Database migrations

```bash
# Tạo migration đầu tiên
make migrate-revision MSG="Initial migration"

# Chạy migrations
make migrate
```

Hoặc dùng lệnh trực tiếp:

```bash
uv run alembic revision --autogenerate -m "Initial migration"
uv run alembic upgrade head
```

## 📚 API Endpoints

- `POST /api/v1/auth/register` - Đăng ký
- `POST /api/v1/auth/login` - Đăng nhập
- `GET /api/v1/auth/me` - Lấy thông tin user hiện tại (cần JWT token)

API Documentation: `http://localhost:8000/docs`

## 🛠️ Makefile Commands

```bash
make help              # Xem tất cả commands
make install           # Install dependencies
make dev               # Start dev environment
make dev-up/down       # Start/stop DB
make prod-build        # Build Docker image
make prod-up/down      # Start/stop production
make migrate           # Run database migrations
make migrate-revision  # Create new migration
make test              # Run tests
make clean             # Clean up
```

## 📦 Tech Stack

- FastAPI - Web framework
- SQLAlchemy (async) - ORM
- Alembic - Database migrations
- PostgreSQL - Database
- JWT - Authentication
- uv - Package manager
- Docker - Containerization

## 📝 Notes

- Development: DB chạy trong Docker, server chạy local
- Production: Tất cả chạy trong Docker
- Secret key: Tạo bằng `openssl rand -hex 32`
- Không commit file `.env` vào git
