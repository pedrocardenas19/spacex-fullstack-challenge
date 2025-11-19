# 🚀 SpaceX Fullstack Challenge

![CI/CD Pipeline](https://github.com/pedrocardenas19/spacex-fullstack-challenge/actions/workflows/ci-cd.yml/badge.svg)
![PR Checks](https://github.com/pedrocardenas19/spacex-fullstack-challenge/actions/workflows/pr-checks.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.12-blue)
![AWS](https://img.shields.io/badge/AWS-ECS%20%7C%20Lambda%20%7C%20DynamoDB-orange)
![Docker](https://img.shields.io/badge/docker-ready-blue)

Aplicación fullstack para visualizar lanzamientos de SpaceX, desplegada en AWS con arquitectura serverless y contenedorizada.

## 📐 Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
│                                                              │
│  ┌──────────────────┐      ┌─────────────────────────┐     │
│  │  EventBridge     │      │   Application Load      │     │
│  │  (Cron: 6h)      │      │   Balancer (ALB)        │     │
│  └────────┬─────────┘      └──────────┬──────────────┘     │
│           │                            │                     │
│           v                            v                     │
│  ┌──────────────────┐      ┌─────────────────────────┐     │
│  │  Lambda Function │      │   ECS Fargate Service   │     │
│  │  (Python 3.10)   │      │   (Docker Container)    │     │
│  │  Sync SpaceX API │      │   - FastAPI Backend     │     │
│  │        ↓         │      │   - React Frontend      │     │
│  │   DynamoDB ←─────┼──────┤   - Serves Static      │     │
│  │  (205 launches)  │      │   - Port 8000          │     │
│  └──────────────────┘      └─────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                      │
│                                                              │
│  Push to main → Tests → Docker Build → ECR Push → ECS Deploy│
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Stack Tecnológico

### Backend
- **FastAPI** - API REST con Python 3.12
- **Boto3** - SDK de AWS para DynamoDB
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI Library
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **TailwindCSS** - Styling
- **Recharts** - Data visualization

### Infraestructura
- **AWS Lambda** - Sync de datos desde SpaceX API
- **AWS DynamoDB** - Base de datos NoSQL
- **AWS ECS Fargate** - Contenedores serverless
- **AWS ECR** - Docker registry
- **Docker** - Multi-stage optimized builds
- **GitHub Actions** - CI/CD automation

## 🚀 Quick Start

### Pre-requisitos
```bash
# Instalar dependencias
make install

# O manualmente:
cd frontend && npm install
cd backend && pip install -r requirements.txt
pip install -r requirements.txt
```

### Desarrollo Local

**Terminal 1 - Backend:**
```bash
make dev-backend
# O: cd backend && uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
make dev-frontend
# O: cd frontend && npm run dev
```

Acceder a:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🐳 Docker

### Build y Run Local
```bash
# Build
make docker-build

# Run (requiere credenciales AWS)
make docker-run

# Test
curl http://localhost:8000/health
```

### Deploy a AWS ECR
```bash
# Usar script automatizado
./deploy-ecr.sh

# O con make
make deploy-ecr
```

## ☁️ Deployment a AWS

### 1. Lambda (Sync de Datos)
```bash
cd src
serverless deploy
```

### 2. ECS Fargate (Aplicación Web)
```bash
# Configurar task definition
aws ecs register-task-definition --cli-input-json file://task-definition.example.json

# Deploy con GitHub Actions (automático en push a main)
git push origin main
```

## 🧪 Testing

```bash
# Todos los tests
make test

# Lambda tests
make test-lambda

# Backend tests
make test-backend

# Con coverage
make test-coverage
```

## 📊 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/launches` | GET | Lista todos los lanzamientos |
| `/launches?status=success` | GET | Filtra por status |
| `/launches/{id}` | GET | Detalle de lanzamiento |
| `/stats/summary` | GET | Estadísticas agregadas |

## 📁 Estructura del Proyecto

```
spacex-fullstack-challenge/
├── .github/
│   └── workflows/
│       ├── ci-cd.yml           # Pipeline principal
│       └── pr-checks.yml       # Checks de PRs
├── frontend/                   # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── App.tsx
│   └── package.json
├── backend/                    # FastAPI
│   ├── app/
│   │   ├── main.py            # API + Static serving
│   │   └── tests/
│   └── requirements.txt
├── src/                        # Lambda function
│   ├── handler.py
│   ├── spacex_client.py
│   ├── models.py
│   ├── dynamo_repository.py
│   └── tests/
├── Dockerfile                  # Multi-stage build
├── deploy-ecr.sh              # Script de deploy
├── Makefile                   # Comandos útiles
└── serverless.yml             # Config de Lambda
```

## 🔐 GitHub Actions Setup

### Secrets Requeridos
En `Settings → Secrets and variables → Actions`:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Variables de Entorno (en workflow)
```yaml
AWS_REGION: us-east-1
ECR_REPOSITORY: spacex-fullstack
ECS_SERVICE: spacex-fullstack-service
ECS_CLUSTER: spacex-cluster
```

Ver documentación completa: [GITHUB_ACTIONS.md](./GITHUB_ACTIONS.md)

## 📚 Documentación

- [🐳 Docker Deployment Guide](./DOCKER_DEPLOYMENT.md)
- [🔄 GitHub Actions Setup](./GITHUB_ACTIONS.md)
- [📋 Task Definition Example](./task-definition.example.json)
- [🔒 IAM Policy](./iam-policy.json)

## 🛠️ Comandos Útiles

```bash
# Ver todos los comandos disponibles
make help

# Linting y formato
make lint
make format

# Logs de ECS
make logs-ecs

# Estado del servicio
make status-ecs

# Restart forzado
make restart-ecs

# Info del proyecto
make info
```

## 🎯 Features

✅ SPA con React + TypeScript  
✅ API REST con FastAPI  
✅ Sync automático cada 6 horas (Lambda)  
✅ Filtros por status y búsqueda  
✅ Paginación configurable  
✅ Gráficos con Recharts  
✅ Modal de detalles  
✅ Responsive design  
✅ Docker multi-stage optimizado  
✅ CI/CD con GitHub Actions  
✅ Tests automatizados  
✅ Deploy a ECS Fargate  

## 📈 Costos Estimados (AWS)

- **Lambda**: ~$0/mes (dentro del free tier)
- **DynamoDB**: ~$1/mes (205 items, on-demand)
- **ECS Fargate**: ~$15-30/mes (512 CPU, 1GB RAM)
- **ALB**: ~$20/mes
- **ECR**: ~$1/mes (storage)
- **Total**: ~$40-60/mes

## 🤝 Contributing

1. Fork el proyecto
2. Crea una feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 License

Este proyecto está bajo la licencia MIT.

## 🙋 Autor

**Pedro Cardenas**  
GitHub: [@pedrocardenas19](https://github.com/pedrocardenas19)

---

⭐ Si te gustó este proyecto, dale una estrella!