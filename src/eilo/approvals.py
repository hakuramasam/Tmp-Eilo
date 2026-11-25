"""Fail-closed approval policy for tool execution."""

from collections.abc import Awaitable, Callable
from enum import IntEnum


class RiskLevel(IntEnum):
    LOW = 0
    MODERATE = 1
    HIGH = 2


ApprovalCallback = Callable[[str, str, dict], bool | Awaitable[bool]]


class ApprovalManager:
    def __init__(self, approval_callback: ApprovalCallback | None = None, auto_approve_up_to: RiskLevel = RiskLevel.LOW) -> None:
        self.approval_callback = approval_callback
        self.auto_approve_up_to = auto_approve_up_to

    async def is_approved(self, tool_name: str, risk: RiskLevel, arguments: dict) -> bool:
        if risk <= self.auto_approve_up_to:
            return True
        if self.approval_callback is None:
            return False
        result = self.approval_callback(tool_name, risk.name.lower(), arguments)
        if hasattr(result, "__await__"):
            result = await result
        return result is True
