"""
API Calculation Skill (Lab 3)
Calculates deterministic faculty appraisal scores using ONLY VALID evidence.
Note: "API" refers to the faculty appraisal scoring concept in the project problem statement.
"""
from typing import Dict, Any, List
import json
from app.skills.base_skill import BaseSkill


class APICalculationSkill(BaseSkill):
    name = "api_calculation"
    description = "Calculate configurable appraisal scores using validated evidence"
    version = "1.0"
    allowed_tools = [
        "calculate_score",
        "calculate_average",
        "get_validation_results",
        "save_appraisal_result",
        "get_previous_appraisal",
    ]

    def execute(self, task_input: Dict[str, Any], tool_registry, memory, **kwargs) -> Dict[str, Any]:
        faculty_id = task_input.get("faculty_id")
        run_id = task_input.get("run_id", "RUN-DEFAULT")
        academic_year = task_input.get("academic_year", "2026-27")

        if not faculty_id:
            raise ValueError("faculty_id is required for api_calculation")

        tool_calls_trace = []

        # 1. Retrieve validation results
        val_res = tool_registry.execute("get_validation_results", self.allowed_tools, faculty_id=faculty_id, run_id=run_id)
        tool_calls_trace.append(val_res)
        validations = val_res.get("result", {}).get("validations", [])

        # Filter ONLY VALID items
        valid_items = [v for v in validations if v.get("status") == "VALID"]

        # Aggregate evidence counts by category and sub_category
        res_pubs = len([v for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "publication"])
        res_confs = len([v for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "conference"])
        res_pats = len([v for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "patent"])
        res_projs = len([v for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "project"])

        research_input = {
            "publications": res_pubs,
            "conference_papers": res_confs,
            "patents": res_pats,
            "projects": res_projs,
        }

        # Calculate Research Score
        calc_res = tool_registry.execute("calculate_score", self.allowed_tools, category="research", evidence_data=research_input)
        tool_calls_trace.append(calc_res)
        research_score_data = calc_res.get("result", {})
        research_score = research_score_data.get("score", 0.0)

        # Enrich research breakdown with itemized publication & paper records
        valid_journals = [
            {
                "title": v.get("title"),
                "journal": v.get("description", "Refereed Journal"),
                "year": v.get("year") or 2026,
                "points_earned": 3.0,
                "status": "VALID",
            }
            for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "publication"
        ]
        valid_confs = [
            {
                "title": v.get("title"),
                "venue": v.get("description", "International Conference"),
                "year": v.get("year") or 2026,
                "points_earned": 4.0,
                "status": "VALID",
            }
            for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "conference"
        ]
        valid_patents = [
            {
                "title": v.get("title"),
                "grant_id": v.get("description", "Patent Specification"),
                "points_earned": 7.0,
                "status": "VALID",
            }
            for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "patent"
        ]
        valid_projects = [
            {
                "title": v.get("title"),
                "sponsorship": v.get("description", "Sponsored Research Grant"),
                "points_earned": 5.0,
                "status": "VALID",
            }
            for v in valid_items if v.get("category") == "research" and v.get("sub_category") == "project"
        ]

        research_score_data["itemized"] = {
            "journals": valid_journals,
            "conferences": valid_confs,
            "patents": valid_patents,
            "projects": valid_projects,
        }
        research_score_data["summary_counts"] = {
            "total_papers": len(valid_journals) + len(valid_confs),
            "journal_publications": len(valid_journals),
            "conference_proceedings": len(valid_confs),
            "patents_granted": len(valid_patents),
            "sponsored_projects": len(valid_projects),
        }

        # Retrieve teaching data from scoped memory or fallback defaults
        teaching_mem = memory.get("teaching_evidence") if memory else None
        teaching_summary = teaching_mem.get("summary", {}) if teaching_mem else {
            "courses_taught": 3,
            "avg_attendance_pct": 91.0,
            "avg_feedback_score": 4.3,
            "pass_rate_pct": 88.3,
        }

        # Calculate Teaching Score
        calc_teach = tool_registry.execute("calculate_score", self.allowed_tools, category="teaching", evidence_data=teaching_summary)
        tool_calls_trace.append(calc_teach)
        teaching_score_data = calc_teach.get("result", {})
        teaching_score_data["summary"] = teaching_summary
        teaching_score = teaching_score_data.get("score", 0.0)

        # Aggregate administration counts
        adm_comms = len([v for v in valid_items if v.get("category") == "administration" and v.get("sub_category") == "committee"])
        adm_roles = len([v for v in valid_items if v.get("category") == "administration" and v.get("sub_category") == "coordinator_role"])
        adm_acts = len([v for v in valid_items if v.get("category") == "administration" and v.get("sub_category") == "activity"])

        admin_input = {
            "committee_memberships": adm_comms,
            "coordinator_roles": adm_roles,
            "institutional_activities": adm_acts,
        }

        # Calculate Administration Score
        calc_adm = tool_registry.execute("calculate_score", self.allowed_tools, category="administration", evidence_data=admin_input)
        tool_calls_trace.append(calc_adm)
        admin_score_data = calc_adm.get("result", {})
        admin_score_data["itemized"] = {
            "committees": [
                {"title": v.get("title"), "role": v.get("description", "Member"), "points_earned": 4.0, "status": "VALID"}
                for v in valid_items if v.get("category") == "administration" and v.get("sub_category") == "committee"
            ],
            "coordinator_roles": [
                {"title": v.get("title"), "scope": v.get("description", "Coordinator"), "points_earned": 6.0, "status": "VALID"}
                for v in valid_items if v.get("category") == "administration" and v.get("sub_category") == "coordinator_role"
            ],
            "activities": [
                {"title": v.get("title"), "details": v.get("description", "Organizer"), "points_earned": 2.0, "status": "VALID"}
                for v in valid_items if v.get("category") == "administration" and v.get("sub_category") == "activity"
            ],
        }
        admin_score_data["summary_counts"] = {
            "committee_count": len(admin_score_data["itemized"]["committees"]),
            "coordinator_count": len(admin_score_data["itemized"]["coordinator_roles"]),
            "activity_count": len(admin_score_data["itemized"]["activities"]),
            "total_admin_engagements": len(admin_score_data["itemized"]["committees"]) + len(admin_score_data["itemized"]["coordinator_roles"]) + len(admin_score_data["itemized"]["activities"]),
        }
        admin_score = admin_score_data.get("score", 0.0)

        total_score = round(research_score + teaching_score + admin_score, 2)

        breakdown = {
            "research": research_score_data,
            "teaching": teaching_score_data,
            "administration": admin_score_data,
            "total_score": total_score,
            "max_score": 100.0,
            "policy_label": "Demo Appraisal Policy — configurable; not official institutional scoring policy.",
        }

        # Save Appraisal Result to DB
        save_res = tool_registry.execute(
            "save_appraisal_result",
            self.allowed_tools,
            faculty_id=faculty_id,
            run_id=run_id,
            academic_year=academic_year,
            research_score=research_score,
            teaching_score=teaching_score,
            administration_score=admin_score,
            total_score=total_score,
            score_breakdown=breakdown,
        )
        tool_calls_trace.append(save_res)

        # Check previous appraisal comparison
        prev_app = tool_registry.execute("get_previous_appraisal", self.allowed_tools, faculty_id=faculty_id)
        tool_calls_trace.append(prev_app)

        result_data = {
            "faculty_id": faculty_id,
            "run_id": run_id,
            "academic_year": academic_year,
            "scores": {
                "research": research_score,
                "teaching": teaching_score,
                "administration": admin_score,
                "total": total_score,
                "max": 100.0,
            },
            "breakdown": breakdown,
            "previous_appraisal": prev_app.get("result", {}).get("data"),
        }

        # Save in scoped memory
        if memory:
            memory.set("current_appraisal_result", result_data)

        return {
            "status": "success",
            "data": result_data,
            "tool_calls_trace": tool_calls_trace,
        }
