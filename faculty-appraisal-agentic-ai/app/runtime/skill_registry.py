"""
Skill Registry (Lab 3 & Lab 6)
Extensible registry for skills in the OpenCLA/OpenClaw-style runtime.
Adding a new skill requires registering it here, WITHOUT modifying the runtime core.
"""
from typing import Dict, Type, List, Optional, Any
from app.skills.base_skill import BaseSkill
from app.skills.research_appraisal.skill import ResearchAppraisalSkill
from app.skills.teaching_appraisal.skill import TeachingAppraisalSkill
from app.skills.administration_appraisal.skill import AdministrationAppraisalSkill
from app.skills.evidence_validation.skill import EvidenceValidationSkill
from app.skills.api_calculation.skill import APICalculationSkill
from app.skills.report_generation.skill import ReportGenerationSkill


class SkillRegistry:
    """Registry managing modular skills."""

    def __init__(self):
        self._skills: Dict[str, Type[BaseSkill]] = {}
        self._register_default_skills()

    def _register_default_skills(self):
        """Register the six core domain skills for faculty appraisal."""
        default_skills = [
            ResearchAppraisalSkill,
            TeachingAppraisalSkill,
            AdministrationAppraisalSkill,
            EvidenceValidationSkill,
            APICalculationSkill,
            ReportGenerationSkill,
        ]
        for skill_cls in default_skills:
            self.register(skill_cls)

    def register(self, skill_cls: Type[BaseSkill]) -> None:
        """
        Register a new skill with the registry.
        Enables runtime extensibility without code modifications to the runtime core.
        """
        if not issubclass(skill_cls, BaseSkill):
            raise TypeError(f"Skill {skill_cls} must subclass BaseSkill")
        self._skills[skill_cls.name] = skill_cls

    def unregister(self, skill_name: str) -> None:
        """Remove a skill from the registry."""
        if skill_name in self._skills:
            del self._skills[skill_name]

    def get(self, skill_name: str) -> Optional[Type[BaseSkill]]:
        """Get skill class by name."""
        return self._skills.get(skill_name)

    def list_skills(self) -> List[Dict[str, Any]]:
        """List all registered skills and their metadata."""
        return [
            {
                "name": name,
                "description": cls.description,
                "version": cls.version,
                "allowed_tools": cls.allowed_tools,
            }
            for name, cls in self._skills.items()
        ]

    def select_skill(self, task: str) -> Optional[str]:
        """
        Select matching skill based on task name or keyword intent.
        No hard-coded application logic is used here; matches registered skill names
        or keywords defined in skill metadata.
        """
        normalized_task = task.lower().strip()

        # 1. Exact or partial match with registered skill name
        for name in self._skills.keys():
            if name in normalized_task or normalized_task in name:
                return name

        # 2. Match against skill metadata descriptions
        for name, cls in self._skills.items():
            keywords = name.split("_")
            if any(kw in normalized_task for kw in keywords if len(kw) > 3):
                return name

        return None
