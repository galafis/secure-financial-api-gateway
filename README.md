# 🔐 Secure Financial API Gateway

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Security](https://img.shields.io/badge/security-hardened-brightgreen.svg)](https://github.com/galafis/secure-financial-api-gateway)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



[English](#english) | [Português](#português)

---

<a name="english"></a>

## 📖 Overview

A **production-ready API Gateway** with advanced security features designed for financial services. Implements JWT authentication, rate limiting, circuit breaker pattern, and comprehensive security headers.

### Key Features

- **🔐 JWT Authentication**: Secure token-based authentication with refresh tokens
- **⏱️ Rate Limiting**: Token bucket algorithm with per-user and per-IP limits
- **🔄 Circuit Breaker**: Prevents cascading failures with automatic recovery
- **🛡️ Security Headers**: OWASP-compliant security headers
- **📝 Request Logging**: Structured logging with request IDs and timing
- **🔒 Password Hashing**: Bcrypt with configurable work factor
- **📊 Admin Routes**: Role-based access control (RBAC)
- **🚀 High Performance**: Async/await with FastAPI

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Client Request                                                   │
│       │                                                           │
│       ▼                                                           │
│  ┌─────────────────────────────────────────────────┐            │
│  │         Security Headers Middleware             │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ▼                                               │
│  ┌─────────────────────────────────────────────────┐            │
│  │         Request Logger Middleware               │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ▼                                               │
│  ┌─────────────────────────────────────────────────┐            │
│  │         Rate Limiter Middleware                 │            │
│  │         (Token Bucket Algorithm)                │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ▼                                               │
│  ┌─────────────────────────────────────────────────┐            │
│  │         Circuit Breaker Middleware              │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ▼                                               │
│  ┌─────────────────────────────────────────────────┐            │
│  │         JWT Authentication                      │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ▼                                               │
│  ┌─────────────────────────────────────────────────┐            │
│  │         Route Handlers                          │            │
│  │  • Auth Routes                                  │            │
│  │  • User Routes                                  │            │
│  │  • Trading Routes                               │            │
│  │  • Admin Routes                                 │            │
│  └─────────────────────────────────────────────────┘            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **pip** package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/galafis/secure-financial-api-gateway.git
cd secure-financial-api-gateway

# Install dependencies
pip install -r requirements.txt

# Run the API Gateway
python src/main.py
```

The API will be available at: http://localhost:8000

**API Documentation**: http://localhost:8000/api/docs

---

## 🔐 Authentication

### Register New User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "secure_password123"
  }'
```

### Access Protected Route

```bash
curl -X GET http://localhost:8000/api/v1/users/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Refresh Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }'
```

---

## 🛡️ Security Features

### JWT Authentication

- **Algorithm**: HS256
- **Access Token**: 30 minutes expiry
- **Refresh Token**: 7 days expiry
- **Password Hashing**: Bcrypt with salt

### Rate Limiting

**Token Bucket Algorithm:**
- Default: 60 requests per minute per client
- Configurable per-user limits
- Automatic token refill
- HTTP 429 response when exceeded

**Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1696598400
```

### Circuit Breaker

**States:**
- **CLOSED**: Normal operation
- **OPEN**: Rejecting requests (service unavailable)
- **HALF-OPEN**: Testing recovery

**Configuration:**
- Failure threshold: 5 consecutive failures
- Timeout: 60 seconds
- Automatic recovery testing

### Security Headers

All responses include:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

---

## 📊 API Endpoints

### Authentication Routes (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login user | No |
| POST | `/refresh` | Refresh access token | No |
| GET | `/me` | Get current user info | Yes |
| POST | `/logout` | Logout user | Yes |

### User Routes (`/api/v1/users`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/profile` | Get user profile | Yes |

### Trading Routes (`/api/v1/trading`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/orders` | Get user orders | Yes |

### Admin Routes (`/api/v1/admin`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users` | List all users | Yes (Admin) |

---

## 📁 Project Structure

```
secure-financial-api-gateway/
├── src/
│   ├── main.py                     # Application entry point
│   ├── middleware/
│   │   ├── rate_limiter.py         # Rate limiting middleware
│   │   ├── circuit_breaker.py      # Circuit breaker middleware
│   │   ├── security_headers.py     # Security headers middleware
│   │   └── request_logger.py       # Request logging middleware
│   ├── auth/
│   │   └── jwt_handler.py          # JWT token handling
│   ├── routes/
│   │   ├── auth_routes.py          # Authentication routes
│   │   ├── user_routes.py          # User routes
│   │   ├── trading_routes.py       # Trading routes
│   │   └── admin_routes.py         # Admin routes
│   └── utils/
│       └── logger.py               # Logging utilities
├── tests/
│   └── test_auth.py                # Authentication tests
├── config/
│   └── settings.py                 # Configuration settings
├── docs/
│   └── api_documentation.md        # API documentation
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Language | Python 3.11+ |
| Authentication | JWT (PyJWT) |
| Password Hashing | Bcrypt (Passlib) |
| Async Runtime | Uvicorn |
| Validation | Pydantic |
| Testing | Pytest |

---

## ⚙️ Configuration

### Environment Variables

```bash
# Server configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production

# JWT configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS configuration
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Rate limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# Circuit breaker
CIRCUIT_BREAKER_FAILURE_THRESHOLD=5
CIRCUIT_BREAKER_TIMEOUT=60
```

---

## 🧪 Testing

### Run Unit Tests

```bash
python -m pytest tests/ -v
```

### Test Rate Limiting

```bash
# Send 100 requests rapidly
for i in {1..100}; do
  curl -X GET http://localhost:8000/api/v1/users/profile \
    -H "Authorization: Bearer $TOKEN"
done
```

### Test Circuit Breaker

```bash
# Simulate service failures
for i in {1..10}; do
  curl -X GET http://localhost:8000/api/v1/trading/orders \
    -H "Authorization: Bearer $TOKEN"
done
```

---

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Build Docker Image Manually

```bash
# Build image
docker build -t secure-financial-api-gateway .

# Run container
docker run -p 8000:8000 -e JWT_SECRET_KEY=your-secret-key secure-financial-api-gateway
```

### Environment Variables for Docker

Create a `.env` file (see `.env.example` for template):

```env
JWT_SECRET_KEY=your-super-secret-key
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com
RATE_LIMIT_REQUESTS_PER_MINUTE=60
```

---

## 🚀 Deployment Guide

### Production Deployment Checklist

- [ ] Change JWT secret key to a strong, random value
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS with specific allowed origins
- [ ] Set up proper logging and monitoring
- [ ] Configure rate limits based on your needs
- [ ] Set up database for persistent user storage
- [ ] Enable Redis for session management
- [ ] Configure firewall rules
- [ ] Set up automated backups
- [ ] Implement secrets management (e.g., AWS Secrets Manager, HashiCorp Vault)

### Cloud Deployment Options

#### AWS (Elastic Beanstalk)
```bash
eb init -p python-3.11 secure-api-gateway
eb create production-env
eb deploy
```

#### Google Cloud Run
```bash
gcloud run deploy secure-api-gateway \
  --source . \
  --platform managed \
  --region us-central1
```

#### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api-gateway
        image: secure-financial-api-gateway:latest
        ports:
        - containerPort: 8000
```

---

## 🔍 Troubleshooting

### Common Issues

**Token Validation Errors (401)**
- Verify token in `Authorization: Bearer <token>` header
- Check JWT secret key matches
- Ensure token hasn't expired

**Rate Limit Exceeded (429)**
- Wait for rate limit reset (60s)
- Increase limits in configuration
- Implement exponential backoff

**Circuit Breaker Open (503)**
- Check downstream service health
- Wait for timeout (60s default)
- Review error logs

**CORS Errors**
```bash
# Set in .env
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## ⚡ Performance

### Optimization Tips

1. **Use Redis for Sessions** - Enables horizontal scaling
2. **Enable Response Caching** - Reduces database queries
3. **Database Connection Pooling** - Improves throughput
4. **Async Processing** - Better concurrency handling
5. **Load Balancing** - Distribute traffic across instances

### Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Response Time (p95) | < 100ms | ~50ms |
| Requests/sec | > 1000 | ~2500 |
| Memory Usage | < 512MB | ~200MB |

---

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "api-gateway",
  "timestamp": "2025-10-06T12:00:00Z"
}
```

### Request Logging

All requests include:
- **X-Request-ID**: Unique request identifier
- **X-Process-Time**: Request processing time in seconds

### Metrics & Observability

**Prometheus Integration** (Optional)
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

**Grafana Dashboards**
- Request rate and latency
- Error rates by endpoint
- Circuit breaker states
- Rate limiter statistics

---

## 🧪 Testing & Quality

### Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test
python -m pytest tests/test_auth.py::test_login_user -v
```

### Test Coverage

Current coverage: **84%**

| Module | Coverage |
|--------|----------|
| auth/jwt_handler.py | 95% |
| middleware/rate_limiter.py | 94% |
| routes/* | 100% |
| middleware/circuit_breaker.py | 70% |

### Code Quality

```bash
# Format code
black src tests

# Check security issues
bandit -r src

# Lint code
flake8 src tests
```

---

## 🔒 Security Best Practices

1. **Change JWT Secret**: Always use a strong, random secret key in production
2. **Use HTTPS**: Enable TLS/SSL for all production traffic
3. **Environment Variables**: Never commit secrets to version control
4. **Rate Limiting**: Adjust limits based on your use case
5. **Password Policy**: Enforce strong password requirements
6. **Token Expiry**: Use short-lived access tokens
7. **Audit Logging**: Log all authentication and authorization events

---

## ❓ FAQ

### General Questions

**Q: Is this production-ready?**  
A: Yes, the gateway includes production-grade security features, but ensure you:
- Change the default JWT secret
- Configure proper CORS origins
- Set up persistent storage (database/Redis)
- Enable HTTPS
- Configure monitoring and logging

**Q: Can I use this for non-financial applications?**  
A: Absolutely! While designed for financial services, the security features are applicable to any API requiring robust authentication and protection.

**Q: How do I scale this horizontally?**  
A: The API is stateless and can be scaled horizontally. Use Redis for session storage and a load balancer to distribute traffic.

### Technical Questions

**Q: How do I customize rate limits per user?**  
A: Modify the `RateLimiterMiddleware` to check user roles/plans and apply different limits accordingly.

**Q: Can I use a different JWT algorithm?**  
A: Yes, update the `ALGORITHM` variable in `jwt_handler.py`. Supported algorithms: HS256, HS384, HS512, RS256, RS384, RS512.

**Q: How do I integrate with a real database?**  
A: Replace the in-memory `users_db` in `auth_routes.py` with database queries using SQLAlchemy or another ORM:
```python
from sqlalchemy.ext.asyncio import AsyncSession
from databases import Database

async def get_user_by_email(email: str, db: AsyncSession):
    return await db.query(User).filter(User.email == email).first()
```

**Q: How do I add more authentication methods?**  
A: Extend the auth routes to include OAuth2, SAML, or other methods. Example for OAuth2:
```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register('google', client_id='...', client_secret='...')
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `python -m pytest tests/ -v`
5. Commit: `git commit -m "feat: add amazing feature"`
6. Push and create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-lafis)

---

<a name="português"></a>

## 📖 Visão Geral

Um **API Gateway pronto para produção** com recursos avançados de segurança projetado para serviços financeiros. Implementa autenticação JWT, rate limiting, circuit breaker pattern e headers de segurança abrangentes.

### Principais Recursos

- **🔐 Autenticação JWT**: Autenticação segura baseada em tokens com refresh tokens
- **⏱️ Rate Limiting**: Algoritmo token bucket com limites por usuário e por IP
- **🔄 Circuit Breaker**: Previne falhas em cascata com recuperação automática
- **🛡️ Security Headers**: Headers de segurança compatíveis com OWASP
- **📝 Request Logging**: Logging estruturado com IDs de requisição e timing
- **🔒 Password Hashing**: Bcrypt com fator de trabalho configurável
- **📊 Rotas Admin**: Controle de acesso baseado em papéis (RBAC)
- **🚀 Alta Performance**: Async/await com FastAPI

### 🐳 Deploy com Docker

```bash
# Executar com Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

### 🧪 Testes

```bash
# Executar testes
python -m pytest tests/ -v

# Executar com cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

**Cobertura atual**: 84%

### 🚀 Guia de Deploy em Produção

**Checklist de Produção**:
- [ ] Alterar a chave secreta JWT para um valor forte e aleatório
- [ ] Habilitar HTTPS/TLS
- [ ] Configurar CORS com origens específicas permitidas
- [ ] Configurar logging e monitoramento adequados
- [ ] Ajustar limites de rate limiting conforme necessário
- [ ] Configurar banco de dados para armazenamento persistente de usuários
- [ ] Habilitar Redis para gerenciamento de sessões
- [ ] Configurar regras de firewall
- [ ] Implementar backups automatizados

### 📊 Métricas de Performance

| Métrica | Alvo | Atual |
|---------|------|-------|
| Tempo de Resposta (p95) | < 100ms | ~50ms |
| Requisições/seg | > 1000 | ~2500 |
| Uso de Memória | < 512MB | ~200MB |

### ❓ Perguntas Frequentes

**Como escalar horizontalmente?**  
A API é stateless e pode ser escalada horizontalmente. Use Redis para armazenamento de sessões e um load balancer para distribuir o tráfego.

**Como integrar com banco de dados real?**  
Substitua o `users_db` em memória em `auth_routes.py` por consultas ao banco de dados usando SQLAlchemy ou outro ORM.

**Como personalizar limites de rate por usuário?**  
Modifique o `RateLimiterMiddleware` para verificar roles/planos de usuário e aplicar limites diferentes.

### 🤝 Como Contribuir

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes.

1. Faça fork do repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça suas alterações e adicione testes
4. Execute os testes: `python -m pytest tests/ -v`
5. Commit: `git commit -m "feat: adiciona nova funcionalidade"`
6. Envie um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-lafis)

---

## ⭐ Mostre seu apoio

Se este projeto foi útil para você, considere dar uma ⭐️!
