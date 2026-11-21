"""
API Calculation Agent (Domain Agent 5)
Responsibilities:
- Load configurable scoring rules
- Use ONLY validated evidence
- Calculate deterministic research, teaching, and administration scores
- Explain scoring breakdown
Note: "API" refers to the faculty appraisal scoring concept in the project problem statement.
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class APICalculationAgent(BaseAgent):
    def __init__(self, runtime):
        super().__init__("API Calculation Agent", runtime)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = context.get("faculty_id")
        run_id = context.get("run_id")
        academic_year = context.get("academic_year", "2026-27")

        # 1. PLAN
        self.record_step(
            stage="PLAN",
            message=f"Plan to execute deterministic score calculation for {faculty_id}. Filtering strictly on VALID evidence according to config/scoring_rules.json.",
        )

        # 2. ACT
        self.record_step(
            stage="ACT",
            message="Invoking 'api_calculation' skill via Agent Runtime.",
        )
        task_result = self.runtime.receive_task(
            task_description="Execute api_calculation deterministic scoring",
            task_input={
                "faculty_id": faculty_id,
                "run_id": run_id,
                "academic_year": academic_year,
            },
            run_id=run_id,
            faculty_id=faculty_id,
        )

        # 3. OBSERVE
        skill_data = task_result.get("result", {})
        scores = skill_data.get("scores", {})
        total_score = scores.get("total", 0.0)
        res_score = scores.get("research", 0.0)
        tea_score = scores.get("teaching", 0.0)
        adm_score = scores.get("administration", 0.0)

        prev_app = skill_data.get("previous_appraisal")
        prev_score = prev_app.get("total_score") if prev_app else None
        diff = round(total_score - prev_score, 2) if prev_score is not None else None

        self.record_step(
            stage="OBSERVE",
            message=f"Calculated Scores -> Research: {res_score}/40, Teaching: {tea_score}/40, Admin: {adm_score}/20 | Total: {total_score}/100. Previous score: {prev_score} (Diff: {diff:+}).",
            details=scores,
        )

        # 4. DECIDE
        self.record_step(
            stage="DECIDE",
            message="Scores committed to appraisal database with status 'DRAFT'. Handing off to Report Generation Agent.",
            details={"total_score": total_score, "score_delta": diff},
        )

        return {
            "agent": self.name,
            "status": task_result.get("status", "success"),
            "data": skill_data,
            "trace_steps": self.trace_steps,
        }
