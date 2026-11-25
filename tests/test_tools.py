import pytest

from eilo.approvals import RiskLevel
from eilo.tools.basic import register_basic_tools, safe_calculate
from eilo.tools.registry import Tool, ToolRegistry


def test_calculator_arithmetic():
    assert safe_calculate("(2 + 3) * 4") == 20


def test_calculator_rejects_code():
    with pytest.raises(ValueError):
        safe_calculate("__import__('os').system('echo unsafe')")


@pytest.mark.asyncio
async def test_builtin_tools_registered_and_run():
    registry = ToolRegistry()
    register_basic_tools(registry)
    assert await registry.execute("calculator", '{"expression":"6 / 2"}') == {"result": 3}


@pytest.mark.asyncio
async def test_high_risk_tool_requires_approval():
    registry = ToolRegistry()
    registry.register(Tool("deploy", "deploy", {"type": "object"}, RiskLevel.HIGH, lambda _: True))
    with pytest.raises(PermissionError):
        await registry.execute("deploy", {})
