import pytest

from eilo.approvals import ApprovalManager, RiskLevel


@pytest.mark.asyncio
async def test_high_risk_denied_without_callback():
    assert not await ApprovalManager().is_approved("deploy", RiskLevel.HIGH, {})


@pytest.mark.asyncio
async def test_explicit_callback_can_approve():
    manager = ApprovalManager(approval_callback=lambda *_: True)
    assert await manager.is_approved("deploy", RiskLevel.HIGH, {})


@pytest.mark.asyncio
async def test_low_risk_allowed_by_default():
    assert await ApprovalManager().is_approved("calculator", RiskLevel.LOW, {})
