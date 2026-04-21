# Unified AI Client Configuration Plan

## Purpose

Design and implement a single, centralized AI client configuration layer that allows agents to dynamically select the appropriate AI provider at runtime. This architecture enables cost control, portability, and consistent behavior across local development, CI/CD pipelines, and production environments.

The system will support multiple providers, including:

- Ollama (local default)
- Anthropic
- OpenAI

---

## Design Goals

- Provide a **single client configuration entry point** for all agents
- Allow runtime selection of AI provider via environment variables
- Default to a **local provider (Ollama)** to reduce usage costs
- Maintain portability across environments (local, Docker, CI, production)
- Avoid provider-specific logic inside agent code
- Enable future provider expansion without refactoring agents

---

## Core Architectural Principle

Agents should never directly instantiate provider clients.

Instead, they should call a centralized factory:

```python
client = get_ai_client()
```

The factory determines which provider to use.

---

## Target Directory Structure

```
agents/

    config/
        settings.py
        ai_provider.py
        client_factory.py

    providers/
        openai_client.py
        anthropic_client.py
        ollama_client.py
```

---

## Provider Selection Mechanism

Provider selection will be controlled using a single environment variable:

```
AI_PROVIDER
```

### Example Values

```
AI_PROVIDER=ollama
AI_PROVIDER=anthropic
AI_PROVIDER=openai
```

---

## Default Behavior

If the variable is not set:

```
AI_PROVIDER=ollama
```

This ensures local development defaults to a cost-free local model.

---

## Example Settings Module

File:

```
config/settings.py
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")
```

---

## Client Factory Implementation

File:

```
config/client_factory.py
```

```python
from config.settings import AI_PROVIDER

from providers.anthropic_client import get_anthropic_client
from providers.openai_client import get_openai_client
from providers.ollama_client import get_ollama_client


def get_ai_client():

    if AI_PROVIDER == "anthropic":
        return get_anthropic_client()

    if AI_PROVIDER == "openai":
        return get_openai_client()

    if AI_PROVIDER == "ollama":
        return get_ollama_client()

    raise RuntimeError(f"Unknown AI provider: {AI_PROVIDER}")
```

---

## Agent Usage Pattern

Agents must use the factory instead of provider-specific code.

```python
from config.client_factory import get_ai_client

client = get_ai_client()
```

This ensures provider independence.

---

## Ollama Integration Strategy

Ollama will be the default provider for:

- Local development
- Iterative testing
- Cost-sensitive workflows
- Offline experimentation

### Example Local Configuration

```
AI_PROVIDER=ollama
OLLAMA_MODEL=llama3
```

---

## Cloud Provider Usage Strategy

Cloud providers will be used when:

- Higher reasoning capability is required
- CI/CD pipelines need deterministic execution
- Production workloads require reliability

### Example CI Configuration

```
AI_PROVIDER=anthropic
```

---

## Docker Integration (Future)

Ollama will run as a service within Docker Compose.

Example:

```yaml
services:

  learning-log:
    build: ./apps/learning-log

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
```

Agents will connect to:

```
http://localhost:11434
```

---

## Environment Strategy

| Environment | Provider |
|------------|----------|
| Local Development | Ollama |
| CI / GitHub Actions | Anthropic |
| Production | Anthropic or OpenAI |

---

## Future Enhancements

Potential capabilities enabled by this architecture:

- Provider fallback logic
- Load balancing across providers
- Cost-aware routing
- Model capability selection
- Multi-provider orchestration
- Offline testing support

---

## Implementation Timing

This work should begin only after the following infrastructure milestones are completed:

1) Learning Log application containerized
2) Playwright tests running against container
3) GitHub Actions CI pipeline stable
4) Deterministic test execution confirmed

---

## Summary

This design introduces a centralized AI client configuration system that enables flexible provider selection while keeping agent code simple and maintainable.

Key outcomes:

- Single client entry point
- Provider abstraction
- Local-first default (Ollama)
- Cloud-ready execution
- Cost-efficient development workflow

