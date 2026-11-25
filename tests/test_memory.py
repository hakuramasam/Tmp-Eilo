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
    try:
        memory.add("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("blank memory should be rejected")
