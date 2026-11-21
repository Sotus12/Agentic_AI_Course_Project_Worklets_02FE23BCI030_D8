"""
FastAPI Backend Application
Exposes REST endpoints for the Faculty Appraisal Multi-Agent System,
including run triggers, audit logs, and MCP discovery.
"""
import os
import sys
import json
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.database import execute_query, execute_write
from app.agents.coordinator import AppraisalCoordinator
from app.runtime.audit import AuditLogger
from app.mcp.client import MCPClient

app = FastAPI(
    title="Faculty Appraisal Management System API",
    description="Multi-Agent System demonstrating Labs 1–6 (OpenCLA Runtime, MCP, Scoped Memory)",
    version="1.0.0",
)

coordinator = AppraisalCoordinator()
audit_logger = AuditLogger()
mcp_client = MCPClient()


class MCPCallRequest(BaseModel):
    capability_name: str
    caller: str
    inputs: Dict[str, Any]


class ApprovalRequest(BaseModel):
    approved_by: str = "Dean of Academic Affairs (Demo)"


@app.get("/")
def read_root():
    return {
        "project": "Faculty Appraisal Management System",
        "scope": "Labs 1–6 (OpenCLA Runtime, MCP, Scoped Memory, Multi-Agent)",
        "status": "operational",
        "demo_faculty_id": "FAC001",
        "policy_note": "Demo Appraisal Policy — configurable; not official institutional scoring policy.",
    }


@app.get("/api/faculty/{faculty_id}")
def get_faculty(faculty_id: str):
    rows = execute_query("SELECT * FROM faculty WHERE faculty_id = ?", (faculty_id,))
    if not rows:
        raise HTTPException(status_code=404, detail=f"Faculty {faculty_id} not found")
    return rows[0]


@app.get("/api/faculty/{faculty_id}/evidence")
def get_faculty_evidence(faculty_id: str, category: Optional[str] = None):
    if category:
        rows = execute_query(
            "SELECT * FROM evidence WHERE faculty_id = ? AND category = ?",
            (faculty_id, category),
        )
    else:
        rows = execute_query("SELECT * FROM evidence WHERE faculty_id = ?", (faculty_id,))
    return {"faculty_id": faculty_id, "count": len(rows), "evidence": rows}


@app.get("/api/scoring/rules")
def get_scoring_rules():
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "config", "scoring_rules.json"
    )
    with open(config_path, "r") as f:
        return json.load(f)


@app.post("/api/appraisal/run/{faculty_id}")
def run_appraisal(faculty_id: str, academic_year: str = "2026-27"):
    """Trigger the multi-agent appraisal pipeline orchestrated by Coordinator."""
    try:
        result = coordinator.run_appraisal_pipeline(faculty_id=faculty_id, academic_year=academic_year)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/appraisal/latest/{faculty_id}")
def get_latest_appraisal(faculty_id: str):
    rows = execute_query(
        "SELECT * FROM appraisal_results WHERE faculty_id = ? ORDER BY created_at DESC LIMIT 1",
        (faculty_id,),
    )
    if not rows:
        return {"data": None, "message": "No appraisal found"}
    result = dict(rows[0])
    if result.get("score_breakdown"):
        try:
            result["score_breakdown"] = json.loads(result["score_breakdown"])
        except Exception:
            pass
    return {"data": result}


@app.post("/api/appraisal/{appraisal_id}/approve")
def approve_appraisal(appraisal_id: int, req: ApprovalRequest):
    """Human-in-the-loop: mark draft appraisal as approved."""
    execute_write(
        "UPDATE appraisal_results SET status = 'APPROVED', approved_by = ?, approved_at = CURRENT_TIMESTAMP WHERE appraisal_id = ?",
        (req.approved_by, appraisal_id),
    )
    return {"status": "success", "message": f"Appraisal {appraisal_id} approved by {req.approved_by}."}


@app.get("/api/audit/logs")
def get_audit_logs(run_id: Optional[str] = None, faculty_id: Optional[str] = None):
    return audit_logger.get_logs(run_id=run_id, faculty_id=faculty_id)


@app.get("/api/mcp/capabilities")
def discover_mcp():
    """Lab 5: Discover MCP capabilities."""
    return mcp_client.discover()


@app.post("/api/mcp/call")
def call_mcp(req: MCPCallRequest):
    """Lab 5: Call MCP capability via discovery client."""
    return mcp_client.call(
        capability_name=req.capability_name,
        caller=req.caller,
        inputs=req.inputs,
    )
