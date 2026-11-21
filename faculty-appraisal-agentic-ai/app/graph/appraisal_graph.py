"""
Concrete Appraisal Node Graph (Lab 7 / Core Concept 7)
Maps Team 8 Faculty Appraisal workflow into an explicit DAG with:
- Intake Node
- Parallel Data Collection (3 sub-nodes)
- Validation Node
- Quality Evaluation Conditional Branch (Clean vs Audit Flagging)
- API Scoring Node
- Human-in-the-Loop Review Gate (with state pausing/resuming)
- Report Generation Node
- Audit & Archive Node
"""
from typing import Dict, Any, Optional
from app.graph.engine import StateGraph, Node, ConditionEdge, ParallelBranchNode, HumanGateNode
from app.runtime.runtime import AgentRuntime
from app.tools.database_tools import query_faculty_data, save_agent_run, save_appraisal_result
from app.tools.report_tools import generate_json, generate_pdf


class IntakeNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("IntakeNode", "Validates faculty profile & context")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = state.get("faculty_id", "FAC001")
        academic_year = state.get("academic_year", "2026-27")
        res = query_faculty_data(faculty_id)
        if not res.get("data"):
            raise ValueError(f"Faculty record not found for ID '{faculty_id}'")
        return {
            "faculty_id": faculty_id,
            "academic_year": academic_year,
            "faculty_profile": res["data"],
            "intake_status": "VALID",
        }


class ResearchCollectionNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("ResearchCollectionNode", "Collects scholarship & grants")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = state["faculty_id"]
        res = self.runtime.receive_task(
            "Execute research_appraisal data collection",
            {"faculty_id": faculty_id},
            run_id=state.get("run_id"),
            faculty_id=faculty_id,
        )
        return {"research_data": res.get("result", {})}


class TeachingCollectionNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("TeachingCollectionNode", "Collects pedagogy & feedback")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = state["faculty_id"]
        res = self.runtime.receive_task(
            "Execute teaching_appraisal data collection",
            {"faculty_id": faculty_id},
            run_id=state.get("run_id"),
            faculty_id=faculty_id,
        )
        return {"teaching_data": res.get("result", {})}


class AdminCollectionNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("AdminCollectionNode", "Collects institutional service")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = state["faculty_id"]
        res = self.runtime.receive_task(
            "Execute administration_appraisal data collection",
            {"faculty_id": faculty_id},
            run_id=state.get("run_id"),
            faculty_id=faculty_id,
        )
        return {"administration_data": res.get("result", {})}


class EvidenceValidationNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("EvidenceValidationNode", "Validates completeness & flags anomalies")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = state["faculty_id"]
        res = self.runtime.receive_task(
            "Execute evidence_validation verification",
            {"faculty_id": faculty_id, "run_id": state.get("run_id")},
            run_id=state.get("run_id"),
            faculty_id=faculty_id,
        )
        val_data = res.get("result", {})
        summary = val_data.get("summary", {})
        has_anomalies = (summary.get("needs_review", 0) > 0 or summary.get("invalid", 0) > 0)
        return {
            "validation_data": val_data,
            "validation_summary": summary,
            "has_anomalies": has_anomalies,
        }


class AuditFlaggingNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("AuditFlaggingNode", "Tags compliance warnings & review flags")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        summary = state.get("validation_summary", {})
        audit_warnings = [
            f"Flagged {summary.get('needs_review', 0)} evidence items requiring human verification.",
            f"Detected {summary.get('invalid', 0)} invalid evidence records excluded from score computation.",
        ]
        return {"audit_flagged": True, "graph_audit_warnings": audit_warnings}


class ScoringNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("ScoringNode", "Deterministic API score computation")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = state["faculty_id"]
        res = self.runtime.receive_task(
            "Execute api_calculation deterministic scoring",
            {"faculty_id": faculty_id, "run_id": state.get("run_id")},
            run_id=state.get("run_id"),
            faculty_id=faculty_id,
        )
        calc_data = res.get("result", {})
        return {
            "scoring_data": calc_data,
            "total_score": calc_data.get("scores", {}).get("total", 0.0),
        }


class ReportGenerationNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("ReportGenerationNode", "Synthesizes PDF and JSON appraisal reports")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = state["faculty_id"]
        run_id = state.get("run_id")
        res = self.runtime.receive_task(
            "Execute report_generation compile and render",
            {"faculty_id": faculty_id, "run_id": run_id},
            run_id=run_id,
            faculty_id=faculty_id,
        )
        report_data = res.get("result", {})
        return {
            "report_data": report_data,
            "pdf_path": report_data.get("pdf_path"),
            "json_path": report_data.get("json_path"),
        }


class ArchiveAndAuditNode(Node):
    def __init__(self, runtime: AgentRuntime):
        super().__init__("ArchiveAndAuditNode", "Persists final graph record and metrics")
        self.runtime = runtime

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        run_id = state.get("run_id")
        faculty_id = state.get("faculty_id")
        status = state.get("gate_status", "APPROVED")
        save_agent_run(run_id, faculty_id, "NodeGraphEngine", "Graph execution completed", "success")
        return {
            "final_status": "ARCHIVED",
            "archived_run_id": run_id,
            "completed": True,
        }


def create_appraisal_node_graph(runtime: Optional[AgentRuntime] = None) -> StateGraph:
    """Builds and compiles the complete DAG appraisal workflow."""
    runtime = runtime or AgentRuntime()
    graph = StateGraph("FacultyAppraisalNodeGraph")

    # 1. Instantiate Nodes
    intake = IntakeNode(runtime)
    parallel_collection = ParallelBranchNode(
        "ParallelCollectionBranch",
        branch_nodes=[
            ResearchCollectionNode(runtime),
            TeachingCollectionNode(runtime),
            AdminCollectionNode(runtime),
        ],
        description="Forks 3 domain collectors concurrently",
    )
    validation = EvidenceValidationNode(runtime)
    flagging = AuditFlaggingNode(runtime)
    scoring = ScoringNode(runtime)
    human_gate = HumanGateNode(
        "HumanReviewGate",
        review_topic="Faculty Performance Score Verification",
        description="Evaluator sign-off gate before finalization",
    )
    reporting = ReportGenerationNode(runtime)
    archive = ArchiveAndAuditNode(runtime)

    # 2. Add Nodes to Graph
    graph.add_node(intake)
    graph.add_node(parallel_collection)
    graph.add_node(validation)
    graph.add_node(flagging)
    graph.add_node(scoring)
    graph.add_node(human_gate)
    graph.add_node(reporting)
    graph.add_node(archive)

    # 3. Configure Entry & Edges
    graph.set_entry_point("IntakeNode")
    graph.add_edge("IntakeNode", "ParallelCollectionBranch")
    graph.add_edge("ParallelCollectionBranch", "EvidenceValidationNode")

    # 4. Conditional Edge: Quality Evaluation
    # If anomalies exist -> Route to AuditFlaggingNode, otherwise straight to ScoringNode
    graph.add_conditional_edge(
        ConditionEdge(
            source="EvidenceValidationNode",
            true_target="AuditFlaggingNode",
            false_target="ScoringNode",
            condition_fn=lambda s: s.get("has_anomalies", False),
            description="Has unvalidated/invalid items?",
        )
    )
    graph.add_edge("AuditFlaggingNode", "ScoringNode")
    graph.add_edge("ScoringNode", "HumanReviewGate")
    graph.add_edge("HumanReviewGate", "ReportGenerationNode")
    graph.add_edge("ReportGenerationNode", "ArchiveAndAuditNode")
    graph.add_finish_point("ArchiveAndAuditNode")

    return graph
