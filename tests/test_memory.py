import pytest

from eilo.memory import MemoryStore


def test_memory_add_search_delete(tmp_path):
    memory = MemoryStore(str(tmp_path / "memory.sqlite3"))
    memory_id = memory.add("Eilo uses SQLite for local notes")
    results = memory.search("SQLite")
    assert len(results) == 1
    assert results[0]["id"] == memory_id
    assert memory.delete(memory_id)
    assert memory.search("SQLite") == []


def test_memory_rejects_blank_content(tmp_path):
    memory = MemoryStore(str(tmp_path / "memory.sqlite3"))
    with pytest.raises(ValueError, match="cannot be empty"):
        memory.add("   ")


def test_in_memory_database_survives_between_operations():
    memory = MemoryStore(":memory:")
    memory_id = memory.add("ephemeral test note")
    assert memory.search("ephemeral")[0]["id"] == memory_id
    assert memory.delete(memory_id)
    assert memory.search("ephemeral") == []
    memory.close()


def test_separate_in_memory_stores_are_isolated():
    first = MemoryStore(":memory:")
    second = MemoryStore(":memory:")
    first.add("private first note")
    assert second.search("private") == []
    first.close()
    second.close()
