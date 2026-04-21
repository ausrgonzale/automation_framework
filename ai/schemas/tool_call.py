"""
===============================================================================
File: tool_call.py

Location:
    ai/schemas/

Purpose:
    Standard data models for tool calls across all AI providers.
    
    Eliminates the need for agents or orchestration code to understand
    provider-specific response formats.

Design Rationale:
    Different AI providers return tool calls in different formats:
    
    - Ollama: {"tools": [{"name": "...", "arguments": {...}}]}
    - OpenAI: {"choices": [{"message": {"tool_calls": [{"function": {...}}]}}]}
    - Anthropic: Similar structure but with different nesting
    
    Instead of having agents parse each format, we standardize to a single
    representation that all providers normalize to. This:
    
    1. Decouples agents from provider details
    2. Makes testing easier (mock StandardToolCall objects)
    3. Simplifies adding new providers
    4. Creates a clear contract between providers and consumers

Usage:
    # Provider receives raw response and normalizes it
    standard_calls = provider.normalize_response(raw_response)
    
    # Agent receives already-normalized StandardToolCall objects
    for call in standard_calls:
        operation = ToolOperation(name=call.name, arguments=call.arguments)

Extension:
    To add a new provider:
    1. Implement AIProvider interface with generate() and normalize_response()
    2. normalize_response() returns List[StandardToolCall]
    3. No changes needed to agents or orchestration code

===============================================================================
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class StandardToolCall:
    """
    Normalized tool call representation.
    
    This is the standard format returned by all AI providers' normalize_response()
    method. Agents and orchestration code consume this format, never raw
    provider responses.
    
    Attributes:
        name: The tool/function name (e.g., "write", "bash")
        arguments: Dictionary of arguments passed to the tool
        
    Guarantees:
        - name is always a non-empty string
        - arguments is always a dict (may be empty)
        - No provider-specific fields or nesting
    
    Example:
        StandardToolCall(
            name="write",
            arguments={
                "path": "tests/unit/test_example.py",
                "content": "..."
            }
        )
    """

    name: str
    arguments: Dict[str, Any]
