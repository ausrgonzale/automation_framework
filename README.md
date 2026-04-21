# Automation Framework

This project is a portable, modular AI-driven test automation framework designed to support scalable UI and API testing across multiple applications.

The framework is intentionally application-agnostic, deterministic, and built using industry-standard tools. It is evolving into a full automation platform capable of generating, storing, executing, and orchestrating automated tests using AI agents.

---

## Platform Vision

The framework is designed to evolve into a complete automation platform supporting:

* UI automation
* API automation
* AI-generated test cases
* Parallel test execution
* Containerized test environments
* Multi-application test support
* Distributed execution orchestration
* Persistent job and workflow management

---

## Core Capabilities

* Supports multiple applications without code coupling
* Enforces deterministic test behavior
* AI-driven test generation and execution
* Modular repository and storage backends
* Extensible agent-based architecture
* Container-friendly execution model
* Scalable orchestration using Redis

---

# Project Structure

```text
automation-framework/

ai/
    agents/
        base_agent.py
        orchestration_agent.py
        coding_agent.py
        execution_agent.py

    clients/
        client_factory.py

    utils/
        story_normalizer.py

mcp/
    excel/
        excel_tool.py
        excel_repositories.py

repositories/
    test_case_repository.py

scripts/
    generate_tests.py

tests/
    unit/
    integration/
    e2e/
        test_login.py
        test_user_registration.py
        test_topics.py
        test_topic_entries.py

documentation/
    architecture.md
    design.md
    implementation_plan.md

docker/
    redis/
        start_redis.sh

conftest.py
README.md
```

---

# Agent Architecture

The framework uses a modular agent-based system to coordinate AI-driven test workflows.

## Orchestration Agent

The Orchestration Agent is the central coordinator responsible for managing automation workflows across the system.

Responsibilities:

* Accept workflow requests
* Coordinate AI agents
* Manage execution pipelines
* Dispatch tasks
* Track workflow state
* Ensure deterministic execution
* Interface with Redis for job persistence

The Orchestration Agent enables the system to scale from:

Single test execution
→ Distributed workflow orchestration
→ Full automation platform

---

## Coding Agent

Responsible for generating automation code.

Responsibilities:

* Generate pytest test cases
* Produce Playwright automation scripts
* Validate generated code
* Ensure framework compatibility

---

## Execution Agent

Responsible for executing tests and reporting results.

Responsibilities:

* Run pytest
* Capture logs and results
* Return execution status
* Support parallel execution

---

# Redis Integration

Redis is used as the runtime coordination and persistence layer for orchestration workflows.

It enables reliable distributed execution and future horizontal scaling.

---

## Redis Responsibilities

* Job queue management
* Workflow state persistence
* Task coordination
* Retry handling
* Distributed worker communication
* Execution tracking

---

## Redis Architecture Role

```text
User Request
     │
     ▼
Orchestration Agent
     │
     ▼
Redis
     │
     ├── Job Queue
     ├── Workflow State
     └── Worker Coordination
```

---

## Starting Redis

Start Redis container:

```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7
```

Or using the provided script:

```bash
./docker/redis/start_redis.sh
```

---

## Redis Configuration

Default connection:

```text
Host: localhost
Port: 6379
Database: 0
```

Environment configuration:

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

---

# Technology Stack

Core Technologies:

* Python
* pytest
* Playwright
* Redis
* Docker

AI Providers:

* OpenAI
* Anthropic
* Ollama

---

## Planned Infrastructure

* pytest-xdist
* Distributed workers
* Kubernetes-ready deployment
* Persistent workflow storage
* Retry and recovery workflows
* Observability and metrics

---

# Design Philosophy

This framework emphasizes:

Reliability over speed
Consistency over shortcuts
Determinism over randomness
Architecture over scripts
Automation over manual workflows

---

# Troubleshooting & Test Setup

## Import / Module Errors

Example:

```text
ModuleNotFoundError: No module named 'repositories.excel_repository'
```

Fix:

Always run pytest from the project root directory:

```bash
export PYTHONPATH=.
pytest
```

Also ensure:

* Every package directory contains `__init__.py`
* Virtual environment is activated
* Dependencies are installed

---

## Redis Connection Errors

Example:

```text
ConnectionError: Redis connection failed
```

Fix:

Verify Redis is running:

```bash
docker ps
```

Expected output:

```text
redis   Up   6379/tcp
```

Restart Redis:

```bash
docker restart redis
```

---

## Pytest Warnings: Test Class `__init__`

Pytest cannot collect test classes with a custom `__init__` method.

Use:

```python
setup_method()
teardown_method()
```

Instead of:

```python
__init__()
```

---

# Configuration

## Local Development

Create a `.env` file in the project root:

```bash
# AI Configuration
AI_PROVIDER=ollama
AI_MODEL=llama3.1:latest

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

---

# CI/CD

## GitHub Actions

Configure repository secrets and see:

docs/GitHub_Actions_Setup.md

The CI workflow automatically:

* Runs tests
* Validates generated code
* Executes automation workflows

---

# Versioning

The project follows semantic versioning.

```text
v0.1.0 — Framework initialization  
v0.2.0 — Core authentication workflows  
v0.3.0 — Topic and entry CRUD workflows  
v0.4.0 — AI-driven test generation  
v0.5.0 — Orchestration Agent and Redis integration  
```

---

# Future Enhancements

Planned capabilities include:

* Distributed worker execution
* Workflow retries and recovery
* Persistent workflow storage
* Parallel execution scaling
* Test reporting and analytics
* Multi-application orchestration
* API-level automation
* Containerized execution environments
