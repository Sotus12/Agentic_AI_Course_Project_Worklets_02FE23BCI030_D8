"""
Research Data Collection Agent (Domain Agent 1)
Responsibilities:
- Identify research evidence
- Read research files
- Extract research information
- Categorize evidence
- Return structured research data
"""
from typing import Dict, Any
from app.agents.base_agent import BaseAgent


class ResearchDataCollectionAgent(BaseAgent):
    def __init__(self, runtime):
        super().__init__("Research Data Collection Agent", runtime)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        faculty_id = context.get("faculty_id")
        run_id = context.get("run_id")

        # 1. PLAN
        self.record_step(
            stage="PLAN",
            message=f"Plan to collect research data for faculty {faculty_id}. Target files: publications, conferences, patents, projects.",
        )

        # 2. ACT - Dispatch task to runtime skill
        self.record_step(
            stage="ACT",
            message="Invoking 'research_appraisal' skill via Agent Runtime.",
        )
        task_result = self.runtime.receive_task(
            task_description="Execute research_appraisal data collection",
            task_input={"faculty_id": faculty_id},
            run_id=run_id,
            faculty_id=faculty_id,
        )

        # 3. OBSERVE
        skill_data = task_result.get("result", {})
        summary = skill_data.get("summary", {})
        pubs_count = summary.get("publications_count", 0)
        confs_count = summary.get("conferences_count", 0)
        pat_count = summary.get("patents_count", 0)
        proj_count = summary.get("projects_count", 0)

        # Check for missing file attachments in publications
        pubs = skill_data.get("publications", [])
        unattached_pubs = [p.get("title") for p in pubs if not p.get("file_ref")]

        self.record_step(
            stage="OBSERVE",
            message=f"Retrieved {pubs_count} publications, {confs_count} conferences, {pat_count} patents, {proj_count} projects. Detected {len(unattached_pubs)} unattached publication files.",
            details={"unattached_publications": unattached_pubs},
        )

        # 4. DECIDE
        decision_notes = []
        if unattached_pubs:
            decision_notes.append(f"Flagged {len(unattached_pubs)} publications with missing file references for validation review.")

        self.record_step(
            stage="DECIDE",
            message="Structured research dataset ready. Forwarding to coordinator pipeline.",
            details={"decision_notes": decision_notes},
        )

        return {
            "agent": self.name,
            "status": task_result.get("status", "success"),
            "data": skill_data,
            "trace_steps": self.trace_steps,
            "warnings": decision_notes,
        }
