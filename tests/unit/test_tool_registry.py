import pytest

from typing import Dict, Any
from mcp.base.registry import MCPRegistry
from mcp.base.tool import MCPTool


# ---------------------------------------------------------------------
# Test Tool Fixture
# ---------------------------------------------------------------------

class DummyTool(MCPTool):

    name = "dummy_tool"

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "status": "success"
        }
# ---------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------

def test_register_tool_success():

    registry = MCPRegistry()

    tool = DummyTool()

    registry.register(tool)

    assert registry.is_registered("dummy_tool")

    assert len(registry) == 1


# ---------------------------------------------------------------------

def test_prevent_duplicate_registration():

    registry = MCPRegistry()

    tool = DummyTool()

    registry.register(tool)

    with pytest.raises(ValueError):

        registry.register(tool)


# ---------------------------------------------------------------------

def test_get_tool_success():

    registry = MCPRegistry()

    tool = DummyTool()

    registry.register(tool)

    retrieved = registry.get_tool("dummy_tool")

    assert retrieved is tool


def test_get_tool_not_found():

    registry = MCPRegistry()

    with pytest.raises(ValueError):

        registry.get_tool("unknown_tool")


# ---------------------------------------------------------------------

def test_list_tools_returns_sorted_names():

    registry = MCPRegistry()

    tool = DummyTool()

    registry.register(tool)

    tools = registry.list_tools()

    assert tools == ["dummy_tool"]


# ---------------------------------------------------------------------

def test_contains_operator():

    registry = MCPRegistry()

    tool = DummyTool()

    registry.register(tool)

    assert "dummy_tool" in registry


# ---------------------------------------------------------------------

def test_registry_length():

    registry = MCPRegistry()

    tool = DummyTool()

    registry.register(tool)

    assert len(registry) == 1


# ---------------------------------------------------------------------

def test_clear_registry():

    registry = MCPRegistry()

    tool = DummyTool()

    registry.register(tool)

    registry.clear()

    assert len(registry) == 0

    assert registry.list_tools() == []