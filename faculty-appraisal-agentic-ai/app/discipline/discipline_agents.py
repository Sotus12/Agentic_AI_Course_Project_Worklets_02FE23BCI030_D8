"""
Discipline-Specific Appraisal Agents (Lab 13)
Tailored appraisal logic for engineering disciplines:
- Computer Science & AI (CS)
- Mechanical & Robotics Engineering (ME)
- Civil & Infrastructure Engineering (CE)
- Electrical & Electronics Engineering (EE)

Applies discipline-specific weighting and NBA Criterion 5 compliance mapping.
"""
from typing import Dict, Any, List, Optional


class DisciplineBaseAgent:
    """Base class for engineering discipline-specific appraisal agents."""
    discipline_code = "GEN"
    discipline_name = "General Engineering"
    nba_criterion_focus = "Criterion 5: Faculty Information and Contributions"

    def evaluate(self, faculty_profile: Dict[str, Any], pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class ComputerScienceAppraisalAgent(DisciplineBaseAgent):
    """
    Computer Science & AI Domain Worklet:
    - High priority on IEEE/ACM proceedings, open-source code artifacts, and AI models
    - NBA Criterion 5.3: Modern computing software tools and algorithmic innovation
    """
    discipline_code = "CS"
    discipline_name = "Computer Science & Artificial Intelligence"
    nba_criterion_focus = "NBA 5.3: Computing Tools, AI Frameworks & Software Lab Innovation"

    def evaluate(self, faculty_profile: Dict[str, Any], pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        calc = pipeline_results.get("calculation", {})
        scores = calc.get("scores", {})
        val_summary = pipeline_results.get("validation", {}).get("summary", {})

        # CS specific indicators: software patents, AI conference papers, open repositories
        research_score = scores.get("research", 0.0)
        teaching_score = scores.get("teaching", 0.0)
        admin_score = scores.get("administration", 0.0)

        # Discipline bonus: reward high-impact conference and AI publication density
        cs_bonus = 3.0 if research_score >= 30.0 else 1.5
        adjusted_research = min(40.0, round(research_score + cs_bonus, 2))
        total = round(adjusted_research + teaching_score + admin_score, 2)

        return {
            "discipline_code": self.discipline_code,
            "discipline_name": self.discipline_name,
            "nba_criterion": self.nba_criterion_focus,
            "domain_weighting_focus": "High-tier IEEE/ACM proceedings, Open-source tool adoption, AI research",
            "discipline_bonus_applied": cs_bonus,
            "adjusted_scores": {
                "research": adjusted_research,
                "teaching": teaching_score,
                "administration": admin_score,
                "total": total,
            },
            "nba_compliance_status": "EXEMPLARY" if total >= 80 else "SATISFACTORY",
            "accreditation_notes": "Meets NBA Criterion 5.3 threshold for computing tool integration and indexed scholarship.",
        }


class MechanicalAppraisalAgent(DisciplineBaseAgent):
    """
    Mechanical & Robotics Domain Worklet:
    - Priority on physical prototyping, CAD/CAM/CAE labs, testing consultancy, fabrication
    - NBA Criterion 5.4: Workshop innovation, industrial prototyping & safety compliance
    """
    discipline_code = "ME"
    discipline_name = "Mechanical & Robotics Engineering"
    nba_criterion_focus = "NBA 5.4: Workshop Prototyping, CAD/CAM Labs & Industrial Fabrication"

    def evaluate(self, faculty_profile: Dict[str, Any], pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        calc = pipeline_results.get("calculation", {})
        scores = calc.get("scores", {})
        admin_score = scores.get("administration", 0.0)
        research_score = scores.get("research", 0.0)
        teaching_score = scores.get("teaching", 0.0)

        # ME specific indicators: lab stewardship, workshop maintenance, hardware prototypes
        me_lab_stewardship_bonus = 2.5
        adjusted_admin = min(20.0, round(admin_score + me_lab_stewardship_bonus, 2))
        total = round(research_score + teaching_score + adjusted_admin, 2)

        return {
            "discipline_code": self.discipline_code,
            "discipline_name": self.discipline_name,
            "nba_criterion": self.nba_criterion_focus,
            "domain_weighting_focus": "Hardware prototyping, CAD/CAM lab stewardship, Robotics testbeds",
            "discipline_bonus_applied": me_lab_stewardship_bonus,
            "adjusted_scores": {
                "research": research_score,
                "teaching": teaching_score,
                "administration": adjusted_admin,
                "total": total,
            },
            "nba_compliance_status": "EXEMPLARY" if total >= 75 else "SATISFACTORY",
            "accreditation_notes": "Meets NBA Criterion 5.4 requirements for fabrication lab stewardship and engineering design.",
        }


class CivilAppraisalAgent(DisciplineBaseAgent):
    """
    Civil & Infrastructure Engineering Domain Worklet:
    - Priority on structural audits, PWD/NHAI government consultancy, material testing labs
    - NBA Criterion 5.5: Technical consultancy, field projects & testing services
    """
    discipline_code = "CE"
    discipline_name = "Civil & Infrastructure Engineering"
    nba_criterion_focus = "NBA 5.5: Technical Consultancy, Material Testing & Field Projects"

    def evaluate(self, faculty_profile: Dict[str, Any], pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        calc = pipeline_results.get("calculation", {})
        scores = calc.get("scores", {})
        research_score = scores.get("research", 0.0)
        teaching_score = scores.get("teaching", 0.0)
        admin_score = scores.get("administration", 0.0)

        # CE specific indicators: consultancy revenue, geotechnical/structural audits
        ce_consultancy_bonus = 3.0
        adjusted_research = min(40.0, round(research_score + ce_consultancy_bonus, 2))
        total = round(adjusted_research + teaching_score + admin_score, 2)

        return {
            "discipline_code": self.discipline_code,
            "discipline_name": self.discipline_name,
            "nba_criterion": self.nba_criterion_focus,
            "domain_weighting_focus": "Structural health audits, PWD/government consultancy, Materials testing",
            "discipline_bonus_applied": ce_consultancy_bonus,
            "adjusted_scores": {
                "research": adjusted_research,
                "teaching": teaching_score,
                "administration": admin_score,
                "total": total,
            },
            "nba_compliance_status": "EXEMPLARY" if total >= 75 else "SATISFACTORY",
            "accreditation_notes": "Meets NBA Criterion 5.5 for field consultancy and civil infrastructure engagement.",
        }


class ElectricalAppraisalAgent(DisciplineBaseAgent):
    """
    Electrical & Electronics Domain Worklet:
    - Priority on VLSI/embedded hardware testbeds, PCB fabrication, IEEE hardware awards, IoT test rigs
    - NBA Criterion 5.6: Hardware simulation testbeds, power systems & embedded prototypes
    """
    discipline_code = "EE"
    discipline_name = "Electrical & Electronics Engineering"
    nba_criterion_focus = "NBA 5.6: Embedded Systems, VLSI/PCB Testbeds & Power Lab Infrastructure"

    def evaluate(self, faculty_profile: Dict[str, Any], pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        calc = pipeline_results.get("calculation", {})
        scores = calc.get("scores", {})
        research_score = scores.get("research", 0.0)
        teaching_score = scores.get("teaching", 0.0)
        admin_score = scores.get("administration", 0.0)

        # EE specific indicators: hardware testbeds and simulation toolkits
        ee_bonus = 2.0
        adjusted_teaching = min(40.0, round(teaching_score + ee_bonus, 2))
        total = round(research_score + adjusted_teaching + admin_score, 2)

        return {
            "discipline_code": self.discipline_code,
            "discipline_name": self.discipline_name,
            "nba_criterion": self.nba_criterion_focus,
            "domain_weighting_focus": "Embedded testbeds, IoT prototyping, VLSI design tools & hardware testing",
            "discipline_bonus_applied": ee_bonus,
            "adjusted_scores": {
                "research": research_score,
                "teaching": adjusted_teaching,
                "administration": admin_score,
                "total": total,
            },
            "nba_compliance_status": "EXEMPLARY" if total >= 80 else "SATISFACTORY",
            "accreditation_notes": "Meets NBA Criterion 5.6 for embedded hardware testbeds and laboratory design.",
        }


class DisciplineAppraisalCoordinator:
    """
    Orchestrates discipline detection and routes to the specialized discipline worklet agent.
    """
    def __init__(self):
        self.agents = {
            "CS": ComputerScienceAppraisalAgent(),
            "ME": MechanicalAppraisalAgent(),
            "CE": CivilAppraisalAgent(),
            "EE": ElectricalAppraisalAgent(),
        }

    def detect_discipline(self, department: str) -> str:
        dept_lower = (department or "").lower()
        if "computer" in dept_lower or "ai" in dept_lower or "software" in dept_lower:
            return "CS"
        elif "mechanical" in dept_lower or "robotics" in dept_lower or "automobile" in dept_lower:
            return "ME"
        elif "civil" in dept_lower or "structural" in dept_lower or "infrastructure" in dept_lower:
            return "CE"
        elif "electrical" in dept_lower or "electronic" in dept_lower or "telecom" in dept_lower:
            return "EE"
        return "CS"  # default fallback

    def evaluate_faculty(self, faculty_profile: Dict[str, Any], pipeline_results: Dict[str, Any]) -> Dict[str, Any]:
        dept = faculty_profile.get("department", "Computer Science")
        code = self.detect_discipline(dept)
        agent = self.agents.get(code, self.agents["CS"])
        return agent.evaluate(faculty_profile, pipeline_results)
