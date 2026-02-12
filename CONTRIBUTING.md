# Contributing to Secure Financial API Gateway

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/secure-financial-api-gateway.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## 💻 Development Setup

### Prerequisites

- Python 3.12+
- pip package manager
- Docker (optional, for containerized development)

### Installation

```bash
# Clone the repository
git clone https://github.com/galafis/secure-financial-api-gateway.git
cd secure-financial-api-gateway

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run tests
python -m pytest tests/ -v
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🔧 Making Changes

1. **Create a feature branch**: `git checkout -b feature/amazing-feature`
2. **Make your changes**: Follow the coding standards below
3. **Test your changes**: Ensure all tests pass
4. **Commit your changes**: Use clear, descriptive commit messages
   ```bash
   git commit -m "feat: add amazing feature"
   ```

### Commit Message Convention

We follow the Conventional Commits specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, missing semicolons, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_auth.py -v
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow existing test patterns

Example:
```python
def test_feature_works_correctly():
    """Test that the feature works as expected"""
    # Arrange
    expected_result = "success"
    
    # Act
    result = my_function()
    
    # Assert
    assert result == expected_result
```

## 📝 Pull Request Process

1. **Update documentation**: If you've changed APIs, update the relevant documentation
2. **Add tests**: Ensure your code is tested
3. **Run the test suite**: All tests must pass
4. **Update CHANGELOG.md**: Add your changes under "Unreleased"
5. **Submit PR**: Provide a clear description of the changes

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
```

## 🎨 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

### Code Quality Tools

```bash
# Format code with black
black src tests

# Sort imports with isort
isort src tests

# Run linter
flake8 src tests

# Security check
bandit -r src
```

### Documentation

- Use clear, concise language
- Include code examples where helpful
- Update README.md for user-facing changes
- Add inline comments for complex logic

## 🐛 Reporting Bugs

When reporting bugs, include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Screenshots (if applicable)

## 💡 Suggesting Enhancements

For feature requests:

- Describe the feature clearly
- Explain the use case
- Provide examples if possible
- Discuss potential implementation approaches

## 📞 Getting Help

- Open an issue for bugs or feature requests
- Join discussions in existing issues
- Contact the maintainer: [@galafis](https://github.com/galafis)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing!
