"""
Administrative Data Collection Agent (Domain Agent 3)
Responsibilities:
- Read administrative evidence
- Identify committee memberships
- Identify coordinator/responsibility roles
- Identify institutional activities
- Return structured administrative data
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class AdministrativeDataCollectionAgent(BaseAgent):
    def __init__(self, runtime):
        super().__init__("Administrative Data Collection Agent", runtime)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = context.get("faculty_id")
        run_id = context.get("run_id")

        # 1. PLAN
        self.record_step(
            stage="PLAN",
            message=f"Plan to extract administrative commitments for faculty {faculty_id}. Target sets: committees, coordinator roles, institutional events.",
        )

        # 2. ACT
        self.record_step(
            stage="ACT",
            message="Invoking 'administration_appraisal' skill via Agent Runtime.",
        )
        task_result = self.runtime.receive_task(
            task_description="Execute administration_appraisal evidence gathering",
            task_input={"faculty_id": faculty_id},
            run_id=run_id,
            faculty_id=faculty_id,
        )

        # 3. OBSERVE
        skill_data = task_result.get("result", {})
        summary = skill_data.get("summary", {})
        comms = summary.get("committee_memberships", 0)
        roles = summary.get("coordinator_roles", 0)
        acts = summary.get("institutional_activities", 0)

        self.record_step(
            stage="OBSERVE",
            message=f"Identified {comms} committee assignments, {roles} coordination responsibilities, and {acts} institutional events.",
            details=summary,
        )

        # 4. DECIDE
        self.record_step(
            stage="DECIDE",
            message="Administrative dataset compiled. Ready for evidence validation.",
        )

        return {
            "agent": self.name,
            "status": task_result.get("status", "success"),
            "data": skill_data,
            "trace_steps": self.trace_steps,
        }
