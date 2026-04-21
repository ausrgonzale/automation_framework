# Test Suite Documentation

## Test Structure

This repository contains the core framework tests. Application-specific E2E tests have been moved to the [pcc-learning-log](https://github.com/username/pcc-learning-log) project.

### Directory Structure

```
tests/
├── unit/              # Unit tests for framework components
├── integration/       # Integration tests for service workflows
├── fixtures/          # Test data and shared fixtures
└── conftest.py        # Global test configuration
```

### Test Categories

#### Unit Tests (`tests/unit/`)
- Framework component testing
- AI provider integration
- Utility functions
- Individual service methods

#### Integration Tests (`tests/integration/`)
- AI client integration
- Service orchestration
- End-to-end service workflows
- Cross-component interactions

#### E2E Tests
- **Location**: [pcc-learning-log](https://github.com/username/pcc-learning-log) project
- Application-specific end-to-end scenarios
- Real user workflows
- Full stack testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific categories
pytest tests/unit/
pytest tests/integration/

# Run with markers
pytest -m unit
pytest -m integration
```

### Test Standards

- Every code change requires corresponding unit tests
- Tests follow `test_<filename>.py` naming convention
- Flat test directory structure (no nested subdirectories)
- Comprehensive coverage of success and failure cases