# GitHub Actions Setup

This document explains how to configure GitHub Actions for the automation framework.

## Environment Variables

The framework uses environment variables for configuration. In GitHub Actions, these are set through repository secrets and workflow environment variables.

### Required Secrets

Set these as repository secrets in GitHub (Settings → Secrets and variables → Actions):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI-powered test generation | `sk-proj-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional, for Claude) | `sk-ant-api03-...` |
| `SEARCH_API_KEY` | Search API key (optional) | `...` |

### How to Set Secrets

1. Go to your GitHub repository
2. Click **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter the secret name and value
6. Click **Add secret**

### Workflow Configuration

The `.github/workflows/pytest.yml` file includes:

```yaml
env:
  AI_PROVIDER: openai  # Uses OpenAI in CI (Ollama not available)
  AI_MODEL: gpt-4o
  AI_RETRIES: 3
  AI_RETRY_DELAY: 1
  AI_RETRY_BACKOFF: 2

  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  SEARCH_API_KEY: ${{ secrets.SEARCH_API_KEY }}
```

### Local Development (.env)

For local development, create a `.env` file in the project root:

```bash
# AI Configuration
AI_PROVIDER=ollama
AI_MODEL=llama3.1:latest
AI_RETRIES=3
AI_RETRY_DELAY=1
AI_RETRY_BACKOFF=2

# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
SEARCH_API_KEY=your_search_key_here
```

### Differences: Local vs CI

| Setting | Local (.env) | CI (GitHub Actions) |
|---------|--------------|---------------------|
| `AI_PROVIDER` | `ollama` | `openai` |
| `AI_MODEL` | `llama3.1:latest` | `gpt-4o` |
| API Keys | Direct values | GitHub secrets |

This setup ensures:
- Sensitive data is never committed to the repository
- Local development uses Ollama (free, local)
- CI/CD uses OpenAI (reliable, cloud-based)
- Platform independence is maintained