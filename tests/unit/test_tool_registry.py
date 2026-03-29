from tools.tool_registry import ToolRegistry


def test_register_and_execute_tool():

    registry = ToolRegistry()

    def dummy_handler(args):
        return "ok"

    registry.register(
        name="dummy",
        handler=dummy_handler,
        schema={"type": "object"},
    )

    result = registry.execute(
        name="dummy",
        arguments={},
    )

    assert result == "ok"