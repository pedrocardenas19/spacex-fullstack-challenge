.PHONY: help install test lint build run deploy clean

# Variables
PYTHON := python3
PIP := pip3
DOCKER := docker
AWS_REGION := us-east-1
ECR_REPO := spacex-fullstack

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ==================================================
# Instalación y Setup
# ==================================================

install: ## Instala todas las dependencias
	@echo "📦 Instalando dependencias..."
	cd frontend && npm install
	cd backend && $(PIP) install -r requirements.txt
	$(PIP) install -r requirements.txt

setup-venv: ## Crea y activa virtualenv
	$(PYTHON) -m venv venv
	@echo "✅ Virtualenv creado. Actívalo con: source venv/bin/activate"

# ==================================================
# Testing
# ==================================================

test: test-lambda test-backend ## Ejecuta todos los tests

test-lambda: ## Tests de Lambda/src
	@echo "🧪 Testing Lambda..."
	cd src && $(PYTHON) -m pytest tests/ -v

test-backend: ## Tests de Backend
	@echo "🧪 Testing Backend..."
	cd backend && $(PYTHON) -m pytest app/tests/ -v

test-coverage: ## Tests con coverage
	@echo "📊 Running tests with coverage..."
	cd src && $(PYTHON) -m pytest tests/ -v --cov=. --cov-report=html
	cd backend && $(PYTHON) -m pytest app/tests/ -v --cov=app --cov-report=html

# ==================================================
# Linting y Formateo
# ==================================================

lint: ## Ejecuta linters
	@echo "🔍 Running linters..."
	flake8 backend/ src/ --max-line-length=100 --exclude=venv,node_modules
	black --check backend/ src/
	isort --check-only backend/ src/

format: ## Formatea el código
	@echo "✨ Formatting code..."
	black backend/ src/
	isort backend/ src/

# ==================================================
# Desarrollo Local
# ==================================================

dev-backend: ## Inicia backend en modo desarrollo
	@echo "🚀 Starting backend..."
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Inicia frontend en modo desarrollo
	@echo "🚀 Starting frontend..."
	cd frontend && npm run dev

dev: ## Inicia backend y frontend (requiere 2 terminales)
	@echo "Use 'make dev-backend' en una terminal y 'make dev-frontend' en otra"

# ==================================================
# Docker
# ==================================================

docker-build: ## Build de imagen Docker
	@echo "🐳 Building Docker image..."
	$(DOCKER) build -t $(ECR_REPO):latest .

docker-run: ## Ejecuta contenedor localmente
	@echo "🐳 Running Docker container..."
	$(DOCKER) run -p 8000:8000 \
		-e LAUNCHES_TABLE_NAME=spacex-launches-dev \
		-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		-e AWS_DEFAULT_REGION=$(AWS_REGION) \
		$(ECR_REPO):latest

docker-test: docker-build ## Build y test local de Docker
	@echo "🧪 Testing Docker container..."
	$(DOCKER) run --rm $(ECR_REPO):latest curl -f http://localhost:8000/health

# ==================================================
# AWS Deployment
# ==================================================

deploy-ecr: ## Deploy a Amazon ECR
	@echo "☁️  Deploying to ECR..."
	./deploy-ecr.sh

deploy-lambda: ## Deploy Lambda con Serverless
	@echo "⚡ Deploying Lambda..."
	cd src && serverless deploy

deploy-all: deploy-lambda deploy-ecr ## Deploy completo (Lambda + ECS)

# ==================================================
# Utilidades
# ==================================================

clean: ## Limpia archivos temporales
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	cd frontend && rm -rf dist/ node_modules/.vite

logs-ecs: ## Ver logs de ECS
	@echo "📋 Fetching ECS logs..."
	aws logs tail /ecs/spacex-fullstack --follow --region $(AWS_REGION)

status-ecs: ## Ver estado de servicio ECS
	@echo "📊 ECS Service Status:"
	aws ecs describe-services \
		--cluster spacex-cluster \
		--services spacex-fullstack-service \
		--region $(AWS_REGION) \
		--query 'services[0].[serviceName,status,runningCount,desiredCount]' \
		--output table

restart-ecs: ## Reinicia servicio ECS (force new deployment)
	@echo "🔄 Restarting ECS service..."
	aws ecs update-service \
		--cluster spacex-cluster \
		--service spacex-fullstack-service \
		--force-new-deployment \
		--region $(AWS_REGION)

# ==================================================
# Database
# ==================================================

db-scan: ## Escanea tabla DynamoDB
	@echo "🗄️  Scanning DynamoDB..."
	aws dynamodb scan \
		--table-name spacex-launches-dev \
		--region $(AWS_REGION) \
		--max-items 10

db-count: ## Cuenta items en DynamoDB
	@echo "🔢 Counting DynamoDB items..."
	aws dynamodb scan \
		--table-name spacex-launches-dev \
		--region $(AWS_REGION) \
		--select COUNT

sync-launches: ## Ejecuta sync manual de lanzamientos
	@echo "🚀 Syncing launches..."
	curl -X POST https://qpzf4ldr0g.execute-api.us-east-1.amazonaws.com/sync

# ==================================================
# Info
# ==================================================

info: ## Muestra información del proyecto
	@echo "=========================================="
	@echo "🚀 SpaceX Fullstack Challenge"
	@echo "=========================================="
	@echo "Python version: $$($(PYTHON) --version)"
	@echo "Node version: $$(node --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker version: $$($(DOCKER) --version 2>/dev/null || echo 'Not installed')"
	@echo "AWS CLI version: $$(aws --version 2>/dev/null || echo 'Not installed')"
	@echo "=========================================="
