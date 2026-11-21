"""
Administration Appraisal Skill (Lab 3)
Collects and structures administration evidence for faculty appraisal.
"""
from typing import Dict, Any, List
from app.skills.base_skill import BaseSkill


class AdministrationAppraisalSkill(BaseSkill):
    name = "administration_appraisal"
    description = "Collect and structure administration evidence for faculty appraisal"
    version = "1.0"
    allowed_tools = ["read_csv", "read_file", "get_evidence"]

    def execute(self, task_input: Dict[str, Any], tool_registry, memory, **kwargs) -> Dict[str, Any]:
        faculty_id = task_input.get("faculty_id")
        if not faculty_id:
            raise ValueError("faculty_id is required for administration_appraisal")

        tool_calls_trace = []

        # Read CSV files
        com_res = tool_registry.execute("read_csv", self.allowed_tools, file_path="administration/committees.csv", faculty_id=faculty_id)
        tool_calls_trace.append(com_res)
        committees = com_res.get("result", {}).get("rows", [])

        resp_res = tool_registry.execute("read_csv", self.allowed_tools, file_path="administration/responsibilities.csv", faculty_id=faculty_id)
        tool_calls_trace.append(resp_res)
        responsibilities = resp_res.get("result", {}).get("rows", [])

        act_res = tool_registry.execute("read_csv", self.allowed_tools, file_path="administration/activities.csv", faculty_id=faculty_id)
        tool_calls_trace.append(act_res)
        activities = act_res.get("result", {}).get("rows", [])

        summary = {
            "committee_memberships": len(committees),
            "coordinator_roles": len(responsibilities),
            "institutional_activities": len(activities),
            "total_items": len(committees) + len(responsibilities) + len(activities),
        }

        result_data = {
            "faculty_id": faculty_id,
            "category": "administration",
            "committees": committees,
            "responsibilities": responsibilities,
            "activities": activities,
            "summary": summary,
        }

        # Update scoped memory
        if memory:
            memory.set("administration_evidence", result_data)

        return {
            "status": "success",
            "data": result_data,
            "tool_calls_trace": tool_calls_trace
        }
