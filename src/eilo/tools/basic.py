"""Safe built-in utility tools."""

import ast
import operator
from datetime import UTC, datetime
from typing import Any

from ..approvals import RiskLevel
from .registry import Tool, ToolRegistry

_OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos}


def safe_calculate(expression: str) -> int | float:
    if len(expression) > 200:
        raise ValueError("Expression is too long.")
    tree = ast.parse(expression, mode="eval")

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            left, right = evaluate(node.left), evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent is too large.")
            value = _OPERATORS[type(node.op)](left, right)
            if abs(value) > 10**100:
                raise ValueError("Result is too large.")
            return value
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Unsupported expression.")

    return evaluate(tree)


def register_basic_tools(registry: ToolRegistry) -> None:
    async def calculate(args: dict[str, Any]) -> dict[str, Any]:
        expression = args.get("expression")
        if not isinstance(expression, str):
            raise ValueError("expression must be a string")
        return {"result": safe_calculate(expression)}

    async def utc_time(_: dict[str, Any]) -> dict[str, str]:
        return {"utc": datetime.now(UTC).isoformat()}

    registry.register(Tool("calculator", "Evaluate basic arithmetic without Python execution.", {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"], "additionalProperties": False}, RiskLevel.LOW, calculate))
    registry.register(Tool("utc_time", "Return the current UTC date and time.", {"type": "object", "properties": {}, "additionalProperties": False}, RiskLevel.LOW, utc_time))
