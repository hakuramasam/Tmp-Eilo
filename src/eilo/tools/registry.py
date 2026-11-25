"""Tool registration and risk-aware execution."""

import json
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from ..approvals import ApprovalManager, RiskLevel

ToolHandler = Callable[[dict[str, Any]], Any | Awaitable[Any]]


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    risk: RiskLevel
    handler: ToolHandler

    def to_api_schema(self) -> dict[str, Any]:
        return {"type": "function", "function": {"name": self.name, "description": self.description, "parameters": self.parameters}}


class ToolRegistry:
    def __init__(self, approvals: ApprovalManager | None = None) -> None:
        self._tools: dict[str, Tool] = {}
        self.approvals = approvals or ApprovalManager()

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def schemas(self) -> list[dict[str, Any]]:
        return [tool.to_api_schema() for tool in self._tools.values()]

    async def execute(self, name: str, arguments: str | dict[str, Any]) -> Any:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Unknown tool: {name}")
        try:
            parsed = json.loads(arguments) if isinstance(arguments, str) else arguments
        except json.JSONDecodeError as exc:
            raise ValueError("Tool arguments must be valid JSON.") from exc
        if not isinstance(parsed, dict):
            raise ValueError("Tool arguments must be a JSON object.")
        if not await self.approvals.is_approved(name, tool.risk, parsed):
            raise PermissionError(f"Approval required for tool: {name}")
        return await tool.handler(parsed)
