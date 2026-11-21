"""
Coordinator / Orchestrator Agent
Infrastructure and pipeline orchestration (NOT counted as one of the 6 domain agents).
Coordinates parallel execution of data collection agents, followed by validation,
scoring, and report generation.
"""
import uuid
import time
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.runtime.runtime import AgentRuntime
from app.agents.research_agent import ResearchDataCollectionAgent
from app.agents.teaching_agent import TeachingLearningDataCollectionAgent
from app.agents.administration_agent import AdministrativeDataCollectionAgent
from app.agents.validation_agent import EvidenceValidationAgent
from app.agents.api_calculation_agent import APICalculationAgent
from app.agents.report_agent import ReportGenerationAgent
from app.tools.database_tools import save_agent_run


class AppraisalCoordinator:
    """
    Central Orchestrator for the Faculty Appraisal Multi-Agent System.
    Manages end-to-end execution flow, error recovery, and state transitions.
    """

    def __init__(self, runtime: AgentRuntime = None):
        self.runtime = runtime or AgentRuntime()
        # The six domain agents
        self.research_agent = ResearchDataCollectionAgent(self.runtime)
        self.teaching_agent = TeachingLearningDataCollectionAgent(self.runtime)
        self.administration_agent = AdministrativeDataCollectionAgent(self.runtime)
        self.validation_agent = EvidenceValidationAgent(self.runtime)
        self.calculation_agent = APICalculationAgent(self.runtime)
        self.report_agent = ReportGenerationAgent(self.runtime)

    def run_appraisal_pipeline(self, faculty_id: str, academic_year: str = "2026-27") -> Dict[str, Any]:
        """
        Execute full appraisal workflow for a given faculty member:
        Phase 1: Parallel data collection (Research, Teaching, Administration)
        Phase 2: Sequential evidence validation
        Phase 3: Deterministic API scoring
        Phase 4: Document and report generation
        """
        run_id = f"APP-{time.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        start_time = time.time()
        pipeline_trace: List[Dict[str, Any]] = []

        def log_event(message: str, agent_name: str = "Coordinator", status: str = "info", details: Any = None):
            pipeline_trace.append({
                "timestamp": time.time(),
                "agent": agent_name,
                "status": status,
                "message": message,
                "details": details or {},
            })

        log_event(f"Coordinator initialized appraisal run for faculty {faculty_id} ({academic_year}).", status="started")
        save_agent_run(run_id, faculty_id, "Coordinator", "Initialize appraisal", "started")

        context = {
            "faculty_id": faculty_id,
            "academic_year": academic_year,
            "run_id": run_id,
        }

        # -------------------------------------------------------------
        # Phase 1: Parallel Data Collection (Research, Teaching, Admin)
        # -------------------------------------------------------------
        log_event("Starting parallel evidence collection across Research, Teaching, and Administration domains.", status="info")

        collection_results = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_agent = {
                executor.submit(self.research_agent.run, context): "Research Agent",
                executor.submit(self.teaching_agent.run, context): "Teaching Agent",
                executor.submit(self.administration_agent.run, context): "Administration Agent",
            }
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    res = future.result()
                    collection_results[agent_name] = res
                    log_event(f"{agent_name} completed evidence collection.", agent_name=agent_name, status="success")
                    save_agent_run(run_id, faculty_id, agent_name, "Data collection", "success", result=res)
                except Exception as exc:
                    log_event(f"{agent_name} encountered an error: {exc}", agent_name=agent_name, status="failed")
                    save_agent_run(run_id, faculty_id, agent_name, "Data collection", "failed", error=str(exc))
                    collection_results[agent_name] = {"status": "failed", "error": str(exc)}

        # -------------------------------------------------------------
        # Phase 2: Evidence Validation Agent
        # -------------------------------------------------------------
        log_event("Passing collected evidence to Evidence Validation Agent.", status="info")
        try:
            val_result = self.validation_agent.run(context)
            log_event("Evidence Validation Agent completed verification checks.", agent_name="Evidence Validation Agent", status="success")
            save_agent_run(run_id, faculty_id, "Evidence Validation Agent", "Evidence validation", "success", result=val_result)
        except Exception as exc:
            log_event(f"Evidence Validation Agent failed: {exc}", agent_name="Evidence Validation Agent", status="failed")
            save_agent_run(run_id, faculty_id, "Evidence Validation Agent", "Evidence validation", "failed", error=str(exc))
            return {
                "run_id": run_id,
                "status": "failed",
                "error": f"Validation step failed: {exc}",
                "trace": pipeline_trace,
            }

        # -------------------------------------------------------------
        # Phase 3: API Calculation Agent
        # -------------------------------------------------------------
        log_event("Passing validated evidence to API Calculation Agent for deterministic scoring.", status="info")
        try:
            calc_result = self.calculation_agent.run(context)
            log_event("API Calculation Agent generated score breakdown.", agent_name="API Calculation Agent", status="success")
            save_agent_run(run_id, faculty_id, "API Calculation Agent", "Score calculation", "success", result=calc_result)
        except Exception as exc:
            log_event(f"API Calculation Agent failed: {exc}", agent_name="API Calculation Agent", status="failed")
            save_agent_run(run_id, faculty_id, "API Calculation Agent", "Score calculation", "failed", error=str(exc))
            return {
                "run_id": run_id,
                "status": "failed",
                "error": f"Scoring step failed: {exc}",
                "trace": pipeline_trace,
            }

        # -------------------------------------------------------------
        # Phase 4: Report Generation Agent
        # -------------------------------------------------------------
        log_event("Passing score breakdown and audit evidence to Report Generation Agent.", status="info")
        try:
            report_result = self.report_agent.run(context)
            log_event("Report Generation Agent generated draft appraisal PDF and JSON.", agent_name="Report Generation Agent", status="success")
            save_agent_run(run_id, faculty_id, "Report Generation Agent", "Report generation", "success", result=report_result)
        except Exception as exc:
            log_event(f"Report Generation Agent failed: {exc}", agent_name="Report Generation Agent", status="failed")
            save_agent_run(run_id, faculty_id, "Report Generation Agent", "Report generation", "failed", error=str(exc))
            return {
                "run_id": run_id,
                "status": "failed",
                "error": f"Report step failed: {exc}",
                "trace": pipeline_trace,
            }

        total_duration_ms = int((time.time() - start_time) * 1000)
        log_event(f"Coordinator completed full pipeline in {total_duration_ms}ms.", status="completed")
        save_agent_run(run_id, faculty_id, "Coordinator", "Full appraisal pipeline", "success", duration_ms=total_duration_ms)

        # Consolidate complete agent traces
        all_agent_steps = []
        for agent in [
            self.research_agent,
            self.teaching_agent,
            self.administration_agent,
            self.validation_agent,
            self.calculation_agent,
            self.report_agent,
        ]:
            all_agent_steps.extend(agent.trace_steps)

        return {
            "run_id": run_id,
            "faculty_id": faculty_id,
            "academic_year": academic_year,
            "status": "COMPLETED",
            "duration_ms": total_duration_ms,
            "collection": collection_results,
            "validation": val_result.get("data"),
            "calculation": calc_result.get("data"),
            "report": report_result.get("data"),
            "pipeline_trace": pipeline_trace,
            "agent_steps": all_agent_steps,
        }
