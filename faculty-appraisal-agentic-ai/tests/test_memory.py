"""
Tests for Lab 4: Memory & Retrieval
Validates:
- Persistent scoped memory isolation (no cross-faculty leakage)
- Get/Set/Delete operations
- Structured state storage
"""
import pytest
from app.runtime.memory import ScopedMemory


def test_memory_scoped_isolation():
    """Verify that memory is strictly scoped and does not leak between faculties."""
    mem_sys = ScopedMemory()

    mem_fac1 = mem_sys.scope("FAC001")
    mem_fac2 = mem_sys.scope("FAC002")

    mem_fac1.set("score", 95.0)
    mem_fac2.set("score", 72.0)

    assert mem_fac1.get("score") == 95.0
    assert mem_fac2.get("score") == 72.0

    mem_fac1.set("confidential_notes", "Faculty 1 special assessment")
    assert mem_fac2.get("confidential_notes") is None


def test_memory_json_serialization():
    """Verify storage of complex structured objects in memory."""
    mem_sys = ScopedMemory()
    mem = mem_sys.scope("FAC_TEST")

    test_data = {
        "publications": 5,
        "awards": ["Best Teacher 2025", "IEEE Senior Member"],
        "metadata": {"approved": False},
    }

    mem.set("test_record", test_data)
    retrieved = mem.get("test_record")

    assert retrieved["publications"] == 5
    assert "Best Teacher 2025" in retrieved["awards"]
    assert retrieved["metadata"]["approved"] is False


def test_memory_unscoped_error():
    """Verify error when operating on unscoped memory instance."""
    mem = ScopedMemory()
    with pytest.raises(ValueError):
        mem.get("any_key")
