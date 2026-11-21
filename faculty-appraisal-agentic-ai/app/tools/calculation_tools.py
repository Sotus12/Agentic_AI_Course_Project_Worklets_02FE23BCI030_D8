"""
Calculation tools — calculate_average, calculate_score.
Deterministic scoring — no LLM-based score generation.
"""
import os
import json


def _load_scoring_rules() -> dict:
    """Load configurable scoring rules from config/scoring_rules.json."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "config", "scoring_rules.json"
    )
    with open(config_path, "r") as f:
        return json.load(f)


def calculate_average(values: list) -> dict:
    """Calculate average of a list of numeric values."""
    try:
        if not values:
            return {"status": "success", "average": 0.0, "count": 0}
        numeric = [float(v) for v in values if v is not None]
        avg = sum(numeric) / len(numeric) if numeric else 0.0
        return {"status": "success", "average": round(avg, 2), "count": len(numeric)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def calculate_score(category: str, evidence_data: dict) -> dict:
    """
    Calculate deterministic score for a category using configurable rules.

    Args:
        category: 'research', 'teaching', or 'administration'
        evidence_data: structured evidence counts/values for the category

    Returns: score breakdown dict
    """
    try:
        rules = _load_scoring_rules()
        if category not in rules:
            return {"status": "error", "error": f"Unknown category: {category}"}

        cat_rules = rules[category]
        criteria = cat_rules["criteria"]
        max_score = cat_rules["max_score"]
        score = 0.0
        details = {}

        if category == "research":
            # Publications
            pub_count = evidence_data.get("publications", 0)
            pub_points = min(pub_count * criteria["publications"]["points_per_item"],
                            criteria["publications"]["max"])
            details["publications"] = {"count": pub_count, "points": pub_points,
                                       "max": criteria["publications"]["max"]}
            score += pub_points

            # Conference papers
            conf_count = evidence_data.get("conference_papers", 0)
            conf_points = min(conf_count * criteria["conference_papers"]["points_per_item"],
                             criteria["conference_papers"]["max"])
            details["conference_papers"] = {"count": conf_count, "points": conf_points,
                                            "max": criteria["conference_papers"]["max"]}
            score += conf_points

            # Patents
            pat_count = evidence_data.get("patents", 0)
            pat_points = min(pat_count * criteria["patents"]["points_per_item"],
                            criteria["patents"]["max"])
            details["patents"] = {"count": pat_count, "points": pat_points,
                                  "max": criteria["patents"]["max"]}
            score += pat_points

            # Projects
            proj_count = evidence_data.get("projects", 0)
            proj_points = min(proj_count * criteria["projects"]["points_per_item"],
                             criteria["projects"]["max"])
            details["projects"] = {"count": proj_count, "points": proj_points,
                                   "max": criteria["projects"]["max"]}
            score += proj_points

        elif category == "teaching":
            # Courses taught
            course_count = evidence_data.get("courses_taught", 0)
            course_points = min(course_count * criteria["courses_taught"]["points_per_course"],
                               criteria["courses_taught"]["max"])
            details["courses_taught"] = {"count": course_count, "points": course_points,
                                         "max": criteria["courses_taught"]["max"]}
            score += course_points

            # Average attendance
            att_pct = evidence_data.get("avg_attendance_pct", 0)
            att_threshold = criteria["avg_attendance_pct"]["full_marks_threshold"]
            att_max = criteria["avg_attendance_pct"]["max"]
            att_points = min((att_pct / att_threshold) * att_max, att_max) if att_threshold > 0 else 0
            att_points = round(att_points, 2)
            details["avg_attendance_pct"] = {"value": att_pct, "points": att_points,
                                             "max": att_max, "threshold": att_threshold}
            score += att_points

            # Average feedback
            fb_score = evidence_data.get("avg_feedback_score", 0)
            fb_threshold = criteria["avg_feedback_score"]["full_marks_threshold"]
            fb_max = criteria["avg_feedback_score"]["max"]
            fb_scale = criteria["avg_feedback_score"]["scale"]
            fb_points = min((fb_score / fb_threshold) * fb_max, fb_max) if fb_threshold > 0 else 0
            fb_points = round(fb_points, 2)
            details["avg_feedback_score"] = {"value": fb_score, "points": fb_points,
                                             "max": fb_max, "threshold": fb_threshold}
            score += fb_points

            # Pass rate
            pr_pct = evidence_data.get("pass_rate_pct", 0)
            pr_threshold = criteria["pass_rate_pct"]["full_marks_threshold"]
            pr_max = criteria["pass_rate_pct"]["max"]
            pr_points = min((pr_pct / pr_threshold) * pr_max, pr_max) if pr_threshold > 0 else 0
            pr_points = round(pr_points, 2)
            details["pass_rate_pct"] = {"value": pr_pct, "points": pr_points,
                                        "max": pr_max, "threshold": pr_threshold}
            score += pr_points

        elif category == "administration":
            # Committees
            com_count = evidence_data.get("committee_memberships", 0)
            com_points = min(com_count * criteria["committee_memberships"]["points_per_item"],
                            criteria["committee_memberships"]["max"])
            details["committee_memberships"] = {"count": com_count, "points": com_points,
                                                "max": criteria["committee_memberships"]["max"]}
            score += com_points

            # Coordinator roles
            role_count = evidence_data.get("coordinator_roles", 0)
            role_points = min(role_count * criteria["coordinator_roles"]["points_per_item"],
                             criteria["coordinator_roles"]["max"])
            details["coordinator_roles"] = {"count": role_count, "points": role_points,
                                            "max": criteria["coordinator_roles"]["max"]}
            score += role_points

            # Activities
            act_count = evidence_data.get("institutional_activities", 0)
            act_points = min(act_count * criteria["institutional_activities"]["points_per_item"],
                            criteria["institutional_activities"]["max"])
            details["institutional_activities"] = {"count": act_count, "points": act_points,
                                                   "max": criteria["institutional_activities"]["max"]}
            score += act_points

        score = min(round(score, 2), max_score)

        return {
            "status": "success",
            "category": category,
            "score": score,
            "max_score": max_score,
            "details": details,
            "note": "DEMO scoring policy — configurable; not official institutional scoring policy."
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# Tool registry entry
TOOLS = {
    "calculate_average": {
        "function": calculate_average,
        "description": "Calculate average of numeric values",
        "inputs": ["values"],
    },
    "calculate_score": {
        "function": calculate_score,
        "description": "Calculate deterministic appraisal score for a category using configurable rules",
        "inputs": ["category", "evidence_data"],
    },
}
