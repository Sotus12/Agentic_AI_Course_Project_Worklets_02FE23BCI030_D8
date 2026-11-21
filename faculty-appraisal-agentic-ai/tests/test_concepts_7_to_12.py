"""
Comprehensive Automated Test Suite for Core Concepts 7 through 12:
- Concept 7 (Lab 7): Node Graphs & Conditional Routing
- Concept 8 (Lab 8): Parallel Swarms & Consensus Conflict Resolution
- Concept 9 (Lab 9): Deep Research & Citation Cross-Referencing
- Concept 10 (Lab 10): Cloud Operations & Self-Healing Remediation Gates
- Concept 11 (Lab 11): Agentic SDLC & Automated Requirement Verification
- Concept 12 (Lab 12): Responsible Autonomy, Audit Hash Chain & State Rollback
"""
import pytest
from app.graph.appraisal_graph import create_appraisal_node_graph
from app.graph.engine import StateGraph, Node, ConditionEdge, HumanGateNode
from app.swarm.swarm import AppraisalSwarm
from app.swarm.message_board import MessageBoard
from app.research.deep_research import DeepResearchAgent
from app.cloud.cloud_agent import CloudOperationsAgent, TelemetryProbe
from app.sdlc.sdlc_factory import AgenticSDLCFactory
from app.governance.responsible_autonomy import ResponsibleAutonomyEngine


# ==============================================================================
# Concept 7: Node Graphs (Lab 7)
# ==============================================================================
def test_node_graph_end_to_end_execution():
    graph = create_appraisal_node_graph()
    result = graph.run({
        "faculty_id": "FAC001",
        "academic_year": "2026-27",
        "auto_advance_human_gate": True,
    })
    assert result["graph_status"] == "COMPLETED"
    assert result["total_steps"] >= 6
    assert result["total_score"] > 0
    assert result["final_status"] == "ARCHIVED"


def test_node_graph_human_gate_pause_and_resumption():
    graph = create_appraisal_node_graph()
    ckpt_id = "TEST-CKPT-PAUSE"
    # Execute with human gate pause
    paused_result = graph.run({
        "faculty_id": "FAC001",
        "academic_year": "2026-27",
        "auto_advance_human_gate": False,
    }, checkpoint_id=ckpt_id)

    assert paused_result["graph_status"] == "PAUSED_FOR_HUMAN"
    assert paused_result["gate_status"] == "PAUSED_AWAITING_HUMAN"
    assert ckpt_id in graph.checkpoints

    # Resume from checkpoint with approval
    resumed_result = graph.resume(ckpt_id, human_approval=True, approver_name="Dr. Evaluator")
    assert resumed_result["graph_status"] == "COMPLETED"
    assert resumed_result["final_status"] == "ARCHIVED"


# ==============================================================================
# Concept 8: Parallel Swarms (Lab 8)
# ==============================================================================
def test_swarm_multi_round_consensus_and_critique():
    swarm = AppraisalSwarm()
    context = {
        "collection": {
            "Research Agent": {"data": {"publications": [1, 2, 3], "projects": [1]}},
            "Teaching Agent": {"data": {"courses": [1, 2], "average_student_evaluation": 4.5}},
            "Administration Agent": {"data": {"roles": [1, 2, 3]}},
        },
        "validation": {"summary": {"invalid": 0, "needs_review": 1}},
    }
    result = swarm.run_swarm(context)

    assert result["status"] == "CONSENSUS_REACHED"
    assert "consensus_scores" in result
    assert result["consensus_scores"]["total"] > 0
    assert len(result["round_1_proposals"]) == 4
    assert len(result["round_2_critiques"]) >= 1
    assert len(result["message_board_trace"]) >= 5


# ==============================================================================
# Concept 9: Deep Research (Lab 9)
# ==============================================================================
def test_deep_research_five_phase_loop():
    agent = DeepResearchAgent()
    result = agent.run_research_loop("FAC001")

    assert result["status"] == "COMPLETED"
    assert result["research_integrity_quotient"] >= 50.0
    assert result["bibliometric_summary"]["total_publications_evaluated"] >= 1
    assert len(result["evidence_verification_matrix"]) >= 1
    assert len(result["deep_research_trace"]) == 4

    # Verify at least one paper has verified indexing
    first_item = result["evidence_verification_matrix"][0]
    assert "indexing_status" in first_item
    assert "verified_citations" in first_item


# ==============================================================================
# Concept 10: Cloud Operations (Lab 10)
# ==============================================================================
def test_cloud_agent_signals_diagnosis_and_approval_gate():
    cloud_agent = CloudOperationsAgent()
    signals = cloud_agent.observe_signals()
    assert len(signals) >= 3

    plan = cloud_agent.diagnose_and_plan(signals)
    assert plan.plan_id.startswith("PLAN-")
    assert len(plan.actions) >= 1

    # Verify action execution with approval logic
    first_action = plan.actions[0]
    if first_action.requires_approval:
        denied = cloud_agent.execute_action(plan.plan_id, first_action.action_id, human_approved=False)
        assert denied["status"] == "APPROVAL_REQUIRED"

        approved = cloud_agent.execute_action(plan.plan_id, first_action.action_id, human_approved=True)
        assert approved["status"] == "SUCCESS"
    else:
        executed = cloud_agent.execute_action(plan.plan_id, first_action.action_id)
        assert executed["status"] == "SUCCESS"


# ==============================================================================
# Concept 11: Agentic SDLC (Lab 11)
# ==============================================================================
def test_agentic_sdlc_requirement_synthesis_and_approval():
    factory = AgenticSDLCFactory()
    req = "Add NBA Criterion 5.2 patent commercialization weighting"
    dossier = factory.process_requirement(req)

    assert dossier.status == "AWAITING_LEAD_APPROVAL"
    assert dossier.test_results["all_tests_passed"] is True
    assert "diff" in dossier.generated_code_diff or "scoring_rules" in dossier.generated_code_diff

    # Human sign-off
    release_res = factory.approve_release(dossier.release_id, "Principal Architect")
    assert release_res["status"] == "RELEASED"
    assert dossier.status == "APPROVED_RELEASED"


# ==============================================================================
# Concept 12: Responsible Autonomy & Safety (Lab 12)
# ==============================================================================
def test_responsible_autonomy_audit_chain_and_rollback():
    engine = ResponsibleAutonomyEngine()

    # 1. Cryptographic Hash Chain
    engine.append_audit_block("APPRAISAL_CALCULATED", "RUN-TEST-01", {"score": 88.0})
    engine.append_audit_block("REPORT_APPROVED", "RUN-TEST-01", {"approved_by": "Dean"})
    is_valid, msg = engine.verify_audit_chain()
    assert is_valid is True
    assert "verified" in msg.lower()

    # 2. State Snapshot & Rollback
    snap_id = engine.create_state_snapshot("RUN-TEST-01", "FAC001", {"score": 88.0, "status": "APPROVED"})
    rollback_res = engine.rollback_to_snapshot(snap_id, "Disputed appraisal recalculation", "Appeals Board")
    assert rollback_res["status"] == "ROLLED_BACK"

    # 3. PII Masking
    raw_text = "Reach Dr. Rao at ananya.rao@kletech.ac.in or call 9876543210 regarding medical leave."
    sanitized = engine.sanitize_pii(raw_text)
    assert "ananya.rao@kletech.ac.in" not in sanitized
    assert "[EMAIL_REDACTED]" in sanitized
    assert "[PHONE_REDACTED]" in sanitized
    assert "[CONFIDENTIAL_PII]" in sanitized

    # 4. Demographic Parity Fairness
    fairness = engine.evaluate_fairness()
    assert fairness.disparate_impact_ratio > 0.0

