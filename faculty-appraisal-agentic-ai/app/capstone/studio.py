"""
Capstone Project Studio (Lab 14 / Capstone System)
Full team-owned agentic system bringing together all 14 labs:
1. Multi-Faculty Batch Orchestration Engine
2. Institutional Executive Decision Support (Rankings, Tenure, Accreditations)
3. NBA / NAAC Tier-1 Readiness Scoring
4. Comprehensive University Audit Dossier Generation
"""
import time
import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

from app.database.database import execute_query, execute_write
from app.agents.coordinator import AppraisalCoordinator
from app.discipline.discipline_agents import DisciplineAppraisalCoordinator
from app.swarm.swarm import AppraisalSwarm
from app.governance.responsible_autonomy import ResponsibleAutonomyEngine


@dataclass
class FacultyTenureVerdict:
    faculty_id: str
    name: str
    department: str
    designation: str
    total_score: float
    discipline_score: float
    tenure_tier: str
    promotion_eligible: bool
    fdp_intervention_required: bool
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InstitutionalAccreditationReport:
    academic_year: str
    timestamp: float
    total_faculty_evaluated: int
    university_mean_score: float
    department_rankings: List[Dict[str, Any]]
    nba_tier1_readiness_score: float
    accreditation_grade: str  # TIER-1 ACCREDITED (5 YEARS), PROVISIONAL (2 YEARS), NON-COMPLIANT
    promotion_eligible_count: int
    fdp_intervention_count: int
    faculty_verdicts: List[FacultyTenureVerdict]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["faculty_verdicts"] = [v.to_dict() if hasattr(v, "to_dict") else v for v in self.faculty_verdicts]
        return d


class CapstoneProjectStudio:
    """
    Capstone Multi-Agent Studio Engine.
    Executes university-scale evaluation across all faculty departments,
    synthesizing executive insights and accreditation readiness.
    """
    def __init__(self):
        self.coordinator = AppraisalCoordinator()
        self.discipline_coord = DisciplineAppraisalCoordinator()
        self.swarm = AppraisalSwarm()
        self.governance = ResponsibleAutonomyEngine()

    def run_institutional_studio(self, academic_year: str = "2026-27") -> InstitutionalAccreditationReport:
        start_time = time.time()

        # 1. Fetch all registered faculty members
        faculty_rows = execute_query("SELECT * FROM faculty ORDER BY faculty_id ASC")
        if not faculty_rows:
            faculty_rows = [
                {
                    "faculty_id": "FAC001",
                    "name": "Dr. Ananya Rao",
                    "department": "Computer Science and AI",
                    "designation": "Associate Professor",
                    "academic_year": academic_year,
                }
            ]

        verdicts: List[FacultyTenureVerdict] = []
        dept_scores: Dict[str, List[float]] = {}

        # 2. Execute full agentic lifecycle across each faculty
        for fac in faculty_rows:
            fid = fac["faculty_id"]
            pipe_res = self.coordinator.run_appraisal_pipeline(fid, academic_year)
            disc_res = self.discipline_coord.evaluate_faculty(fac, pipe_res)

            standard_score = pipe_res.get("calculation", {}).get("scores", {}).get("total", 0.0)
            discipline_total = disc_res.get("adjusted_scores", {}).get("total", standard_score)

            # Record for department aggregation
            dept = fac.get("department", "General")
            dept_scores.setdefault(dept, []).append(discipline_total)

            # Classify Tenure & Promotion Tier
            if discipline_total >= 85.0:
                tier = "PROMOTION_ELIGIBLE"
                promo = True
                fdp = False
                rationale = f"Exemplary research density and teaching excellence (Score: {discipline_total}/100). Clears promotion threshold."
            elif discipline_total >= 75.0:
                tier = "MERIT_INCREMENT"
                promo = False
                fdp = False
                rationale = f"High performance across pedagogical and institutional service domains (Score: {discipline_total}/100)."
            elif discipline_total >= 65.0:
                tier = "TENURE_TRACK_SATISFACTORY"
                promo = False
                fdp = False
                rationale = f"Satisfactory standard renewal (Score: {discipline_total}/100). Recommended to increase indexed publications."
            else:
                tier = "FDP_INTERVENTION_REQUIRED"
                promo = False
                fdp = True
                rationale = f"Underperformance detected in research/teaching evidence (Score: {discipline_total}/100). Mandatory mentoring assigned."

            verdict = FacultyTenureVerdict(
                faculty_id=fid,
                name=fac.get("name", "Faculty Member"),
                department=dept,
                designation=fac.get("designation", "Assistant Professor"),
                total_score=standard_score,
                discipline_score=discipline_total,
                tenure_tier=tier,
                promotion_eligible=promo,
                fdp_intervention_required=fdp,
                rationale=rationale,
            )
            verdicts.append(verdict)

            # Cryptographically sign appraisal outcome in audit chain (Lab 12 integration)
            self.governance.append_audit_block(
                "CAPSTONE_STUDIO_APPRAISAL_VERDICT",
                pipe_res.get("run_id", f"RUN-{fid}"),
                verdict.to_dict(),
            )

        # 3. Compute Institutional Statistics
        all_disc_scores = [v.discipline_score for v in verdicts]
        mean_score = round(sum(all_disc_scores) / max(1, len(all_disc_scores)), 2)

        # Department Rankings
        rankings = []
        for d, s_list in dept_scores.items():
            d_mean = round(sum(s_list) / len(s_list), 2)
            rankings.append({
                "department": d,
                "faculty_count": len(s_list),
                "mean_score": d_mean,
            })
        rankings.sort(key=lambda r: r["mean_score"], reverse=True)
        for i, r in enumerate(rankings):
            r["rank"] = i + 1

        # NBA Tier-1 Readiness Index (0-100 score)
        # Factors: Mean score (60%), Promotion density (25%), FDP penalty (15%)
        promo_count = sum(1 for v in verdicts if v.promotion_eligible)
        fdp_count = sum(1 for v in verdicts if v.fdp_intervention_required)
        promo_ratio = promo_count / max(1, len(verdicts))
        fdp_ratio = fdp_count / max(1, len(verdicts))

        nba_readiness = round(
            min(100.0, max(40.0, (mean_score * 0.70) + (promo_ratio * 30.0) - (fdp_ratio * 20.0))),
            1,
        )

        if nba_readiness >= 80.0:
            accreditation_grade = "TIER-1 ACCREDITED (5 YEARS VALIDITY)"
        elif nba_readiness >= 65.0:
            accreditation_grade = "PROVISIONAL ACCREDITATION (2 YEARS VALIDITY)"
        else:
            accreditation_grade = "ACCREDITATION DEFERRED / ACTION PLAN REQUIRED"

        report = InstitutionalAccreditationReport(
            academic_year=academic_year,
            timestamp=start_time,
            total_faculty_evaluated=len(verdicts),
            university_mean_score=mean_score,
            department_rankings=rankings,
            nba_tier1_readiness_score=nba_readiness,
            accreditation_grade=accreditation_grade,
            promotion_eligible_count=promo_count,
            fdp_intervention_count=fdp_count,
            faculty_verdicts=verdicts,
        )

        return report
