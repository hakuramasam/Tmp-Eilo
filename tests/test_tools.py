import pytest

from eilo.approvals import ApprovalManager, RiskLevel
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
    registry.register(
        Tool("deploy", "deploy", {"type": "object"}, RiskLevel.HIGH, lambda _: True)
    )
    with pytest.raises(PermissionError):
        await registry.execute("deploy", {})


@pytest.mark.asyncio
async def test_approved_synchronous_handler_executes():
    approvals = ApprovalManager(approval_callback=lambda *_: True)
    registry = ToolRegistry(approvals=approvals)
    registry.register(
        Tool(
            "sync_value",
            "Return a synchronous value",
            {"type": "object", "properties": {}, "additionalProperties": False},
            RiskLevel.HIGH,
            lambda _: {"ok": True},
        )
    )
    assert await registry.execute("sync_value", {}) == {"ok": True}


@pytest.mark.asyncio
async def test_tool_arguments_are_validated_before_handler():
    called = False

    def handler(_: dict) -> dict:
        nonlocal called
        called = True
        return {"ok": True}

    registry = ToolRegistry()
    registry.register(
        Tool(
            "requires_name",
            "Requires a name",
            {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": False,
            },
            RiskLevel.LOW,
            handler,
        )
    )
    with pytest.raises(ValueError, match="name"):
        await registry.execute("requires_name", {})
    with pytest.raises(ValueError, match="Additional properties"):
        await registry.execute("requires_name", {"name": "Eilo", "unexpected": True})
    assert not called
