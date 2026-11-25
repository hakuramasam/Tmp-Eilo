"""OpenAI-compatible asynchronous chat-completions client."""

from typing import Any

import httpx

from .config import settings


class LLMError(RuntimeError):
    """Raised when the language-model provider request fails."""


class OpenAICompatibleClient:
    def __init__(self) -> None:
        if not settings.model:
            raise ValueError("EILO_MODEL must be configured.")
        self.base_url = settings.api_base_url.rstrip("/")
        self.api_key = settings.api_key
        self.model = settings.model
        self.timeout = settings.timeout_seconds

    async def chat(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload: dict[str, Any] = {"model": self.model, "messages": messages}
        if tools:
            payload.update({"tools": tools, "tool_choice": "auto"})
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise LLMError(f"Chat completion request failed: {type(exc).__name__}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("choices"), list) or not data["choices"]:
            raise LLMError("Provider returned an invalid chat-completions response.")
        return data
