# Automation Framework — Project Summary
**As of: April 24, 2026**

---

## What This Framework Is

A modular, AI-driven test automation platform designed to be application-agnostic. The core vision is to generate, store, and orchestrate automated tests using AI agents across multiple applications.

---

## Architecture Overview

| Layer | Status | Description |
|---|---|---|
| **AI Agents** | Built | `OrchestrationAgent`, `CodingAgent`, `SearchAgent`, `TestcaseGenerationAgent` |
| **AI Providers** | Built | Abstracted clients for OpenAI, Anthropic, and Ollama (local) |
| **Testcase Generation Service** | Built | Core service that generates test cases from requirements |
| **Story Normalizer** | Built | Normalizes Jira/Excel user stories to a canonical format |
| **Repositories** | Built | CSV/Excel persistence via template-driven `CsvRepository` |
| **MCP Integrations** | Partial | Excel and Jira integrations in `mcp/`, registry/client abstractions defined |
| **Orchestration Script** | Built | `scripts/orchestrate_test_generation.py` — reads CSV stories → normalizes → generates → writes output |
| **NL Orchestration Runner** | Built | `run_nl_orchestration.py` — natural language command interface to the `OrchestrationAgent` |
| **Redis Queue** | Integrated | `OrchestrationAgent` enqueues jobs into Redis for async processing |

---

## Project Structure

```
ai/
    agents/         # OrchestrationAgent, CodingAgent, SearchAgent, TestcaseGenerationAgent
    client_factory.py
    providers/      # OpenAI, Anthropic, Ollama provider adapters
    prompts/        # Prompt builders (testcase_generation)
    schemas/        # CheckCase, CheckCaseSet, CheckcaseGenerationRequest
    utils/          # StoryNormalizer, retry helpers

mcp/
    excel/          # Excel MCP integration
    jira/           # Jira MCP integration
    base/           # Registry, client abstractions, tool definitions

repositories/
    csv_repository.py
    file_repository.py
    testcase_repository.py  # CheckcaseRepository ABC

services/
    testcase_generation_service.py  # CheckcaseGenerationService

scripts/
    generate_tests.py               # AI-powered unit test generation from source files
    orchestrate_test_generation.py  # End-to-end test generation CLI
    normalize_prompt.py

config/             # Centralized config, logging, .env loading

tests/
    unit/           # 17 unit test files covering all framework modules
    integration/    # 4 integration test files
```

---

## E2E Tests Status

Application-specific E2E tests (Django/Playwright) were moved to the separate `pcc-learning-log` project. This repository focuses purely on the framework infrastructure and AI generation pipeline.

---

## Previous Work Completed

### Script Fixes for `scripts/generate_tests.py`
- Fixed Ollama timeout/model loading — switched default from `qwen2.5` → `llama3.1`
- Fixed URL normalization bug in the Ollama provider
- Fixed `CodingAgent` to use `client.generate()` consistently
- Added `load_dotenv()` to `client_factory.py` so env vars load at runtime
- Installed OpenAI SDK dependency

### Pytest Collection Warning Fix
- Added `__test__ = False` to non-test classes whose names started with `Test*`
- Documented a new naming convention: use `Check*` prefix for non-test classes

---

## Work Completed Today (April 24, 2026)

### `Check*` Prefix Refactor

Renamed all non-test classes from the `Test*` prefix to the `Check*` prefix per the team naming convention. Removed all `__test__ = False` guards that were previously added as a workaround.

**Classes renamed:**

| Old Name | New Name | File |
|---|---|---|
| `TestCase` | `CheckCase` | `ai/schemas/testcase.py` |
| `TestCaseSet` | `CheckCaseSet` | `ai/schemas/testcase.py` |
| `TestcaseGenerationRequest` | `CheckcaseGenerationRequest` | `ai/schemas/testcase_generation_request.py` |
| `TestcaseGenerationService` | `CheckcaseGenerationService` | `services/testcase_generation_service.py` |
| `TestcaseRepository` | `CheckcaseRepository` | `repositories/testcase_repository.py` |

**Files updated (23 edits across 13 files):**
- `ai/schemas/testcase.py`
- `ai/schemas/testcase_generation_request.py`
- `ai/agents/testcase_generation_agent.py`
- `ai/prompts/testcase_generation.py`
- `repositories/testcase_repository.py`
- `repositories/file_repository.py`
- `services/testcase_generation_service.py`
- `scripts/orchestrate_test_generation.py`
- `tests/unit/test_testcase_generation_service.py`
- `tests/unit/test_generate_mock_testcase.py`
- `tests/integration/test_generate_ai_testcases.py`

**Test results after refactor:** 42 passed, 2 pre-existing failures (unrelated to this change).

---

## Known Pre-Existing Test Failures

| Test | Reason |
|---|---|
| `test_normalize_prompt_basic` | Assertion expects `"Do not explain"` but prompt text changed |
| `test_run_valid_command` (search agent) | `DummyRegistry` missing `_tools` attribute in test fixture |

These failures existed before today's refactor and require separate investigation.

---

## Quick Start Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all framework tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Generate tests from a source file using AI
python -m scripts.generate_tests

# Run orchestration with a natural language command
python run_nl_orchestration.py "Generate e2e tests for https://... ExampleApp app"
```

---

## Team Naming Convention

> **`Check*`** is the official prefix for non-test classes (schemas, services, repositories, etc.).
> **`Test*`** is reserved exclusively for actual pytest test classes and functions.
