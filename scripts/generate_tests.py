from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import List, Optional

from ai.agents.coding_agent import CodingAgent, ToolOperation
from ai.client_factory import get_ai_client

# Module-level defaults
DEFAULT_TEMPERATURE = 0
DEFAULT_STREAM = False


def process_job_payload(payload: dict) -> None:
    """
    Process a job payload from the orchestration agent, using normalized prompt and generation params.
    """
    logger.info("Processing job payload with normalized prompt")
    prompt = payload.get("normalized_prompt")
    generation_params = payload.get("generation_params", {})

    if not prompt:
        logger.error("No normalized_prompt found in payload")
        return

    client = get_ai_client()

    # Pass all generation_params to CodingAgent
    agent = CodingAgent(
        client,
        temperature=generation_params.get("temperature", DEFAULT_TEMPERATURE),
        stream=generation_params.get("stream", DEFAULT_STREAM),
        max_tokens=generation_params.get("num_predict", 2000),
        stop=generation_params.get("stop"),
    )

    operations = agent.process(prompt, generation_params=generation_params)

    if not operations:
        logger.error("No operations returned from agent")
        return

    logger.info("Operations collected: %s", len(operations))
    execute_operations_once(operations)
    logger.info("Job payload processing completed")


"""
===============================================================================
File: generate_tests.py

Location:
    scripts/

Purpose:
    Deterministic entry point for generating pytest unit tests using the
    CodingAgent.

Design Principles:

    - Call the agent once
    - Cache returned operations
    - Execute each operation type once
    - Produce predictable logs
    - Prevent duplicate writes or pytest runs

This file acts as the orchestration layer for test generation.

===============================================================================
"""

"""
===============================================================================
File: generate_tests.py

Location:
    scripts/

Purpose:
    Deterministic entry point for generating pytest unit tests using the
    CodingAgent.

Design Principles:

    - Call the agent once
    - Cache returned operations
    - Execute each operation type once
    - Produce predictable logs
    - Prevent duplicate writes or pytest runs

This file acts as the orchestration layer for test generation.

===============================================================================
"""


# =============================================================================
# Logging Configuration
# =============================================================================


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


# =============================================================================
# Execution State Guards
# =============================================================================


file_written: bool = False
pytest_executed: bool = False


# =============================================================================
# Tool Execution Functions
# =============================================================================


def execute_write(arguments: dict) -> None:
    """
    Write generated test file to disk.
    """

    global file_written

    if file_written:
        logger.info("Write already executed — skipping")
        return

    path_value = arguments.get("path")

    if not isinstance(path_value, str):
        logger.error("Invalid path argument")
        return

    path = Path(path_value)

    content = arguments.get("content", "")

    if not isinstance(content, str):
        logger.error("Invalid content argument")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content)

    file_written = True

    print()
    print("The following test cases were created:")
    print()
    print(f"Location: {path}")


# -----------------------------------------------------------------------------


def execute_bash(arguments: dict) -> None:
    """
    Execute pytest or other shell command.
    """
    # Define defaults if not already defined

    # Pass all generation_params to CodingAgent
    global pytest_executed

    if pytest_executed:
        logger.info("Pytest already executed — skipping")
        return

    command_value = arguments.get("command", "pytest")

    if not isinstance(command_value, str):
        logger.error("Invalid command argument")
        return

    print()
    print("------------------------------------------------------------")
    print()
    print("pytest execution results:")
    print()

    try:
        subprocess.run(
            command_value,
            shell=True,
            check=False,
        )

        pytest_executed = True

    except Exception as exc:
        logger.exception("Failed to execute command")
        raise RuntimeError("Command execution failed") from exc


# =============================================================================
# Operation Execution
# =============================================================================


def find_operation(
    operations: List[ToolOperation],
    name: str,
) -> Optional[ToolOperation]:
    """
    Return the first operation matching the given name.
    """

    return next(
        (op for op in operations if op.name == name),
        None,
    )


# -----------------------------------------------------------------------------


def execute_operations_once(
    operations: List[ToolOperation],
) -> None:
    """
    Deterministically execute operations.

    Only one write and one bash operation will be executed.
    """

    write_operation = find_operation(operations, "write")
    bash_operation = find_operation(operations, "bash")

    if write_operation:
        logger.info("Executing write operation")
        execute_write(write_operation.arguments)

    if bash_operation:
        logger.info("Executing bash operation")
        execute_bash(bash_operation.arguments)


# =============================================================================
# Main Entry Point
# =============================================================================


def main() -> None:
    """
    Main execution flow.
    """

    logger.info("Starting test generation")

    file_path = Path("services/testcase_generation_service.py")

    if not file_path.exists():
        logger.error("Hardcoded file not found: %s", file_path)
        return

    file_content = file_path.read_text()

    query = f"""
You are a code generation engine. Your job is to:
1. Read the provided Python file.
2. Identify all top-level functions and methods that need unit tests.
3. Output a single valid JSON object ONLY, in the format below, with NO explanations, NO reasoning, NO extra text. Output must start with '{{' and end with '}}'.

Input file:
{file_path}

Content:
{file_content}

Output format:
{{
    "tools": [
        {{"name": "write", "arguments": {{"path": "tests/unit/test_example.py", "content": "...pytest code..."}}}},
        {{"name": "bash", "arguments": {{"command": "pytest tests/unit/test_example.py -v"}}}}
    ]
}}

Do not explain. Do not narrate. Do not output anything except the JSON object.
"""

    client = get_ai_client()

    agent = CodingAgent(client)

    operations = agent.process(query)

    if not operations:
        logger.error("No operations returned from agent")
        return

    logger.info("Operations collected: %s", len(operations))

    execute_operations_once(operations)

    logger.info("Generation completed")


# =============================================================================
# Script Execution Guard
# =============================================================================


if __name__ == "__main__":
    main()
