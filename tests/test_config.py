import pytest
from pydantic import ValidationError

from eilo.config import Settings


def test_timeout_must_be_positive():
    with pytest.raises(ValidationError):
        Settings(timeout_seconds=0)


def test_tool_rounds_must_be_within_safe_bounds():
    with pytest.raises(ValidationError):
        Settings(max_tool_rounds=0)
    with pytest.raises(ValidationError):
        Settings(max_tool_rounds=101)
