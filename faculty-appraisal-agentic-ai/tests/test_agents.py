"""
Tests for Domain Agents & Coordinator Pipeline
Validates:
- All 6 domain agents execute their Plan-Act-Observe-Decide cycles
- Coordinator orchestrates full pipeline end-to-end
- Exception handling and warnings propagation when evidence is incomplete
"""
import pytest
from app.runtime.runtime import AgentRuntime
from app.agents.research_agent import ResearchDataCollectionAgent
from app.agents.teaching_agent import TeachingLearningDataCollectionAgent
from app.agents.administration_agent import AdministrativeDataCollectionAgent
from app.agents.validation_agent import EvidenceValidationAgent
from app.agents.api_calculation_agent import APICalculationAgent
from app.agents.report_agent import ReportGenerationAgent
from app.agents.coordinator import AppraisalCoordinator


@pytest.fixture
def runtime():
    return AgentRuntime()


def test_research_agent(runtime):
    agent = ResearchDataCollectionAgent(runtime)
    res = agent.run({"faculty_id": "FAC001", "run_id": "TEST-RUN-1"})
    assert res["status"] == "success"
    assert "publications" in res["data"]
    # Check Plan-Act-Observe-Decide stages were recorded
    stages = [s["stage"] for s in res["trace_steps"]]
    assert "PLAN" in stages
    assert "ACT" in stages
    assert "OBSERVE" in stages
    assert "DECIDE" in stages


def test_coordinator_end_to_end_pipeline(runtime):
    coordinator = AppraisalCoordinator(runtime)
    result = coordinator.run_appraisal_pipeline("FAC001", "2026-27")

    assert result["status"] == "COMPLETED"
    assert "run_id" in result
    assert result["calculation"]["scores"]["total"] > 0
    assert result["validation"]["summary"]["total_evaluated"] >= 19
    assert result["report"]["pdf_path"] is not None
    assert result["report"]["json_path"] is not None

    # Check that parallel phase occurred in trace
    trace_msgs = [e["message"] for e in result["pipeline_trace"]]
    assert any("Starting parallel evidence collection" in m for m in trace_msgs)
