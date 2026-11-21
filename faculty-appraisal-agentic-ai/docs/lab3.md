# Lab 3: Skill Creation & Skill Registry

## 1. What is a Skill?

In an Agentic AI architecture, a **Skill** is a reusable, self-contained capability package that combines:
1. A specification document (`SKILL.md`) describing inputs, outputs, constraints, and error handling.
2. An executable implementation (`skill.py`) adhering to `BaseSkill`.
3. An explicit declaration of `allowed_tools`.

A **Tool** is a low-level primitive (e.g. `read_csv`, `calculate_average`), whereas a **Skill** is higher-level workflow logic coordinating tools to achieve an operational milestone.

---

## 2. Six Registered Skills

| Skill | SKILL.md Path | Allowed Tools | Purpose |
|---|---|---|---|
| `research_appraisal` | `app/skills/research_appraisal/SKILL.md` | `read_csv`, `read_pdf`, `read_file`, `get_evidence` | Gathers research publications, patents, projects |
| `teaching_appraisal` | `app/skills/teaching_appraisal/SKILL.md` | `read_csv`, `read_file`, `get_evidence`, `calculate_average` | Gathers courses, attendance, feedback ratings |
| `administration_appraisal` | `app/skills/administration_appraisal/SKILL.md` | `read_csv`, `read_file`, `get_evidence` | Gathers committees, roles, institutional events |
| `evidence_validation` | `app/skills/evidence_validation/SKILL.md` | `read_file`, `read_pdf`, `get_evidence`, `save_validation_result` | Validates completeness, files, duplicates |
| `api_calculation` | `app/skills/api_calculation/SKILL.md` | `calculate_score`, `calculate_average`, `get_validation_results`, `save_appraisal_result`, `get_previous_appraisal` | Deterministically calculates scores on VALID items |
| `report_generation` | `app/skills/report_generation/SKILL.md` | `query_faculty_data`, `get_validation_results`, `get_previous_appraisal`, `generate_pdf`, `generate_json` | Compiles PDF & JSON draft reports |

---

## 3. Dynamic Skill Registry (`SKILL_REGISTRY`)

The runtime does **not** use an `if/elif` block to route tasks. Instead, it relies on `SkillRegistry`:

```python
class SkillRegistry:
    def __init__(self):
        self._skills = {}
        # Self-register default domain skills
        self.register(ResearchAppraisalSkill)
        self.register(TeachingAppraisalSkill)
        self.register(AdministrationAppraisalSkill)
        self.register(EvidenceValidationSkill)
        self.register(APICalculationSkill)
        self.register(ReportGenerationSkill)

    def register(self, skill_cls: Type[BaseSkill]):
        self._skills[skill_cls.name] = skill_cls
```

### Adding a New Skill Without Code Rewrite
To add a new capability (e.g., `PatentAnalysisSkill`), a developer simply subclasses `BaseSkill` and registers it:
```python
registry.register(PatentAnalysisSkill)
# The runtime can now execute tasks requiring PatentAnalysisSkill immediately!
```
No modifications to `AgentRuntime.run_task` or core routing are ever required.
