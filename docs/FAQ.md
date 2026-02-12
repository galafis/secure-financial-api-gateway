# Perguntas Frequentes / FAQ

## O que e este projeto? / What is this project?

Um gateway de API construido com FastAPI que implementa padroes de seguranca para aplicacoes financeiras: autenticacao JWT, rate limiting, circuit breaker e headers de seguranca.

An API gateway built with FastAPI that implements security patterns for financial applications: JWT authentication, rate limiting, circuit breaker, and security headers.

## Posso usar em producao? / Is this production-ready?

O codigo demonstra padroes de producao, mas utiliza armazenamento em memoria e segredos padrao. Antes de implantar:
- Substitua o armazenamento em memoria por um banco de dados
- Configure segredos JWT reais via variaveis de ambiente
- Habilite HTTPS
- Revise as politicas de CORS

The code demonstrates production patterns but uses in-memory storage and default secrets. Before deploying:
- Replace in-memory storage with a database
- Configure real JWT secrets via environment variables
- Enable HTTPS
- Review CORS policies

## Quais sao os requisitos? / What are the requirements?

- Python 3.12+
- pip
- Docker (opcional / optional)

## Como contribuir? / How to contribute?

Leia o arquivo [CONTRIBUTING.md](../CONTRIBUTING.md).

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Como reportar bugs? / How to report bugs?

Abra uma issue no GitHub com descricao do bug, passos para reproduzir e detalhes do ambiente.

Open a GitHub issue with a description, reproduction steps, and environment details.

---

Nao encontrou sua resposta? Abra uma issue no GitHub.

Didn't find your answer? Open an issue on GitHub.
