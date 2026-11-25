"""Bounded tool-using agent loop."""

import json
from typing import Any

from .config import settings
from .llm import OpenAICompatibleClient
from .prompts import load_system_prompt
from .tools.registry import ToolRegistry


class EiloAgent:
    def __init__(self, llm: OpenAICompatibleClient | None = None, tools: ToolRegistry | None = None) -> None:
        self.llm = llm or OpenAICompatibleClient()
        self.tools = tools or ToolRegistry()

    async def run(self, user_message: str) -> str:
        messages: list[dict[str, Any]] = [{"role": "system", "content": load_system_prompt()}, {"role": "user", "content": user_message}]
        for _ in range(settings.max_tool_rounds):
            response = await self.llm.chat(messages, self.tools.schemas())
            assistant = response["choices"][0].get("message", {})
            if not isinstance(assistant, dict):
                raise RuntimeError("Provider returned an invalid assistant message.")
            messages.append(assistant)
            calls = assistant.get("tool_calls") or []
            if not calls:
                content = assistant.get("content")
                return content if isinstance(content, str) else ""
            for call in calls:
                function = call.get("function", {})
                name, arguments = function.get("name"), function.get("arguments", "{}")
                try:
                    result = await self.tools.execute(name, arguments)
                    output = json.dumps(result, default=str)
                except Exception as exc:
                    output = json.dumps({"error": type(exc).__name__, "message": str(exc)})
                messages.append({"role": "tool", "tool_call_id": call.get("id", ""), "content": output})
        raise RuntimeError("Maximum tool-call rounds reached.")
