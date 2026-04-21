"""
===============================================================================
File: base.py

Location:
    ai/providers/

Purpose:
    Abstract base interface for all AI provider implementations.

Design Pattern:
    Each AI provider must implement two methods:
    
    1. generate() - Returns raw text response from the model
    2. normalize_response() - Converts raw response to standard format
    
    This dual-method pattern ensures:
    - Providers handle their own response parsing
    - Agents never touch provider-specific formats
    - New providers can be added without modifying agents

Architecture Layer:
    
    Provider Response → normalize_response() → StandardToolCall[]
                                                    ↓
                                             CodingAgent
                                                    ↓
                                            ToolOperation[]
                                                    ↓
                                          Orchestration (generate_tests.py)

Adding a New Provider:
    1. Create new class inheriting from AIProvider
    2. Implement generate() to call the provider's API
    3. Implement normalize_response() to parse their response format
    4. Register in client_factory.py
    5. No changes needed to agents or orchestration

===============================================================================
"""

from abc import ABC, abstractmethod
from typing import List, Any
from ai.schemas.tool_call import StandardToolCall


class AIProvider(ABC):
    """
    Abstract base class for AI provider implementations.

    All providers (Ollama, OpenAI, Anthropic, etc.) must inherit from this
    class and implement both abstract methods.
    
    Design Goals:
        - Consistent interface regardless of backend
        - Response parsing encapsulated in providers
        - Agents remain provider-agnostic
        - Easy to add new providers without cascading changes
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a response from the AI model.
        
        Args:
            prompt: The user prompt/query
            system: Optional system prompt for context
            temperature: Control randomness (0.0 = deterministic)
            max_tokens: Maximum response length
            
        Returns:
            Raw text response from the model (not parsed)
            
        Raises:
            RuntimeError: If the request fails
            
        Note:
            This returns the raw, unparsed response. Tool call extraction
            is handled by normalize_response().
        """
        pass

    @abstractmethod
    def normalize_response(
        self,
        response: Any,
    ) -> List[StandardToolCall]:
        """
        Convert provider-specific response format to standard tool calls.
        
        This method handles all provider-specific parsing logic, ensuring
        the CodingAgent never needs to know about different response formats.
        
        Args:
            response: Raw response from generate()
            
        Returns:
            List of StandardToolCall objects (may be empty if no tools found)
            
        Implementation Notes:
            - Must handle JSON parsing errors gracefully
            - Should log warnings if response structure is unexpected
            - Return empty list if no tool calls are present
            - Each StandardToolCall must have valid name and arguments
            
        Example for Ollama format:
            Input: {"tools": [{"name": "write", "arguments": {...}}]}
            Output: [StandardToolCall(name="write", arguments={...})]
            
        Example for OpenAI format:
            Input: {"choices": [{"message": {"tool_calls": [...]}}]}
            Output: [StandardToolCall(name="...", arguments={...})]
        """
        pass