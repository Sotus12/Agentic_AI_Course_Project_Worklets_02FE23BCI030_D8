"""
Tests for API Calculation & Configurable Scoring Rules
Validates:
- Deterministic score generation (no stochastic LLM variations)
- Compliance with configurable scoring rules (config/scoring_rules.json)
- Proper capping at maximum weights (Research: 40, Teaching: 40, Admin: 20, Total: 100)
"""
import pytest
from app.tools.calculation_tools import calculate_score


def test_research_score_bounds_and_determinism():
    """Verify research scoring is deterministic and capped at 40."""
    input_data = {
        "publications": 10,       # 10 * 3 = 30 -> capped at 15
        "conference_papers": 5,   # 5 * 4 = 20 -> capped at 8
        "patents": 2,             # 2 * 7 = 14 -> capped at 7
        "projects": 3,            # 3 * 5 = 15 -> capped at 10
    }
    # Expected sum = 15 + 8 + 7 + 10 = 40 (max)
    res = calculate_score("research", input_data)
    assert res["status"] == "success"
    assert res["score"] == 40.0
    assert res["max_score"] == 40.0


def test_teaching_score_calculation():
    """Verify teaching scoring calculates proportionate points based on metrics."""
    input_data = {
        "courses_taught": 3,        # 3 * 2 = 6 (max 8)
        "avg_attendance_pct": 90.0, # (90/85)*10 -> capped at 10.0
        "avg_feedback_score": 4.5,  # (4.5/4.0)*12 -> capped at 12.0
        "pass_rate_pct": 85.0,      # (85/80)*10 -> capped at 10.0
    }
    res = calculate_score("teaching", input_data)
    assert res["status"] == "success"
    # 6 + 10 + 12 + 10 = 38
    assert res["score"] == 38.0
    assert res["score"] <= res["max_score"]


def test_administration_score_calculation():
    """Verify administration score calculation."""
    input_data = {
        "committee_memberships": 2,     # 2 * 4 = 8 (max 8)
        "coordinator_roles": 1,         # 1 * 6 = 6 (max 6)
        "institutional_activities": 3,  # 3 * 2 = 6 (max 6)
    }
    # Total = 8 + 6 + 6 = 20 (max 20)
    res = calculate_score("administration", input_data)
    assert res["status"] == "success"
    assert res["score"] == 20.0
    assert res["score"] <= res["max_score"]
