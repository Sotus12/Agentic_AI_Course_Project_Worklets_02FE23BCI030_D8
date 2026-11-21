"""
Evidence Validation Agent (Domain Agent 4)
Responsibilities:
- Validate evidence completeness, file existence, and duplicates
- Assign statuses: VALID, INVALID, NEEDS_REVIEW
- Provide validation rationales
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class EvidenceValidationAgent(BaseAgent):
    def __init__(self, runtime):
        super().__init__("Evidence Validation Agent", runtime)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = context.get("faculty_id")
        run_id = context.get("run_id")

        # 1. PLAN
        self.record_step(
            stage="PLAN",
            message=f"Plan to validate all collected evidence items for faculty {faculty_id}. Verifying file integrity, duplicate submissions, and required schemas.",
        )

        # 2. ACT
        self.record_step(
            stage="ACT",
            message="Invoking 'evidence_validation' skill via Agent Runtime.",
        )
        task_result = self.runtime.receive_task(
            task_description="Execute evidence_validation verification suite",
            task_input={"faculty_id": faculty_id, "run_id": run_id},
            run_id=run_id,
            faculty_id=faculty_id,
        )

        # 3. OBSERVE
        skill_data = task_result.get("result", {})
        summary = skill_data.get("summary", {})
        valid_count = summary.get("VALID", 0)
        invalid_count = summary.get("INVALID", 0)
        needs_review_count = summary.get("NEEDS_REVIEW", 0)

        self.record_step(
            stage="OBSERVE",
            message=f"Validation completed: {valid_count} VALID, {invalid_count} INVALID, {needs_review_count} NEEDS_REVIEW.",
            details=summary,
        )

        # 4. DECIDE
        decision = "Validation complete. Filtered only VALID evidence items for deterministic API scoring."
        if needs_review_count > 0:
            decision += f" Noted {needs_review_count} items requiring administrative human verification."

        self.record_step(
            stage="DECIDE",
            message=decision,
            details={"valid_ratio": f"{valid_count}/{summary.get('total_evaluated', 0)}"},
        )

        return {
            "agent": self.name,
            "status": task_result.get("status", "success"),
            "data": skill_data,
            "trace_steps": self.trace_steps,
        }
