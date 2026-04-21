# Configuration System Overview

The framework uses a single consolidated configuration file for simplicity and platform independence.

## Configuration File

```
config/config.yaml
```

This single file contains all settings organized into sections:
- `framework` - Core system settings
- `execution` - Test execution parameters
- `ai` - AI provider configurations
- `providers` - External service integrations
- `environments` - Environment-specific overrides
- `projects` - Project-specific settings

## Environment Variables

Sensitive data uses environment variables:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `JIRA_USERNAME`, `JIRA_API_TOKEN`
- `TESTRAIL_USERNAME`, `TESTRAIL_API_KEY`

## Usage Examples

```bash
# Local development
export ENVIRONMENT=local
python -m scripts.generate_tests

# CI/CD
export ENVIRONMENT=ci
export OPENAI_API_KEY=...
python -m scripts.run_tests

# Custom project
export PROJECT=myproject
python -m scripts.generate_tests
```

## Benefits

- **Minimal Files**: Single config file reduces complexity
- **Modular**: Sectioned organization maintains separation of concerns
- **Platform Independent**: Environment-driven, no hardcoded paths
- **Extensible**: Easy to add new providers or environments