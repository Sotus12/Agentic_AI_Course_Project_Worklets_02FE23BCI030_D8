"""
Teaching-Learning Appraisal Skill (Lab 3)
Collects and structures teaching-learning evidence for faculty appraisal.
"""
from typing import Dict, Any, List
from app.skills.base_skill import BaseSkill


class TeachingAppraisalSkill(BaseSkill):
    name = "teaching_appraisal"
    description = "Collect and structure teaching-learning evidence for faculty appraisal"
    version = "1.0"
    allowed_tools = ["read_csv", "read_file", "get_evidence", "calculate_average"]

    def execute(self, task_input: Dict[str, Any], tool_registry, memory, **kwargs) -> Dict[str, Any]:
        faculty_id = task_input.get("faculty_id")
        if not faculty_id:
            raise ValueError("faculty_id is required for teaching_appraisal")

        tool_calls_trace = []

        # Read CSV files
        courses_res = tool_registry.execute("read_csv", self.allowed_tools, file_path="teaching/courses.csv", faculty_id=faculty_id)
        tool_calls_trace.append(courses_res)
        courses = courses_res.get("result", {}).get("rows", [])

        att_res = tool_registry.execute("read_csv", self.allowed_tools, file_path="teaching/attendance.csv", faculty_id=faculty_id)
        tool_calls_trace.append(att_res)
        attendance_rows = att_res.get("result", {}).get("rows", [])

        fb_res = tool_registry.execute("read_csv", self.allowed_tools, file_path="teaching/feedback.csv", faculty_id=faculty_id)
        tool_calls_trace.append(fb_res)
        feedback_rows = fb_res.get("result", {}).get("rows", [])

        res_res = tool_registry.execute("read_csv", self.allowed_tools, file_path="teaching/results.csv", faculty_id=faculty_id)
        tool_calls_trace.append(res_res)
        results_rows = res_res.get("result", {}).get("rows", [])

        # Calculate metrics using calculation tool
        att_vals = [float(r["attendance_pct"]) for r in attendance_rows if "attendance_pct" in r]
        avg_att_calc = tool_registry.execute("calculate_average", self.allowed_tools, values=att_vals)
        tool_calls_trace.append(avg_att_calc)
        avg_att = avg_att_calc.get("result", {}).get("average", 0.0)

        fb_vals = [float(r["avg_rating"]) for r in feedback_rows if "avg_rating" in r]
        avg_fb_calc = tool_registry.execute("calculate_average", self.allowed_tools, values=fb_vals)
        tool_calls_trace.append(avg_fb_calc)
        avg_fb = avg_fb_calc.get("result", {}).get("average", 0.0)

        pr_vals = [float(r["pass_rate_pct"]) for r in results_rows if "pass_rate_pct" in r]
        avg_pr_calc = tool_registry.execute("calculate_average", self.allowed_tools, values=pr_vals)
        tool_calls_trace.append(avg_pr_calc)
        avg_pr = avg_pr_calc.get("result", {}).get("average", 0.0)

        summary = {
            "courses_taught": len(courses),
            "avg_attendance_pct": avg_att,
            "avg_feedback_score": avg_fb,
            "pass_rate_pct": avg_pr,
        }

        result_data = {
            "faculty_id": faculty_id,
            "category": "teaching",
            "courses": courses,
            "attendance": attendance_rows,
            "feedback": feedback_rows,
            "results": results_rows,
            "summary": summary,
        }

        # Update scoped memory
        if memory:
            memory.set("teaching_evidence", result_data)

        return {
            "status": "success",
            "data": result_data,
            "tool_calls_trace": tool_calls_trace
        }
