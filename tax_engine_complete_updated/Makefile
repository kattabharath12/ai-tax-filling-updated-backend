# Tax Engine Makefile

.PHONY: help install dev build up down logs clean test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev: ## Start development environment
	docker-compose up -d db redis
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	cd frontend && npm start

build: ## Build Docker images
	docker-compose build

up: ## Start all services with Docker
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## View logs
	docker-compose logs -f

clean: ## Clean up Docker resources
	docker-compose down -v
	docker system prune -f

test: ## Run tests
	cd backend && python -m pytest
	cd frontend && npm test

migrate: ## Run database migrations
	cd backend && alembic upgrade head

backup: ## Backup database
	docker exec tax_engine_db mysqldump -u taxuser -ptaxpassword tax_engine > backup_$(shell date +%Y%m%d_%H%M%S).sql