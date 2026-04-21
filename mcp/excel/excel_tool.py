from typing import Dict, Any, List
import logging

from mcp.base.tool import MCPTool
from repositories.excel_repository import ExcelRepository


logger = logging.getLogger(__name__)


class ExcelTool(MCPTool):

    name = "excel"
    version = "1.0.0"

    capabilities = [
        "persistence",
        "excel",
        "testcases",
    ]

    # ------------------------------------------------------------------

    def __init__(self) -> None:

        self.repository = ExcelRepository()

    # ------------------------------------------------------------------
    # MCP Schema
    # ------------------------------------------------------------------

    def schema(self) -> Dict[str, Any]:

        return {
            "name": self.name,
            "version": self.version,
            "description": "Excel persistence operations",
            "operations": {
                "create": {
                    "description": "Save test cases",
                    "required": ["data"],
                },
                "read": {
                    "description": "Load test cases",
                    "optional": ["id"],
                },
                "list": {
                    "description": "List worksheets",
                },
                "exists": {
                    "description": "Check workbook existence",
                    "optional": ["id"],
                },
                "health": {
                    "description": "Check tool health",
                },
            },
        }

    # ------------------------------------------------------------------
    # Validation Helper
    # ------------------------------------------------------------------

    def _require(
        self,
        arguments: Dict[str, Any],
        field: str,
    ) -> None:

        if field not in arguments:

            raise ValueError(
                f"Missing required field: {field}"
            )

    # ------------------------------------------------------------------
    # Health Check
    # ------------------------------------------------------------------

    def ping(self) -> bool:

        try:

            return self.repository.exists("Sheet1")

        except Exception:

            logger.exception(
                "Excel health check failed"
            )

            return False

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(
        self,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:

        operation = arguments.get("operation")

        if not operation:

            raise ValueError(
                "Operation is required"
            )

        logger.info(
            "ExcelTool operation executed",
            extra={
                "operation": operation,
            },
        )

        # --------------------------------------------------------------

        if operation == "create":

            self._require(arguments, "data")

            data: List[Dict[str, Any]] = arguments["data"]

            self.repository.save(data)

            return {
                "status": "success",
                "operation": operation,
                "count": len(data),
            }

        # --------------------------------------------------------------

        if operation == "read":

            identifier = arguments.get(
                "id",
                "Sheet1",
            )

            result = self.repository.load(
                identifier
            )

            return {
                "status": "success",
                "operation": operation,
                "count": len(result),
                "result": result,
            }

        # --------------------------------------------------------------

        if operation == "list":

            sheets = self.repository.list()

            return {
                "status": "success",
                "operation": operation,
                "count": len(sheets),
                "sheets": sheets,
            }

        # --------------------------------------------------------------

        if operation == "exists":

            identifier = arguments.get(
                "id",
                "Sheet1",
            )

            exists = self.repository.exists(
                identifier
            )

            return {
                "status": "success",
                "operation": operation,
                "exists": exists,
            }

        # --------------------------------------------------------------

        if operation == "health":

            healthy = self.ping()

            return {
                "status": "healthy"
                if healthy
                else "unavailable"
            }

        # --------------------------------------------------------------

        raise ValueError(
            f"Unsupported operation: {operation}"
        )