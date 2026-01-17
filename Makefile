.PHONY: help install dev dev-up dev-down dev-logs prod-build prod-up prod-down prod-logs prod-restart clean test lint format migrate migrate-up migrate-down migrate-revision

# Variables
PYTHON := python
UV := uv
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_DEV := docker-compose -f docker-compose.dev.yml
DOCKER_COMPOSE_PROD := docker-compose -f docker-compose.yml

# Default target
help:
	@echo "FastAPI Boilerplate - Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install          Install dependencies using uv"
	@echo "  make dev-up           Start infrastructure (DB) for development"
	@echo "  make dev-down         Stop infrastructure (DB) for development"
	@echo "  make dev-logs         View infrastructure logs"
	@echo "  make dev              Start infrastructure and run server locally"
	@echo ""
	@echo "Production:"
	@echo "  make prod-build       Build Docker image for production"
	@echo "  make prod-up          Start all services (DB + App) in Docker"
	@echo "  make prod-down        Stop all services"
	@echo "  make prod-logs        View production logs"
	@echo "  make prod-restart     Restart production services"
	@echo ""
	@echo "Database:"
	@echo "  make migrate           Run database migrations"
	@echo "  make migrate-up        Run database migrations (alias)"
	@echo "  make migrate-down      Rollback one migration"
	@echo "  make migrate-revision MSG='message'  Create new migration (autogenerate)"
	@echo ""
	@echo "Utilities:"
	@echo "  make test             Run tests"
	@echo "  make lint             Run linter"
	@echo "  make format           Format code"
	@echo "  make clean            Clean up (containers, volumes, cache)"

# Install dependencies
install:
	@echo "Installing dependencies..."
	$(UV) sync

# Development: Start infrastructure only (DB)
dev-up:
	@echo "Starting development infrastructure (PostgreSQL)..."
	$(DOCKER_COMPOSE_DEV) up -d
	@echo "Waiting for database to be ready..."
	@sleep 5
	@echo "Database is ready at localhost:5432"

# Development: Stop infrastructure
dev-down:
	@echo "Stopping development infrastructure..."
	$(DOCKER_COMPOSE_DEV) down

# Development: View logs
dev-logs:
	$(DOCKER_COMPOSE_DEV) logs -f

# Development: Start infrastructure and run server locally
dev: dev-up
	@echo "Starting FastAPI server locally..."
	@echo "Make sure you have .env file configured with:"
	@echo "  DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/boilerplate"
	@echo ""
	$(UV) run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Database migrations
migrate:
	@echo "Running database migrations..."
	$(UV) run alembic upgrade head

migrate-up:
	@echo "Running database migrations..."
	$(UV) run alembic upgrade head

migrate-down:
	@echo "Rolling back one migration..."
	$(UV) run alembic downgrade -1

migrate-revision:
	@echo "Creating new migration..."
	@if [ -z "$(MSG)" ]; then \
		echo "Error: MSG is required"; \
		echo "Usage: make migrate-revision MSG='your message'"; \
		echo "Example: make migrate-revision MSG='Add user table'"; \
		exit 1; \
	fi
	$(UV) run alembic revision --autogenerate -m "$(MSG)"

# Production: Build Docker image
prod-build:
	@echo "Building production Docker image..."
	$(DOCKER_COMPOSE_PROD) build

# Production: Start all services
prod-up:
	@echo "Starting production services..."
	$(DOCKER_COMPOSE_PROD) up -d
	@echo "Services are starting..."
	@echo "API will be available at http://localhost:8000"

# Production: Stop all services
prod-down:
	@echo "Stopping production services..."
	$(DOCKER_COMPOSE_PROD) down

# Production: View logs
prod-logs:
	$(DOCKER_COMPOSE_PROD) logs -f

# Production: Restart services
prod-restart:
	@echo "Restarting production services..."
	$(DOCKER_COMPOSE_PROD) restart

# Run tests
test:
	@echo "Running tests..."
	$(UV) run pytest

# Run linter
lint:
	@echo "Running linter..."
	$(UV) run ruff check app/

# Format code
format:
	@echo "Formatting code..."
	$(UV) run ruff format app/

# Clean up
clean:
	@echo "Cleaning up..."
	$(DOCKER_COMPOSE_DEV) down -v
	$(DOCKER_COMPOSE_PROD) down -v
	@echo "Removing Python cache..."
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup complete"

