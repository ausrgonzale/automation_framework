# QA Agent Pipeline Architecture

## Overview

This document describes the architecture of an Agentic AI system designed to automate the full QA lifecycle — from pulling user stories out of Jira, generating and managing test cases in TestRail, writing and executing Playwright/pytest scripts, and reporting results back automatically.

---

## Core Concepts

An agentic AI system is built from four fundamental building blocks:

1. **The LLM** — the brain. Decides what to do, which tools to call, and when the task is complete.
2. **Tools** — the hands. Functions the LLM can invoke to interact with the world (read files, call APIs, run tests, etc.).
3. **The agentic loop** — lets the LLM keep calling tools until the task is complete, passing full conversation history on each iteration.
4. **The conversational loop** — the outer wrapper that allows the user to keep giving the agent new tasks.

---

## What is MCP?

**Model Context Protocol (MCP)** is a standard that allows agents to connect to external tool servers rather than having all tools hardcoded in the agent itself.

- **MCP Server** — a separate process that exposes tools over a standard protocol (e.g. a Playwright MCP server exposes tools like `navigate`, `click`, `run_test`)
- **MCP Client** — lives inside the agent and connects to one or more MCP servers to discover and call their tools

### Without MCP
Tools are Python functions defined directly in the agent code. Only your agent can use them.

### With MCP
Tools live on a server. Your agent connects to any MCP server and instantly gets its tools — without writing the tool code yourself.

---

## Pipeline Architecture

```
Jira MCP
    |
    | (user stories)
    v
Orchestrator Agent
    |
    |------------------------------|------------------------------|
    v                             v                              v
Test Generator Agent       Script Writer Agent           Test Runner Agent
    |                             |                              |
    | (test cases)                | (scripts)                    | (execute)
    v                             |------------------------->    v
TestRail MCP                                             BrowserStack MCP
    ^                                                            |
    |________________________(results)__________________________|
```

---

## Components

### Orchestrator Agent
The thin brain of the system. Receives the high-level task and delegates to specialized sub-agents. It does not do the work itself — it coordinates.

**Responsibilities:**
- Connect to Jira MCP to retrieve user stories
- Determine which sub-agents to invoke and in what order
- Manage the overall conversation history and context

---

### Test Generator Agent
Reads user stories from Jira and produces structured, human-readable test cases.

**Responsibilities:**
- Parse user story acceptance criteria
- Generate test case titles, steps, and expected results
- Insert test cases into TestRail via MCP

**Tools used:**
- Jira MCP — read user stories
- TestRail MCP — create test cases and test runs

---

### Script Writer Agent
Takes structured test cases and produces executable pytest/Playwright scripts.

**Responsibilities:**
- Generate Playwright test scripts from TestRail test cases
- Follow project conventions (page objects, fixtures, assertions)
- Write scripts to the local filesystem

**Tools used:**
- TestRail MCP — read test cases
- File tools (`read`, `write`, `edit`) — manage script files

---

### Test Runner Agent
Executes the generated scripts and captures results.

**Responsibilities:**
- Execute pytest/Playwright scripts locally or via BrowserStack
- Capture pass/fail status, error messages, and screenshots
- Report results back to TestRail

**Tools used:**
- BrowserStack MCP — cross-browser execution
- Bash tool — local execution
- TestRail MCP — update test run results

---

## MCP Servers

| Server | Purpose |
|---|---|
| **Jira MCP** | Read user stories and acceptance criteria |
| **TestRail MCP** | Create/read test cases, create test runs, update results |
| **BrowserStack MCP** | Execute Playwright tests across browsers and devices |

---

## Project File Structure

```
qa-agent/
├── agent.py              # Orchestrator — thin agentic + conversational loop
├── tools.py              # All tool definitions and executors
├── connections.py        # API clients, MCP connections, credentials
└── agents/
    ├── test_generator.py # Generates test cases from user stories
    ├── script_writer.py  # Generates pytest/Playwright scripts
    └── test_runner.py    # Executes tests and reports results
```

---

## Data Flow

1. **Jira → Test Generator** — user stories pulled via Jira MCP
2. **Test Generator → TestRail** — structured test cases inserted via TestRail MCP
3. **TestRail → Script Writer** — test cases read and converted to Playwright scripts
4. **Script Writer → Test Runner** — scripts handed off for execution
5. **Test Runner → BrowserStack** — scripts executed cross-browser
6. **BrowserStack → TestRail** — results written back via TestRail MCP

---

## Key Design Principles

- **Keep the orchestrator thin** — it coordinates, it does not implement
- **Specialized agents have focused tools** — each agent only has access to the tools it needs
- **MCP over hardcoded tools** — prefer MCP servers for external integrations so tools can be reused across agents
- **Context management matters** — message history grows with each loop iteration; plan for summarization or pruning in production
- **Safety first** — bash and file write tools should be sandboxed; confirm before destructive actions

---

## Portfolio Value

This project demonstrates end-to-end competency in:

- **AI agent design** — orchestrator + specialist pattern
- **MCP integration** — connecting agents to real external systems
- **Test automation** — Playwright, pytest, cross-browser execution
- **Test management** — TestRail integration for full traceability
- **Python architecture** — clean separation of agent, tools, and connections

---

*Architecture designed as part of an SDET Manager portfolio project.*
