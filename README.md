# Eilo Agent

Eilo is a modular, safety-conscious AI agent foundation built with Python 3.11+, an OpenAI-compatible chat-completions API, a risk-aware tool registry, and local SQLite memory.

## Features
- Async OpenAI-compatible LLM adapter using HTTPX.
- Pydantic Settings configuration via environment variables and optional `.env`.
- Bounded tool-call loop with JSON Schema-validated tool arguments and sync/async handlers.
- Fail-closed approval manager for moderate/high-risk actions.
- Safe arithmetic calculator and UTC clock tools.
- SQLite note storage with simple keyword search and deletion.
- Typer CLI with Rich output.
- Tests for approvals, tools, and memory.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
```

Set `EILO_API_BASE_URL`, `EILO_API_KEY`, and `EILO_MODEL` in your local `.env`. Do not commit real credentials.

```bash
eilo chat "What is 19 * 23?"
eilo remember "My project uses Python"
eilo recall "Python"
pytest
```

For local OpenAI-compatible servers, set the base URL to the server's `/v1` API root and configure the model name it serves.

## Project layout
- `instructions/`: system and operational guidance.
- `workflows/`: repeatable task procedures.
- `tools/`: integration contracts and security notes.
- `evaluations/`: evaluation plans.
- `src/eilo/`: runnable Python package.
- `tests/`: automated tests.

## Safety and limitations
The starter does not include arbitrary shell execution, browser/computer use, MCP transport, hosted scheduling, multi-agent orchestration, deployment automation, wallet access, or financial transaction capabilities. Those are documented extension points, not implemented features. The approval manager has no built-in interactive UI; high-risk tools are denied unless an application supplies an explicit approval callback. Review and threat-model any extension before production use.

Memory is local keyword-based SQLite storage, not vector or semantic retrieval. Do not store secrets or sensitive personal information.

## Development
```bash
pip install -e '.[dev]'
ruff check .
pytest
```

See [AGENTS.md](AGENTS.md) for contribution and operating rules.
