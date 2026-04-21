from unittest.mock import patch

from ai.agents.search_agent import SearchAgent
from mcp.base.registry import MCPRegistry


class DummyRegistry(MCPRegistry):
    def __init__(self):
        pass

    def list_tools(self):
        return ["read_file", "write_file"]

    def get_tool_schemas(self):
        return [
            {"name": "read_file", "input_schema": {"properties": {"path": {}}}},
            {
                "name": "write_file",
                "input_schema": {"properties": {"path": {}, "content": {}}},
            },
        ]

    def execute(self, tool_name, arguments):
        return f"Executed {tool_name} with {arguments}"


def test_show_startup_help(capsys):
    agent = SearchAgent(DummyRegistry())
    agent.show_startup_help()
    out = capsys.readouterr().out
    assert "Search Agent started" in out
    assert "read_file <path>" in out
    assert "write_file <path>" in out


def test_show_help(capsys):
    agent = SearchAgent(DummyRegistry())
    agent.show_help()
    out = capsys.readouterr().out
    assert "read_file path" in out
    assert "write_file path content" in out


def test_run_help_and_exit(monkeypatch, capsys):
    agent = SearchAgent(DummyRegistry())
    inputs = iter(["help", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    with patch.object(agent, "show_help", wraps=agent.show_help) as mock_help:
        agent.run()
        assert mock_help.called
    out = capsys.readouterr().out
    assert "Available commands" in out


def test_run_valid_command(monkeypatch, capsys):
    agent = SearchAgent(DummyRegistry())
    inputs = iter(["read_file foo.txt", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    agent.run()
    out = capsys.readouterr().out
    assert "Executed read_file with" in out


def test_run_invalid_command(monkeypatch, capsys):
    agent = SearchAgent(DummyRegistry())
    inputs = iter(["write_file onlyonearg", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    agent.run()
    out = capsys.readouterr().out
    assert "Usage: write_file <path> <content>" in out
