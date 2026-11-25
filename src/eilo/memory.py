"""Small local SQLite memory store with keyword retrieval."""

import sqlite3
import uuid
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Iterator


class MemoryStore:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._uri = database_path == ":memory:"
        self._dsn = (
            f"file:eilo-memory-{uuid.uuid4().hex}?mode=memory&cache=shared"
            if self._uri
            else database_path
        )
        self._keeper = sqlite3.connect(self._dsn, uri=True) if self._uri else None

        if not self._uri:
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)

        with self._session() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._dsn, uri=self._uri)

    @contextmanager
    def _session(self) -> Iterator[sqlite3.Connection]:
        with closing(self._connect()) as connection:
            with connection:
                yield connection

    def close(self) -> None:
        """Release the anchor connection used to keep an in-memory database alive."""
        if self._keeper is not None:
            self._keeper.close()
            self._keeper = None

    def add(self, content: str) -> int:
        if not content.strip():
            raise ValueError("Memory content cannot be empty.")
        with self._session() as connection:
            cursor = connection.execute(
                "INSERT INTO memories(content) VALUES (?)", (content,)
            )
            return int(cursor.lastrowid)

    def search(self, query: str, limit: int = 10) -> list[dict[str, str | int]]:
        words = [word for word in query.split() if word]
        if not words:
            return []
        clauses = " OR ".join("content LIKE ?" for _ in words)
        params = [f"%{word}%" for word in words]
        bounded_limit = max(1, min(limit, 100))
        with self._session() as connection:
            rows = connection.execute(
                f"""
                SELECT id, content, created_at
                FROM memories
                WHERE {clauses}
                ORDER BY id DESC
                LIMIT ?
                """,
                (*params, bounded_limit),
            ).fetchall()
        return [
            {"id": row[0], "content": row[1], "created_at": row[2]}
            for row in rows
        ]

    def delete(self, memory_id: int) -> bool:
        with self._session() as connection:
            cursor = connection.execute(
                "DELETE FROM memories WHERE id = ?", (memory_id,)
            )
            return cursor.rowcount > 0
