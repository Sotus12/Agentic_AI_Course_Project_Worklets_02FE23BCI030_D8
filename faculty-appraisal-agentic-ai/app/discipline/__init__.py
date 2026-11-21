"""
Discipline-Specific Agents Package (Lab 13)
Tailored appraisal agents for engineering disciplines:
- Computer Science & AI (CS)
- Mechanical & Robotics Engineering (ME)
- Civil & Structural Engineering (CE)
- Electrical & Electronics Engineering (EE)
"""
from app.discipline.discipline_agents import (
    DisciplineBaseAgent,
    ComputerScienceAppraisalAgent,
    MechanicalAppraisalAgent,
    CivilAppraisalAgent,
    ElectricalAppraisalAgent,
    DisciplineAppraisalCoordinator,
)

__all__ = [
    "DisciplineBaseAgent",
    "ComputerScienceAppraisalAgent",
    "MechanicalAppraisalAgent",
    "CivilAppraisalAgent",
    "ElectricalAppraisalAgent",
    "DisciplineAppraisalCoordinator",
]
