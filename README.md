# 🔐 Secure Financial API Gateway



[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Security](https://img.shields.io/badge/security-hardened-brightgreen.svg)](https://github.com/galafis/secure-financial-api-gateway)



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
