# 🚀 SpaceX Fullstack Challenge

![CI/CD Pipeline](https://github.com/pedrocardenas19/spacex-fullstack-challenge/actions/workflows/ci-cd.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.12-blue)
![AWS](https://img.shields.io/badge/AWS-ECS%20%7C%20Lambda%20%7C%20DynamoDB-orange)
![Docker](https://img.shields.io/badge/docker-ready-blue)

A production-ready fullstack application for visualizing SpaceX launches, deployed on AWS with serverless architecture and containerized workloads.

**Live Demo**: http://spacex-alb-307099083.us-east-1.elb.amazonaws.com  
**API Documentation (Swagger)**: http://spacex-alb-307099083.us-east-1.elb.amazonaws.com/docs

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
│                                                              │
│  ┌──────────────────┐      ┌─────────────────────────┐     │
│  │  EventBridge     │      │   ECS Fargate Service   │     │
│  │  (Cron: 6h)      │      │   (Docker Container)    │     │
│  └────────┬─────────┘      │   - FastAPI Backend     │     │
│           │                │   - React Frontend      │     │
│           v                │   - Static Serving      │     │
│  ┌──────────────────┐      └─────────────────────────┘     │
│  │  Lambda Function │               │                       │
│  │  (Python 3.10)   │               │                       │
│  │  SpaceX API Sync │               │                       │
│  │        ↓         │               ↓                       │
│  │   DynamoDB ←─────┼───────────────┘                      │
│  │  (205 launches)  │      (via ALB on port 80)            │
│  └──────────────────┘                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                      │
│                                                              │
│  Push → Tests → Docker Build → ECR Push → ECS Deploy        │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Technical Assessment Highlights

### Key Features Implemented

✅ **Serverless Data Pipeline** - Lambda function with EventBridge (6h cron) syncing SpaceX API data  
✅ **Modern Frontend** - React 18 + TypeScript + Vite + TailwindCSS v4  
✅ **Robust Backend** - FastAPI with proper error handling and CORS  
✅ **NoSQL Database** - DynamoDB with 205 SpaceX launches (current as of 2022)  
✅ **Production Deployment** - AWS ECS Fargate with automated CI/CD  
✅ **Docker Optimization** - Multi-stage build reducing image size  
✅ **Automated Testing** - Unit tests with pytest and coverage reporting  
✅ **CI/CD Pipeline** - GitHub Actions with automated deployment  
✅ **Infrastructure as Code** - Serverless Framework + ECS task definitions  

### User Interface Features

- **Advanced Filtering** - Success/Failure/Upcoming mission status
- **Real-time Search** - Filter by mission name
- **Pagination** - Configurable results per page (10/25/50/100)
- **Detailed Modal** - Complete launch information with rocket specs
- **Statistics Dashboard** - Interactive charts with Recharts
- **Responsive Design** - Mobile-first approach
- **Loading States** - Proper UX feedback

## 🏗️ Technology Stack

### Frontend
- **React 18** - Component-based UI with hooks
- **TypeScript** - Type safety and better DX
- **Vite** - Fast build tool and HMR
- **TailwindCSS v4** - Utility-first CSS framework
- **Recharts** - Data visualization library

### Backend
- **FastAPI** - High-performance async Python framework
- **Boto3** - AWS SDK for DynamoDB operations
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation

### Infrastructure & DevOps
- **AWS Lambda** - Serverless function for data sync
- **AWS DynamoDB** - Managed NoSQL database
- **AWS ECS Fargate** - Serverless container orchestration
- **AWS ECR** - Private Docker registry
- **Docker** - Multi-stage optimized builds
- **GitHub Actions** - Complete CI/CD automation
- **Serverless Framework** - Lambda deployment tool

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (Lambda) / 3.12 (Backend)
- Node.js 20+
- Docker
- AWS CLI configured
- AWS Account with appropriate permissions

### Local Development

**1. Clone and Install Dependencies:**
```bash
git clone https://github.com/pedrocardenas19/spacex-fullstack-challenge.git
cd spacex-fullstack-challenge

# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

**2. Run Backend (Terminal 1):**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**3. Run Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🐳 Docker Deployment

### Build and Run Locally
```bash
# Build multi-stage image
docker build -t spacex-fullstack .

# Run container (requires AWS credentials)
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_DEFAULT_REGION=us-east-1 \
  spacex-fullstack

# Test
curl http://localhost:8000/health
```

### Deploy to AWS ECR
```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 647376275168.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag spacex-fullstack:latest 647376275168.dkr.ecr.us-east-1.amazonaws.com/spacex-fullstack:latest
docker push 647376275168.dkr.ecr.us-east-1.amazonaws.com/spacex-fullstack:latest
```

## ☁️ AWS Infrastructure Setup

### 1. Lambda Function (Data Sync)

The Lambda function is already deployed and syncs SpaceX launch data every 6 hours automatically.

**Lambda Configuration:**
- Runtime: Python 3.10
- Memory: 256 MB
- Timeout: 120s
- Trigger: EventBridge (cron: `rate(6 hours)`)
- Automatic sync from SpaceX API to DynamoDB

### 2. Deploy ECS Service (Web Application)

The application is already deployed and running on AWS ECS Fargate:

**Current Deployment:**
- **Cluster**: spacex-cluster
- **Service**: spacex-fullstack-service
- **Task Definition**: spacex-fullstack-task
- **Access**: Via ALB (port 80)
- **Resources**: 512 CPU units, 1024 MB RAM

**To redeploy after changes:**
```bash
# Automated via GitHub Actions on push to main
git push origin main

# Or manually update ECS service
aws ecs update-service \
  --cluster spacex-cluster \
  --service spacex-fullstack-service \
  --force-new-deployment
```

## 🧪 Testing

### Run All Tests
```bash
# Lambda tests
cd src
pip install -r requirements.txt
pytest tests/ -v

# Backend tests
cd backend
pip install -r requirements.txt
pytest app/tests/ -v --cov=app --cov-report=term-missing
```

### Test Coverage
Current coverage: **>80%** across critical paths

**Lambda Tests:**
- SpaceX API client integration
- DynamoDB repository operations
- Data transformation logic

**Backend Tests:**
- API endpoints (health, launches, stats)
- Query parameter validation
- DynamoDB mocking with boto3

## 📊 API Endpoints

### Base URL
- **Production (ALB - Port 80)**: http://spacex-alb-307099083.us-east-1.elb.amazonaws.com
- **Swagger/OpenAPI Docs**: http://spacex-alb-307099083.us-east-1.elb.amazonaws.com/docs
- **ReDoc**: http://spacex-alb-307099083.us-east-1.elb.amazonaws.com/redoc

**Note**: Lambda sync runs automatically every 6 hours via EventBridge. Manual sync is not exposed publicly for security.

### Available Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/health` | GET | Health check | `GET /health` |
| `/launches` | GET | List all launches | `GET /launches` |
| `/launches?status=success` | GET | Filter by status | `GET /launches?status=success` |
| `/launches?search=falcon` | GET | Search by name | `GET /launches?search=falcon` |
| `/launches/{id}` | GET | Launch details | `GET /launches/5eb87cd9ffd86e000604b32a` |
| `/stats/summary` | GET | Statistics | `GET /stats/summary` |

### Response Examples

**GET /launches**
```json
[
  {
    "id": "5eb87cd9ffd86e000604b32a",
    "name": "FalconSat",
    "date_utc": "2006-03-24T22:30:00.000Z",
    "success": false,
    "rocket_name": "Falcon 1",
    "launchpad_name": "Kwajalein Atoll",
    "details": "Engine failure at 33 seconds..."
  }
]
```

**GET /stats/summary**
```json
{
  "total": 205,
  "success": 181,
  "failure": 6,
  "upcoming": 18,
  "success_rate": 96.79
}
```

## 📁 Project Structure

```
spacex-fullstack-challenge/
├── .github/
│   └── workflows/
│       ├── ci-cd.yml              # Main CI/CD pipeline
│       └── pr-checks.yml          # PR validation
├── frontend/                      # React Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── LaunchCard.tsx    # Launch item component
│   │   │   ├── LaunchModal.tsx   # Detail modal
│   │   │   ├── Pagination.tsx    # Pagination control
│   │   │   └── Statistics.tsx    # Charts dashboard
│   │   ├── api.ts                # API client
│   │   ├── types.ts              # TypeScript interfaces
│   │   └── App.tsx               # Main component
│   ├── package.json
│   └── vite.config.ts
├── backend/                       # FastAPI Application
│   ├── app/
│   │   ├── main.py               # API + static serving
│   │   └── tests/
│   │       └── test_main.py      # API tests
│   └── requirements.txt
├── src/                           # Lambda Function
│   ├── handler.py                # Lambda entry point
│   ├── spacex_client.py          # SpaceX API client
│   ├── models.py                 # Data models
│   ├── dynamo_repository.py      # DynamoDB operations
│   ├── tests/
│   │   └── test_spacex_client.py
│   ├── requirements.txt
│   └── serverless.yml            # Serverless config
├── Dockerfile                     # Multi-stage production build
├── .dockerignore                 # Docker ignore patterns
├── .gitignore                    # Git ignore patterns
└── README.md                     # This file
```

## 🔐 CI/CD Pipeline

### GitHub Actions Workflow

The project includes a complete CI/CD pipeline that runs on every push to `main`:

1. **Lambda Tests** - Run pytest on Lambda function code
2. **Backend Tests** - Run pytest with coverage on FastAPI code
3. **Docker Build** - Build multi-stage Docker image
4. **ECR Push** - Push image to Amazon ECR
5. **ECS Deploy** - Update ECS service with new image

### Required GitHub Secrets

Configure these in `Settings → Secrets and variables → Actions`:

- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key

### Workflow Configuration
```yaml
# .github/workflows/ci-cd.yml
env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: spacex-fullstack
  ECS_SERVICE: spacex-fullstack-service
  ECS_CLUSTER: spacex-cluster
```

## 🌐 Production Infrastructure

**Application URL**: http://spacex-alb-307099083.us-east-1.elb.amazonaws.com

### Application Load Balancer (ALB)
The application is deployed behind an ALB for high availability and production-grade reliability:

- **DNS**: `spacex-alb-307099083.us-east-1.elb.amazonaws.com`
- **Port**: 80 (HTTP) - firewall-friendly
- **Availability Zones**: us-east-1b, us-east-1d, us-east-1e, us-east-1f
- **Health Check**: `/health` endpoint with automatic failover
- **Target**: ECS Fargate tasks on port 8000

**Benefits:**
- ✅ Standard port 80 - no corporate firewall issues
- ✅ Multi-AZ deployment for high availability
- ✅ Automatic health checks and traffic routing
- ✅ Seamless zero-downtime deployments
- ✅ Production-ready architecture

## 💰 AWS Cost Estimate

Based on us-east-1 region pricing:

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------||
| Lambda | 256MB, ~100 invocations/month | $0 (Free Tier) |
| DynamoDB | 205 items, on-demand | ~$1 |
| ECS Fargate | 0.5 vCPU, 1GB RAM, 24/7 | ~$15-20 |
| ALB | Application Load Balancer | ~$20 |
| ECR | ~500MB image storage | ~$0.50 |
| Data Transfer | ~1GB/month | ~$0.50 |
| **Total** | | **~$37-42/month** |

## 🔧 Environment Variables

### Lambda Function
```bash
AWS_REGION=us-east-1
DYNAMODB_TABLE=spacex-launches-dev
```

### Docker Container
```bash
AWS_ACCESS_KEY_ID=<your-key>
AWS_SECRET_ACCESS_KEY=<your-secret>
AWS_DEFAULT_REGION=us-east-1
```

## 📚 Additional Resources

- **Serverless Configuration**: `src/serverless.yml` - Lambda and EventBridge setup
- **Docker Configuration**: `Dockerfile` - Multi-stage production build
- **CI/CD Pipeline**: `.github/workflows/ci-cd.yml` - Complete automation with ALB integration
- **ECS Task Definition**: 512 CPU units, 1024 MB memory, optimized for cost and performance

## ✅ Quality Assurance

- ✅ **Type Safety** - TypeScript for frontend, Pydantic for backend
- ✅ **Code Quality** - Linting and formatting
- ✅ **Automated Testing** - Unit tests with >80% coverage
- ✅ **CI/CD** - Automated testing and deployment
- ✅ **Error Handling** - Proper HTTP status codes and error messages
- ✅ **Security** - Non-root Docker user, environment variables
- ✅ **Performance** - Multi-stage Docker build, CDN-ready
- ✅ **Monitoring** - ECS health checks, CloudWatch logs

## 🎓 Technical Assessment Evaluation Points

### Architecture & Design
- ✅ Proper separation of concerns (Lambda, API, Frontend)
- ✅ Serverless-first approach for cost optimization
- ✅ Container orchestration with ECS Fargate
- ✅ NoSQL database design with DynamoDB

### Code Quality
- ✅ Clean, readable, maintainable code
- ✅ TypeScript interfaces and type safety
- ✅ Python type hints with Pydantic
- ✅ Proper error handling and logging
- ✅ RESTful API design principles

### DevOps & Deployment
- ✅ Docker multi-stage optimization
- ✅ Automated CI/CD pipeline
- ✅ Infrastructure as Code (Serverless Framework)
- ✅ Production-ready deployment on AWS

### Testing & Quality
- ✅ Unit tests with pytest
- ✅ Test coverage reporting
- ✅ Automated testing in CI/CD
- ✅ Mocking external dependencies (boto3, DynamoDB)

### User Experience
- ✅ Responsive, modern UI
- ✅ Fast loading with optimized builds
- ✅ Intuitive filtering and search
- ✅ Proper loading states and error messages

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Pedro Cardenas**  
GitHub: [@pedrocardenas19](https://github.com/pedrocardenas19)

---

**⭐ Technical Assessment Submission - November 2025**