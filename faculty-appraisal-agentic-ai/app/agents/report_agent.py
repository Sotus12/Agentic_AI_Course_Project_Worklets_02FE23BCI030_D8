"""
Report Generation Agent (Domain Agent 6)
Responsibilities:
- Retrieve faculty profile, validated evidence, and appraisal results
- Generate PDF appraisal report
- Generate JSON appraisal result
- Mark status as "DRAFT — Awaiting Human Review"
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class ReportGenerationAgent(BaseAgent):
    def __init__(self, runtime):
        super().__init__("Report Generation Agent", runtime)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = context.get("faculty_id")
        run_id = context.get("run_id")

        # 1. PLAN
        self.record_step(
            stage="PLAN",
            message=f"Plan to generate formal appraisal documentation for {faculty_id}. Target formats: PDF executive summary and full JSON payload.",
        )

        # 2. ACT
        self.record_step(
            stage="ACT",
            message="Invoking 'report_generation' skill via Agent Runtime.",
        )
        task_result = self.runtime.receive_task(
            task_description="Execute report_generation compile and render",
            task_input={"faculty_id": faculty_id, "run_id": run_id},
            run_id=run_id,
            faculty_id=faculty_id,
        )

        # 3. OBSERVE
        skill_data = task_result.get("result", {})
        pdf_path = skill_data.get("pdf_path")
        json_path = skill_data.get("json_path")
        warnings_count = skill_data.get("warnings_count", 0)

        self.record_step(
            stage="OBSERVE",
            message=f"Generated PDF ({pdf_path}) and JSON ({json_path}). Embedded {warnings_count} audit warnings.",
            details={"pdf": pdf_path, "json": json_path, "warnings_count": warnings_count},
        )

        # 4. DECIDE
        self.record_step(
            stage="DECIDE",
            message="Appraisal reports finalized with status 'DRAFT — Awaiting Human Review'. Workflow complete.",
            details={"status": "DRAFT — Awaiting Human Review"},
        )

        return {
            "agent": self.name,
            "status": task_result.get("status", "success"),
            "data": skill_data,
            "trace_steps": self.trace_steps,
        }
