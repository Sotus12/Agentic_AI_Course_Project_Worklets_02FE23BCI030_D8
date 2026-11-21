"""
Unit and Integration Tests for Lab 13 and Lab 14
- Lab 13: Discipline-Specific Agents (CS, ME, CE, EE worklets & NBA mappings)
- Lab 14: Capstone Project Studio (Full team-owned agentic system)
"""
import pytest
from app.discipline.discipline_agents import (
    DisciplineAppraisalCoordinator,
    ComputerScienceAppraisalAgent,
    MechanicalAppraisalAgent,
    CivilAppraisalAgent,
    ElectricalAppraisalAgent,
)
from app.capstone.studio import CapstoneProjectStudio
from app.agents.coordinator import AppraisalCoordinator


def test_discipline_detection_and_routing():
    dac = DisciplineAppraisalCoordinator()
    assert dac.detect_discipline("Computer Science and AI") == "CS"
    assert dac.detect_discipline("Department of Mechanical Engineering") == "ME"
    assert dac.detect_discipline("Civil & Structural Engineering") == "CE"
    assert dac.detect_discipline("Electronics and Communication Engineering") == "EE"


def test_discipline_specific_evaluation():
    dac = DisciplineAppraisalCoordinator()
    coord = AppraisalCoordinator()
    pipe = coord.run_appraisal_pipeline("FAC001")

    # Evaluate with CS agent
    cs_profile = {"faculty_id": "FAC001", "name": "Dr. Ananya Rao", "department": "Computer Science and AI"}
    cs_eval = dac.evaluate_faculty(cs_profile, pipe)

    assert cs_eval["discipline_code"] == "CS"
    assert "NBA 5.3" in cs_eval["nba_criterion"]
    assert cs_eval["discipline_bonus_applied"] > 0
    assert cs_eval["adjusted_scores"]["total"] > 0
    assert cs_eval["nba_compliance_status"] in ("EXEMPLARY", "SATISFACTORY")


def test_mechanical_discipline_worklet():
    dac = DisciplineAppraisalCoordinator()
    coord = AppraisalCoordinator()
    pipe = coord.run_appraisal_pipeline("FAC003")

    me_profile = {"faculty_id": "FAC003", "name": "Dr. Sneha Patil", "department": "Mechanical & Robotics"}
    me_eval = dac.evaluate_faculty(me_profile, pipe)

    assert me_eval["discipline_code"] == "ME"
    assert "NBA 5.4" in me_eval["nba_criterion"]
    assert me_eval["discipline_bonus_applied"] > 0


def test_capstone_project_studio_end_to_end():
    studio = CapstoneProjectStudio()
    report = studio.run_institutional_studio("2026-27")

    assert report.total_faculty_evaluated >= 3
    assert report.university_mean_score > 0
    assert len(report.department_rankings) >= 2
    assert report.nba_tier1_readiness_score > 0
    assert report.accreditation_grade in (
        "TIER-1 ACCREDITED (5 YEARS VALIDITY)",
        "PROVISIONAL ACCREDITATION (2 YEARS VALIDITY)",
        "ACCREDITATION DEFERRED / ACTION PLAN REQUIRED",
    )
    assert len(report.faculty_verdicts) >= 3

    # Check that tenure verdicts were generated
    for v in report.faculty_verdicts:
        assert v.tenure_tier in (
            "PROMOTION_ELIGIBLE",
            "MERIT_INCREMENT",
            "TENURE_TRACK_SATISFACTORY",
            "FDP_INTERVENTION_REQUIRED",
        )
