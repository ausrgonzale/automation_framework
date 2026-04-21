# Automation Framework — Complete Target System Architecture & Filesystem Placement

This document now combines:

* The **original target system architecture**
* The **concrete filesystem and package placement** for implementation
* A **developer-ready structure** that shows both system design and where code lives

This unified document is intended to be the **single source of truth** for developers building the Automation Framework.

It supports onboarding, planning, and implementation of the AI‑driven QA automation platform.

---

# Status Legend

| Status         | Meaning                   |
| -------------- | ------------------------- |
| ✅ COMPLETE     | Implemented and stable    |
| 🟡 IN PROGRESS | Actively being integrated |
| ⬜ PLANNED      | Not yet implemented       |

---

# System Design Principles

This architecture follows:

* Separation of concerns
* Agent-driven orchestration
* Pluggable tool execution
* Provider independence
* Testability
* Observability
* Incremental extensibility

---

# Full Target System Architecture

```text
+------------------------------------------------------------------+
|                     USER / CI / API / SCHEDULER                  |
|------------------------------------------------------------------|
| CLI | REST API | CI/CD Pipeline | Batch Jobs | Scheduled Runs    |
+-------------------------------+----------------------------------+
                                |
                                v

+------------------------------------------------------------------+
|                     ORCHESTRATION AGENT                          |
+-------------------------------+----------------------------------+
        |              |              |              |
        v              v              v              v

+--------------+  +--------------+  +--------------+  +--------------+
| SearchAgent  |  | CodingAgent  |  | TestCaseAgent|  | ExecutionAgent|
+--------------+  +--------------+  +--------------+  +--------------+

                               |
                               v

+------------------------------------------------------------------+
|                         MCP LAYER                                |
+------------------------------------------------------------------+

                               |
                               v

+------------------------------------------------------------------+
|                       SYSTEM CAPABILITIES                        |
+------------------------------------------------------------------+

                               |
                               v

+------------------------------------------------------------------+
|                        EXTERNAL SYSTEMS                          |
+------------------------------------------------------------------+
| OpenAI | Anthropic | Ollama | Jira | TestRail | CI | Database    |
+------------------------------------------------------------------+
```

---

# Unified Repository Filesystem Structure (IMPLEMENTATION VIEW)

This section defines the **actual directory structure** developers will use when building the system.

```text
automation_framework/
│
├── ai/
│   └── agents/
│
├── clients/
├── config/
├── core/
├── domain/
├── execution/
├── integrations/
├── mcp/
│   └── tools/
│
├── repositories/
├── services/
├── tests/
├── utils/
│
├── main.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

This structure aligns directly with the architectural layers defined above.

---

# Agent Layer — Implementation Placement

Directory:

```text
ai/agents/
```

Files:

```text
ai/agents/
│
├── orchestration_agent.py
├── search_agent.py
├── coding_agent.py
├── testcase_agent.py
├── execution_agent.py
│
└── __init__.py
```

Responsibilities:

* Coordinate workflows
* Call services
* Use repositories
* Remain infrastructure-agnostic

---

# Services Layer — Business Logic

Directory:

```text
services/
```

Files:

```text
services/
│
├── testcase_generation_service.py
├── validation_service.py
├── execution_service.py
│
└── __init__.py
```

Responsibilities:

* Implement workflows
* Validate inputs
* Call repositories
* Call AI clients

---

# Repository Layer — Persistence

Directory:

```text
repositories/
```

Files:

```text
repositories/
│
├── testcase_repository.py
├── file_repository.py
├── excel_repository.py
├── testrail_repository.py
├── database_repository.py
│
└── __init__.py
```

Responsibilities:

* Store test cases
* Retrieve test cases
* Support multiple backends

---

# AI Client Layer — Provider Integration

Directory:

```text
clients/
```

Files:

```text
clients/
│
├── ai_client_factory.py
├── openai_client.py
├── anthropic_client.py
├── ollama_client.py
│
└── __init__.py
```

Responsibilities:

* Provider selection
* Authentication
* Retry handling
* Timeout configuration

---

# Domain Layer — System Contracts

Directory:

```text
domain/
```

Files:

```text
domain/
│
├── models.py
│
└── __init__.py
```

Responsibilities:

* Define request/response models
* Define data structures
* Remain infrastructure-free

---

# Execution Layer — Test Running

Directory:

```text
execution/
```

Files:

```text
execution/
│
├── pytest_runner.py
├── playwright_runner.py
├── result_collector.py
│
└── __init__.py
```

Responsibilities:

* Run automation
* Capture results
* Return execution status

---

# MCP Layer — Tool Execution

Directory:

```text
mcp/
```

Subdirectories:

```text
mcp/
│
├── registry/
├── client/
├── tools/
│
└── __init__.py
```

---

# Configuration Layer — Dependency Wiring

Directory:

```text
config/
```

Files:

```text
config/
│
├── settings.py
├── dependency_container.py
│
└── __init__.py
```

Responsibilities:

* Build system objects
* Wire dependencies
* Configure providers

---

# Core Infrastructure Layer

Directory:

```text
core/
```

Files:

```text
core/
│
├── logger.py
├── exceptions.py
├── retry.py
│
└── __init__.py
```

---

# Utilities Layer

Directory:

```text
utils/
```

Files:

```text
utils/
│
├── file_utils.py
├── json_utils.py
│
└── __init__.py
```

---

# Testing Layer

Directory:

```text
tests/
```

Structure:

```text
tests/
│
├── agents/
├── services/
├── repositories/
├── execution/
│
└── conftest.py
```

---

# End-to-End Target Workflow

```text
Requirement
     ↓
OrchestrationAgent
     ↓
TestCaseAgent
     ↓
Repository
     ↓
ExecutionAgent
     ↓
Result Collector
     ↓
Reporting
```

---

# Developer Build Guidance

New developers should:

1. Implement logic inside services
2. Keep agents thin
3. Use repositories for persistence
4. Keep domain models pure
5. Wire dependencies in config

---

# Current System Maturity (Updated View)

Infrastructure:

100% complete

Agents:

75% complete

Workflows:

30% complete

Platform:

10% complete

---

# One‑Sentence System Definition

The Automation Framework is an agent‑driven automation platform where AI makes decisions and tools execute actions in a consistent, extensible architecture with clearly defined filesystem placement for implementation.

---

# Current State Summary (Implementation Reality — April 2026)

This section reflects the **actual current system state** so development can continue without ambiguity. It aligns the target architecture with the working implementation baseline provided in the handoff summary.

---

## Core Runtime Pipeline — Verified Working

```text
User
   ↓
Agent
   ↓
AI Client
   ↓
MCP Client
   ↓
Tool
   ↓
System Action
```

This pipeline is stable and validated in production-style testing scenarios.

---

## Implemented Components (Confirmed Stable)

Infrastructure:

* MCP registry and client
* Filesystem tools (except file_exists)
* AI client integrations (OpenAI and Anthropic)
* Centralized logging configuration
* Unit test coverage for tools and registry
* SearchAgent CLI workflow
* CodingAgent file generation workflow

These components form the **reliable execution foundation** of the platform.

---

## Partially Implemented Components

TestCaseAgent:

Status: 🟡 IN PROGRESS

Current State:

* Agent structure exists
* Prompt logic started
* AI generation partially implemented

Remaining Work:

* Repository integration
* Validation workflow
* Execution trigger

Client Factory:

Status: 🟡 IN PROGRESS

Remaining Work:

* Provider selection via configuration
* Support for additional providers (Ollama, Azure, Bedrock)

Integration Tests:

Status: 🟡 IN PROGRESS

Purpose:

* Validate cross-component workflows

---

## Not Yet Implemented (Confirmed Gaps)

ExecutionAgent

OrchestrationAgent

Repository abstraction layer

Execution runners (pytest / Playwright)

External system integrations

Reporting system

End-to-end workflows

These represent the next major capability milestones for the platform.

---

## Current Directory Structure (Verified Runtime Layout)

```text
automation_framework/

ai/
    agents/
        search_agent.py
        coding_agent.py
        testcase_agent.py

    prompts/
    schemas/
    utils/

config/
    logging_config.py
    openai_client.py
    anthropic_client.py
    client_factory.py

mcp/
    client.py
    registry.py
    registry_setup.py
    tool.py

    tools/
        filesystem/

repositories/
execution/
integrations/

tests/
docs/
pytest.ini
```

This reflects the **real operational state**, not the theoretical target structure.

---

## Immediate Next Development Targets (Execution Order)

1. Implement file_exists_tool

2. Finish TestCaseAgent workflow

3. Add repository abstraction

4. Build ExecutionAgent

5. Introduce OrchestrationAgent

This order minimizes architectural risk and preserves system stability.

---

## System Readiness Snapshot

Infrastructure:

100 percent complete

Agents:

75 percent complete

Workflow capability:

30 percent complete

Platform capability:

10 percent complete

---

## Practical Interpretation for Developers

The platform foundation is complete.

The remaining work is **capability layering**, not infrastructure building.

Focus should remain on:

* finishing agent workflows
* adding persistence
* enabling execution
* coordinating orchestration

Not rebuilding core infrastructure.

---

# Implementation — file_exists_tool

File Location:

```text
mcp/tools/filesystem/file_exists_tool.py
```

Purpose:

Provide a standardized, safe way to check whether a file or directory exists. This tool is used by repositories, execution logic, and orchestration workflows to make deterministic decisions before performing filesystem operations.

---

## Production Implementation

```python
"""
file_exists_tool.py

Filesystem capability:

Check whether a file or directory exists.

This tool is intentionally simple and deterministic.
It should NEVER raise an exception for a normal
non-existent path — it should return False.
"""

from pathlib import Path

from mcp.tool import Tool
from config.logging_config import get_logger

logger = get_logger(__name__)


class FileExistsTool(Tool):
    """
    MCP Tool: file_exists

    Input:

        {
            "path": "string"
        }

    Output:

        {
            "exists": bool
        }
    """

    name = "file_exists"

    description = "Check whether a file or directory exists"

    def execute(self, path: str) -> dict:
        """
        Determine if the provided path exists.
        """

        logger.debug("file_exists called", extra={
            "path": path
        })

        try:
            exists = Path(path).exists()

            logger.debug("file_exists result", extra={
                "path": path,
                "exists": exists
            })

            return {
                "exists": exists
            }

        except Exception as exc:

            logger.exception(
                "file_exists failed",
                extra={
                    "path": path
                }
            )

            raise
```

---

## Registry Registration Step

Update:

```text
mcp/registry_setup.py
```

Add:

```python
from mcp.tools.filesystem.file_exists_tool import (
    FileExistsTool,
)
```

Then register the tool:

```python
registry.register(FileExistsTool())
```

Place this alongside the other filesystem tool registrations.

---

## Unit Test — Required

File Location:

```text
tests/mcp/tools/filesystem/test_file_exists_tool.py
```

Implementation:

```python
from pathlib import Path

from mcp.tools.filesystem.file_exists_tool import (
    FileExistsTool,
)


def test_file_exists_returns_true(tmp_path):

    file_path = tmp_path / "test.txt"

    file_path.write_text("hello")

    tool = FileExistsTool()

    result = tool.execute(
        path=str(file_path)
    )

    assert result["exists"] is True


def test_file_exists_returns_false(tmp_path):

    file_path = tmp_path / "missing.txt"

    tool = FileExistsTool()

    result = tool.execute(
        path=str(file_path)
    )

    assert result["exists"] is False
```

---

## Definition of Done

The capability is complete when:

* file_exists_tool.py implemented
* Tool registered in registry_setup
* Unit tests created
* All tests pass
* Tool callable from agents

---

## What This Unlocks Next

Immediately after this tool is complete, the next safe development target is:

Finish TestCaseAgent workflow

Because that workflow will rely on deterministic filesystem checks before saving test artifacts.
