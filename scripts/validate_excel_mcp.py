"""
Runtime validation for Excel MCP tool.

This is NOT a unit test.
It is a deterministic smoke test to verify MCP behavior.
"""

from mcp.excel.excel_tool import ExcelTool


def main():

    print("\nInitializing ExcelTool...")

    tool = ExcelTool()

    # --------------------------------------------------
    # Health
    # --------------------------------------------------

    print("\nRunning health check...")

    health = tool.execute({
        "operation": "health"
    })

    print("Health:", health)

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    print("\nCreating test case...")

    create_result = tool.execute({
        "operation": "create",
        "data": [
            {
                "id": 1,
                "title": "Smoke Test",
                "steps": "Run validation script",
                "expected_result": "Excel row created",
                "priority": "High",
            }
        ]
    })

    print("Create:", create_result)

    # --------------------------------------------------
    # Read
    # --------------------------------------------------

    print("\nReading test cases...")

    read_result = tool.execute({
        "operation": "read"
    })

    print("Read:", read_result)

    # --------------------------------------------------
    # List
    # --------------------------------------------------

    print("\nListing sheets...")

    list_result = tool.execute({
        "operation": "list"
    })

    print("List:", list_result)

    print("\nExcel MCP validation complete.")


if __name__ == "__main__":
    main()