"""System prompt loading."""

from pathlib import Path

from .config import settings

DEFAULT_PROMPT = """You are Eilo, a helpful and safety-conscious AI agent. Be accurate, protect secrets, validate tool use, and request approval for consequential actions. Never claim an action succeeded without evidence."""


def load_system_prompt() -> str:
    candidates: list[Path] = []
    if settings.system_prompt_path:
        candidates.append(Path(settings.system_prompt_path))
    candidates.extend([
        Path.cwd() / "instructions" / "SYSTEM.md",
        Path(__file__).resolve().parents[2] / "instructions" / "SYSTEM.md",
        Path(__file__).resolve().parents[3] / "instructions" / "SYSTEM.md",
    ])
    for path in candidates:
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return DEFAULT_PROMPT
