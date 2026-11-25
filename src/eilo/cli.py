"""Command-line interface."""

import asyncio
import typer
from rich.console import Console

from .agent import EiloAgent
from .config import settings
from .memory import MemoryStore
from .tools.basic import register_basic_tools
from .tools.registry import ToolRegistry

app = typer.Typer(help="Eilo AI agent")
console = Console()


def build_agent() -> EiloAgent:
    registry = ToolRegistry()
    register_basic_tools(registry)
    return EiloAgent(tools=registry)


@app.command()
def chat(message: str = typer.Argument(..., help="Message to send to Eilo")) -> None:
    try:
        console.print(asyncio.run(build_agent().run(message)))
    except Exception as exc:
        console.print(f"[red]Eilo error:[/red] {type(exc).__name__}: {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def remember(content: str = typer.Argument(..., help="A non-sensitive note to store")) -> None:
    memory = MemoryStore(settings.database_path)
    console.print(f"Stored memory #{memory.add(content)}")


@app.command()
def recall(query: str = typer.Argument(..., help="Keywords to search")) -> None:
    for item in MemoryStore(settings.database_path).search(query):
        console.print(f"#{item['id']} — {item['content']}")


if __name__ == "__main__":
    app()
