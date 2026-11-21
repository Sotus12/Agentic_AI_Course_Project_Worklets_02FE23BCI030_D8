"""
Report Generation Skill (Lab 3)
Retrieves profile, validated evidence, and scores to generate PDF and JSON reports.
"""
from typing import Dict, Any, List
from app.skills.base_skill import BaseSkill


class ReportGenerationSkill(BaseSkill):
    name = "report_generation"
    description = "Generate PDF and JSON appraisal reports from scored evidence"
    version = "1.0"
    allowed_tools = [
        "query_faculty_data",
        "get_validation_results",
        "get_previous_appraisal",
        "generate_pdf",
        "generate_json",
    ]

    def execute(self, task_input: Dict[str, Any], tool_registry, memory, **kwargs) -> Dict[str, Any]:
        faculty_id = task_input.get("faculty_id")
        run_id = task_input.get("run_id", "RUN-DEFAULT")

        if not faculty_id:
            raise ValueError("faculty_id is required for report_generation")

        tool_calls_trace = []

        # 1. Faculty profile
        prof_res = tool_registry.execute("query_faculty_data", self.allowed_tools, faculty_id=faculty_id)
        tool_calls_trace.append(prof_res)
        faculty_profile = prof_res.get("result", {}).get("data", {})

        # 2. Validation results & summary
        val_res = tool_registry.execute("get_validation_results", self.allowed_tools, faculty_id=faculty_id, run_id=run_id)
        tool_calls_trace.append(val_res)
        validations = val_res.get("result", {}).get("validations", [])

        val_summary = {
            "VALID": len([v for v in validations if v.get("status") == "VALID"]),
            "INVALID": len([v for v in validations if v.get("status") == "INVALID"]),
            "NEEDS_REVIEW": len([v for v in validations if v.get("status") == "NEEDS_REVIEW"]),
        }

        # 3. Retrieve scores from memory or previous tool execution
        appraisal_state = memory.get("current_appraisal_result") if memory else None
        scores_data = appraisal_state.get("scores", {}) if appraisal_state else {}
        breakdown_data = appraisal_state.get("breakdown", {}) if appraisal_state else {}

        # 4. Warnings for unvalidated or review items
        warnings = []
        for v in validations:
            if v.get("status") == "NEEDS_REVIEW":
                warnings.append(f"[NEEDS REVIEW] {v.get('title')}: {v.get('reason')}")
            elif v.get("status") == "INVALID":
                warnings.append(f"[INVALID] {v.get('title')}: {v.get('reason')}")

        # 5. Previous appraisal comparison
        prev_res = tool_registry.execute("get_previous_appraisal", self.allowed_tools, faculty_id=faculty_id)
        tool_calls_trace.append(prev_res)
        prev_data = prev_res.get("result", {}).get("data")

        comparison = {}
        if prev_data:
            prev_score = prev_data.get("total_score", 0.0)
            curr_score = scores_data.get("total", 0.0)
            comparison = {
                "previous_year": prev_data.get("academic_year"),
                "previous_score": prev_score,
                "current_score": curr_score,
                "difference": round(curr_score - prev_score, 2),
            }

        # Structure payload for report generators
        report_payload = {
            "faculty": faculty_profile,
            "scores": {
                "research": {"score": scores_data.get("research", 0.0), "max_score": 40},
                "teaching": {"score": scores_data.get("teaching", 0.0), "max_score": 40},
                "administration": {"score": scores_data.get("administration", 0.0), "max_score": 20},
                "total_score": scores_data.get("total", 0.0),
                "max_score": 100.0,
            },
            "validation_summary": val_summary,
            "warnings": warnings,
            "comparison": comparison,
            "detailed_breakdown": breakdown_data,
        }

        # Generate JSON Report
        json_gen = tool_registry.execute(
            "generate_json",
            self.allowed_tools,
            report_data=report_payload,
            faculty_id=faculty_id,
            run_id=run_id,
        )
        tool_calls_trace.append(json_gen)

        # Generate PDF Report
        pdf_gen = tool_registry.execute(
            "generate_pdf",
            self.allowed_tools,
            report_data=report_payload,
            faculty_id=faculty_id,
            run_id=run_id,
        )
        tool_calls_trace.append(pdf_gen)

        result_data = {
            "faculty_id": faculty_id,
            "run_id": run_id,
            "status": "DRAFT",
            "json_path": json_gen.get("result", {}).get("path"),
            "pdf_path": pdf_gen.get("result", {}).get("path"),
            "warnings_count": len(warnings),
        }

        if memory:
            memory.set("report_generation", result_data)

        return {
            "status": "success",
            "data": result_data,
            "tool_calls_trace": tool_calls_trace,
        }
