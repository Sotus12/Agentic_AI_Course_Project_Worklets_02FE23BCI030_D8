"""
Research Appraisal Skill (Lab 3)
Collects and structures research evidence for faculty appraisal.
"""
from typing import Dict, Any, List
from app.skills.base_skill import BaseSkill


class ResearchAppraisalSkill(BaseSkill):
    name = "research_appraisal"
    description = "Collect and structure research evidence for faculty appraisal"
    version = "1.0"
    allowed_tools = ["read_csv", "read_pdf", "read_file", "get_evidence"]

    def execute(self, task_input: Dict[str, Any], tool_registry, memory, **kwargs) -> Dict[str, Any]:
        faculty_id = task_input.get("faculty_id")
        if not faculty_id:
            raise ValueError("faculty_id is required for research_appraisal")

        tool_calls_trace = []

        # Read CSV files for research data
        res_pubs = tool_registry.execute("read_csv", self.allowed_tools, file_path="research/publications.csv", faculty_id=faculty_id)
        tool_calls_trace.append(res_pubs)
        publications = res_pubs.get("result", {}).get("rows", [])

        res_confs = tool_registry.execute("read_csv", self.allowed_tools, file_path="research/conferences.csv", faculty_id=faculty_id)
        tool_calls_trace.append(res_confs)
        conferences = res_confs.get("result", {}).get("rows", [])

        res_pats = tool_registry.execute("read_csv", self.allowed_tools, file_path="research/patents.csv", faculty_id=faculty_id)
        tool_calls_trace.append(res_pats)
        patents = res_pats.get("result", {}).get("rows", [])

        res_projs = tool_registry.execute("read_csv", self.allowed_tools, file_path="research/projects.csv", faculty_id=faculty_id)
        tool_calls_trace.append(res_projs)
        projects = res_projs.get("result", {}).get("rows", [])

        # Also verify database registered evidence
        db_ev = tool_registry.execute("get_evidence", self.allowed_tools, faculty_id=faculty_id, category="research")
        tool_calls_trace.append(db_ev)
        db_evidence = db_ev.get("result", {}).get("evidence", [])

        summary = {
            "publications_count": len(publications),
            "conferences_count": len(conferences),
            "patents_count": len(patents),
            "projects_count": len(projects),
            "total_items": len(publications) + len(conferences) + len(patents) + len(projects)
        }

        result_data = {
            "faculty_id": faculty_id,
            "category": "research",
            "publications": publications,
            "conferences": conferences,
            "patents": patents,
            "projects": projects,
            "db_evidence": db_evidence,
            "summary": summary,
        }

        # Update scoped memory
        if memory:
            memory.set("research_evidence", result_data)

        return {
            "status": "success",
            "data": result_data,
            "tool_calls_trace": tool_calls_trace
        }
