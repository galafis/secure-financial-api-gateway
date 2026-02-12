# 🔒 Secure Financial Api Gateway

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [Português](#português)

---

## English

### 🎯 Overview

**Secure Financial Api Gateway** — Secure API gateway designed for financial services. Features OAuth2/JWT authentication, rate limiting, request validation, TLS encryption, and comprehensive audit trails.

Total source lines: **1,183** across **22** files in **1** language.

### ✨ Key Features

- **Production-Ready Architecture**: Modular, well-documented, and following best practices
- **Comprehensive Implementation**: Complete solution with all core functionality
- **Clean Code**: Type-safe, well-tested, and maintainable codebase
- **Easy Deployment**: Docker support for quick setup and deployment

### 🚀 Quick Start

#### Prerequisites
- Python 3.12+
- Docker and Docker Compose (optional)

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/galafis/secure-financial-api-gateway.git
cd secure-financial-api-gateway
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Running

```bash
python src/main.py
```

## 🐳 Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
```

### 📁 Project Structure

```
secure-financial-api-gateway/
├── docs/
│   ├── FAQ.md
│   ├── USE_CASES.md
│   └── security.md
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── jwt_handler.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── circuit_breaker.py
│   │   ├── rate_limiter.py
│   │   ├── request_logger.py
│   │   └── security_headers.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   ├── trading_routes.py
│   │   └── user_routes.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── test_admin.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_middleware.py
│   ├── test_trading.py
│   └── test_users.py
├── CONTRIBUTING.md
├── README.md
├── SECURITY.md
├── docker-compose.yml
├── pyproject.toml
├── pytest.ini
└── requirements.txt
```

### 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | 22 files |

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👤 Author

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

---

## Português

### 🎯 Visão Geral

**Secure Financial Api Gateway** — Secure API gateway designed for financial services. Features OAuth2/JWT authentication, rate limiting, request validation, TLS encryption, and comprehensive audit trails.

Total de linhas de código: **1,183** em **22** arquivos em **1** linguagem.

### ✨ Funcionalidades Principais

- **Arquitetura Pronta para Produção**: Modular, bem documentada e seguindo boas práticas
- **Implementação Completa**: Solução completa com todas as funcionalidades principais
- **Código Limpo**: Type-safe, bem testado e manutenível
- **Fácil Implantação**: Suporte Docker para configuração e implantação rápidas

### 🚀 Início Rápido

#### Pré-requisitos
- Python 3.12+
- Docker e Docker Compose (opcional)

#### Instalação

1. **Clone the repository**
```bash
git clone https://github.com/galafis/secure-financial-api-gateway.git
cd secure-financial-api-gateway
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Execução

```bash
python src/main.py
```

### 🧪 Testes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
```

### 📁 Estrutura do Projeto

```
secure-financial-api-gateway/
├── docs/
│   ├── FAQ.md
│   ├── USE_CASES.md
│   └── security.md
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   └── jwt_handler.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── circuit_breaker.py
│   │   ├── rate_limiter.py
│   │   ├── request_logger.py
│   │   └── security_headers.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   ├── trading_routes.py
│   │   └── user_routes.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── test_admin.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_middleware.py
│   ├── test_trading.py
│   └── test_users.py
├── CONTRIBUTING.md
├── README.md
├── SECURITY.md
├── docker-compose.yml
├── pyproject.toml
├── pytest.ini
└── requirements.txt
```

### 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| Python | 22 files |

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 👤 Autor

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)
