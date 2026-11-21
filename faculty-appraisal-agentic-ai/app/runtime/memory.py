"""
Scoped Memory System (Lab 4)
Simple persistent memory backed by SQLite.
Memory is scoped per faculty/user to prevent cross-contamination.
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.database.database import get_connection


class ScopedMemory:
    """
    Scoped memory system — each faculty's memory is isolated.

    Usage:
        memory = ScopedMemory()
        mem = memory.scope("FAC001")
        mem.set("profile", {"name": "Dr. Rao"})
        profile = mem.get("profile")
    """

    def __init__(self):
        self._scope_id = None

    def scope(self, user_id: str) -> "ScopedMemory":
        """Create a scoped memory instance for a specific user/faculty."""
        scoped = ScopedMemory()
        scoped._scope_id = f"faculty:{user_id}"
        return scoped

    def _ensure_scope(self):
        if not self._scope_id:
            raise ValueError("Memory must be scoped before use. Call memory.scope(user_id) first.")

    def get(self, key: str, default=None):
        """Retrieve a value from scoped memory."""
        self._ensure_scope()
        conn = get_connection()
        try:
            cursor = conn.execute(
                "SELECT value FROM memory WHERE scope = ? AND key = ?",
                (self._scope_id, key)
            )
            row = cursor.fetchone()
            if row:
                try:
                    return json.loads(row[0])
                except (json.JSONDecodeError, TypeError):
                    return row[0]
            return default
        finally:
            conn.close()

    def set(self, key: str, value) -> None:
        """Store a value in scoped memory."""
        self._ensure_scope()
        conn = get_connection()
        try:
            serialized = json.dumps(value) if not isinstance(value, str) else value
            conn.execute(
                "INSERT OR REPLACE INTO memory (scope, key, value, updated_at) VALUES (?, ?, ?, ?)",
                (self._scope_id, key, serialized, datetime.now().isoformat())
            )
            conn.commit()
        finally:
            conn.close()

    def get_all(self) -> dict:
        """Retrieve all key-value pairs in the current scope."""
        self._ensure_scope()
        conn = get_connection()
        try:
            cursor = conn.execute(
                "SELECT key, value FROM memory WHERE scope = ?",
                (self._scope_id,)
            )
            result = {}
            for row in cursor.fetchall():
                try:
                    result[row[0]] = json.loads(row[1])
                except (json.JSONDecodeError, TypeError):
                    result[row[0]] = row[1]
            return result
        finally:
            conn.close()

    def delete(self, key: str) -> None:
        """Delete a key from scoped memory."""
        self._ensure_scope()
        conn = get_connection()
        try:
            conn.execute(
                "DELETE FROM memory WHERE scope = ? AND key = ?",
                (self._scope_id, key)
            )
            conn.commit()
        finally:
            conn.close()

    @property
    def scope_id(self) -> str:
        return self._scope_id
