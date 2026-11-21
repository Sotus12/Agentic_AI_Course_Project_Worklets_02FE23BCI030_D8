"""
Tests for Lab 6: OpenCLA/OpenClaw-style Runtime
Validates:
- receive_task() / select_skill() flow
- SKILL_REGISTRY extensibility: adding a new skill WITHOUT modifying runtime core
- Successful execution recording in audit log
- Failed execution recording in audit log
"""
import pytest
from app.runtime.runtime import AgentRuntime
from app.runtime.skill_registry import SkillRegistry
from app.runtime.audit import AuditLogger
from app.skills.base_skill import BaseSkill


class CustomPatentAnalysisSkill(BaseSkill):
    """A completely new skill added dynamically to prove runtime extensibility."""
    name = "custom_patent_analysis"
    description = "Analyze novel patent submissions for international filings"
    version = "1.0"
    allowed_tools = ["read_csv"]

    def execute(self, task_input, tool_registry, memory, **kwargs):
        patents_count = task_input.get("patents_count", 0)
        return {
            "status": "success",
            "data": {
                "evaluated_patents": patents_count,
                "commercial_viability": "High",
            },
            "tool_calls_trace": [],
        }


def test_runtime_successful_execution():
    """Verify standard task execution and audit logging in the runtime."""
    runtime = AgentRuntime()
    result = runtime.receive_task(
        task_description="Execute research_appraisal data collection",
        task_input={"faculty_id": "FAC001"},
        faculty_id="FAC001",
    )
    assert result["status"] == "success"
    assert result["skill"] == "research_appraisal"
    assert "publications" in result["result"]

    # Verify audit log entry was created
    audit = AuditLogger()
    logs = audit.get_logs(run_id=result["run_id"])
    assert len(logs) >= 1
    assert logs[0]["status"] == "success"
    assert logs[0]["skill"] == "research_appraisal"


def test_runtime_failed_execution_unrecognized_skill():
    """Verify runtime handles unknown task gracefully and logs failure."""
    runtime = AgentRuntime()
    result = runtime.receive_task(
        task_description="Perform quantum computing trajectory prediction",
        task_input={},
        faculty_id="FAC001",
    )
    assert result["status"] == "failed"
    assert "No registered skill found" in result["error"]

    # Verify audit log has the failure
    audit = AuditLogger()
    logs = audit.get_logs(run_id=result["run_id"])
    assert len(logs) >= 1
    assert logs[0]["status"] == "failed"
    assert logs[0]["skill"] is None


def test_runtime_add_new_skill_without_core_modification():
    """
    CRITICAL INSTRUCTOR TEST:
    Can the runtime add a new skill without code rewrite?
    Registers a custom skill and executes it through receive_task.
    """
    registry = SkillRegistry()
    runtime = AgentRuntime(skill_registry=registry)

    # 1. Register new skill dynamically
    registry.register(CustomPatentAnalysisSkill)

    # 2. Verify skill is listed in registry
    skills = registry.list_skills()
    skill_names = [s["name"] for s in skills]
    assert "custom_patent_analysis" in skill_names

    # 3. Execute new skill via receive_task without ANY change to AgentRuntime!
    result = runtime.receive_task(
        task_description="Run custom_patent_analysis on latest disclosures",
        task_input={"patents_count": 3},
        faculty_id="FAC001",
    )

    assert result["status"] == "success"
    assert result["skill"] == "custom_patent_analysis"
    assert result["result"]["evaluated_patents"] == 3
    assert result["result"]["commercial_viability"] == "High"
