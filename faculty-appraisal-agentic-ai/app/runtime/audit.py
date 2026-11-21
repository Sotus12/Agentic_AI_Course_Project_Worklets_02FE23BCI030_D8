"""
Audit Log System (Lab 6)
Records every task execution, tool calls, memory access, and outcomes.
Structured and queryable via SQLite.
"""
import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.database.database import execute_write, execute_query


class AuditLogger:
    """Structured audit logger for runtime task executions."""

    def __init__(self):
        pass

    def log(
        self,
        run_id: str,
        task: str,
        status: str,
        faculty_id: Optional[str] = None,
        skill: Optional[str] = None,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        memory_access: Optional[Dict[str, Any]] = None,
        mcp_calls: Optional[List[Dict[str, Any]]] = None,
        result_summary: Optional[str] = None,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ) -> int:
        """
        Record a structured audit log entry.
        Status must be 'success', 'failed', or 'partial'.
        """
        query = """
        INSERT INTO audit_logs (
            run_id, faculty_id, task, skill, tool_calls, memory_access,
            mcp_calls, result_summary, status, error, duration_ms
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            run_id,
            faculty_id,
            task,
            skill,
            json.dumps(tool_calls or []),
            json.dumps(memory_access or {}),
            json.dumps(mcp_calls or []),
            result_summary,
            status,
            error,
            duration_ms or 0,
        )
        return execute_write(query, params)

    def get_logs(self, run_id: Optional[str] = None, faculty_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve audit logs, optionally filtered by run_id or faculty_id."""
        if run_id:
            rows = execute_query("SELECT * FROM audit_logs WHERE run_id = ? ORDER BY id ASC", (run_id,))
        elif faculty_id:
            rows = execute_query("SELECT * FROM audit_logs WHERE faculty_id = ? ORDER BY id DESC", (faculty_id,))
        else:
            rows = execute_query("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50")

        # Parse JSON fields for caller convenience
        for row in rows:
            for field in ["tool_calls", "memory_access", "mcp_calls"]:
                if row.get(field):
                    try:
                        row[field] = json.loads(row[field])
                    except (json.JSONDecodeError, TypeError):
                        pass
        return rows
