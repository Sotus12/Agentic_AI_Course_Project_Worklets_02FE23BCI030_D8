"""
Database tools — query_faculty_data, get_evidence, save_validation_result,
save_appraisal_result, get_previous_appraisal.
All database operations are auditable tool calls.
"""
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.database.database import execute_query, execute_write


def query_faculty_data(faculty_id: str) -> dict:
    """Query faculty profile from the database."""
    try:
        rows = execute_query("SELECT * FROM faculty WHERE faculty_id = ?", (faculty_id,))
        if not rows:
            return {"status": "error", "error": f"Faculty {faculty_id} not found"}
        return {"status": "success", "data": rows[0]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_evidence(faculty_id: str, category: str = None) -> dict:
    """Get evidence records for a faculty, optionally filtered by category."""
    try:
        if category:
            rows = execute_query(
                "SELECT * FROM evidence WHERE faculty_id = ? AND category = ?",
                (faculty_id, category)
            )
        else:
            rows = execute_query(
                "SELECT * FROM evidence WHERE faculty_id = ?",
                (faculty_id,)
            )
        return {"status": "success", "evidence": rows, "count": len(rows)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_validation_results(faculty_id: str, run_id: str) -> dict:
    """Get validation results for a specific appraisal run."""
    try:
        rows = execute_query(
            "SELECT v.*, e.title, e.category, e.sub_category FROM validation_results v "
            "JOIN evidence e ON v.evidence_id = e.evidence_id "
            "WHERE v.faculty_id = ? AND v.run_id = ?",
            (faculty_id, run_id)
        )
        return {"status": "success", "validations": rows, "count": len(rows)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def save_validation_result(evidence_id: int, faculty_id: str, run_id: str,
                           status: str, reason: str) -> dict:
    """Save a validation result for a piece of evidence."""
    try:
        row_id = execute_write(
            "INSERT INTO validation_results (evidence_id, faculty_id, run_id, status, reason) VALUES (?,?,?,?,?)",
            (evidence_id, faculty_id, run_id, status, reason)
        )
        return {"status": "success", "validation_id": row_id}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def save_appraisal_result(faculty_id: str, run_id: str, academic_year: str,
                          research_score: float, teaching_score: float,
                          administration_score: float, total_score: float,
                          score_breakdown: dict) -> dict:
    """Save the calculated appraisal result."""
    try:
        row_id = execute_write(
            """INSERT INTO appraisal_results
            (faculty_id, run_id, academic_year, research_score, teaching_score,
             administration_score, total_score, max_score, score_breakdown, status)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (faculty_id, run_id, academic_year, research_score, teaching_score,
             administration_score, total_score, 100.0, json.dumps(score_breakdown), "DRAFT")
        )
        return {"status": "success", "appraisal_id": row_id}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_previous_appraisal(faculty_id: str) -> dict:
    """Get the most recent previous appraisal result for comparison."""
    try:
        rows = execute_query(
            "SELECT * FROM appraisal_results WHERE faculty_id = ? ORDER BY created_at DESC LIMIT 1",
            (faculty_id,)
        )
        if not rows:
            return {"status": "success", "data": None, "message": "No previous appraisal found"}
        result = rows[0]
        if result.get("score_breakdown"):
            result["score_breakdown"] = json.loads(result["score_breakdown"])
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def save_agent_run(run_id: str, faculty_id: str, agent_name: str, task: str,
                   status: str, result: dict = None, error: str = None,
                   duration_ms: int = None) -> dict:
    """Record an agent run."""
    try:
        row_id = execute_write(
            """INSERT INTO agent_runs (run_id, faculty_id, agent_name, task, status, result, error, duration_ms, completed_at)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (run_id, faculty_id, agent_name, task, status,
             json.dumps(result) if result else None, error, duration_ms,
             datetime.now().isoformat() if status != "started" else None)
        )
        return {"status": "success", "id": row_id}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# Tool registry entry
TOOLS = {
    "query_faculty_data": {
        "function": query_faculty_data,
        "description": "Query faculty profile from database",
        "inputs": ["faculty_id"],
    },
    "get_evidence": {
        "function": get_evidence,
        "description": "Get evidence records for a faculty, optionally by category",
        "inputs": ["faculty_id", "category"],
    },
    "get_validation_results": {
        "function": get_validation_results,
        "description": "Get validation results for a run",
        "inputs": ["faculty_id", "run_id"],
    },
    "save_validation_result": {
        "function": save_validation_result,
        "description": "Save a validation result for evidence",
        "inputs": ["evidence_id", "faculty_id", "run_id", "status", "reason"],
    },
    "save_appraisal_result": {
        "function": save_appraisal_result,
        "description": "Save calculated appraisal scores",
        "inputs": ["faculty_id", "run_id", "academic_year", "research_score",
                    "teaching_score", "administration_score", "total_score", "score_breakdown"],
    },
    "get_previous_appraisal": {
        "function": get_previous_appraisal,
        "description": "Get previous appraisal for comparison",
        "inputs": ["faculty_id"],
    },
    "save_agent_run": {
        "function": save_agent_run,
        "description": "Record an agent execution run",
        "inputs": ["run_id", "faculty_id", "agent_name", "task", "status"],
    },
}
