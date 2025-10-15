# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with 84% code coverage
- GitHub Actions CI/CD pipeline with automated testing
- Docker and Docker Compose support for containerized deployment
- Environment configuration template (.env.example)
- Contributing guidelines (CONTRIBUTING.md)
- Security policy (SECURITY.md)
- FAQ section in README
- Deployment guides for AWS, GCP, Azure, and Kubernetes
- Troubleshooting guide
- Performance optimization tips
- Enhanced Portuguese documentation

### Changed
- Fixed JWT handler to use timezone-aware datetime (removed deprecation warnings)
- Fixed JWT exception handling to use correct PyJWT exception classes
- Enhanced README with more badges, sections, and examples
- Improved test organization with pytest.ini configuration

### Security
- Added Bandit security scanning to CI/CD pipeline
- Added Safety dependency vulnerability scanning
- Enhanced security documentation

## [1.0.0] - 2025-10-06

### Added
- Initial release
- Core functionality implemented
- Comprehensive test suite
- Documentation and examples
- CI/CD pipeline

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## Release Notes

### Version 1.1.0 (Upcoming)

**Highlights:**
- Enhanced test coverage (84%)
- Docker support for easy deployment
- Comprehensive CI/CD pipeline
- Improved documentation and guides
- Security hardening

**Breaking Changes:**
- None

**Contributors:**
- Gabriel Demetrios Lafis

### Version 1.0.0 (2025-10-06)

**Highlights:**
- First stable release
- Production-ready code
- Full documentation
- Extensive test coverage

**Contributors:**
- Gabriel Demetrios Lafis

---

[Unreleased]: https://github.com/galafis/secure-financial-api-gateway/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/galafis/secure-financial-api-gateway/releases/tag/v1.0.0
