# Faculty Appraisal Management System (Team D8)

**Course:** Agentic AI (Course Code: `26ECAC401`)  
**Institution:** KLE Technological University, Belagavi  
**Department:** Computer Science & Engineering (Artificial Intelligence)  
**Academic Year:** 2026–27  

---

## 👥 Team Members (Team D8)

| Name | USN |
| :--- | :--- |
| **Lomesh Kumar Jangde** | `02FE23BCI032` |
| **Satyam Savarna** | `02FE23BCI030` |
| **Pratiksha Magadum** | `02FE23BCI045` |
| **Shreya Tupale** | `02FE23BCI042` |

**Under the Guidance of:** Dr. Priyanka Patil  

---

## 📂 Repository Contents

This repository hosts the complete deliverables for the Agentic AI Course Project:

1. **`faculty-appraisal-agentic-ai/`**  
   The complete production-ready source code of the Faculty Appraisal Management System implementing all 14 curriculum labs:
   - **Lab 1:** Agent vs Chatbot (Autonomous loop: Goal → Plan → Act → Observe)
   - **Lab 2:** Tool-Using Agent (Centralized `ToolRegistry` with permission gating)
   - **Lab 3:** Skill Creation (Dynamic `SkillRegistry` with reusable domain skills)
   - **Lab 4:** Memory & Retrieval (Scoped SQLite key-value context isolation)
   - **Lab 5:** MCP-Style Connector (Model Context Protocol security boundaries)
   - **Lab 6:** OpenCLA / OpenClaw Runtime (Dynamic dispatch & SQLite audit table)
   - **Lab 7:** Agentic Node Graph (State-graph workflow DAG with human checkpoint gate)
   - **Lab 8:** Parallel Swarm (Decentralized peer-to-peer collaboration & message board)
   - **Lab 9:** Deep Research Agent (5-phase bibliometric citation truth-table loop)
   - **Lab 10:** Cloud Operations Agent (Telemetry monitoring & approval-gated healing)
   - **Lab 11:** Agentic SDLC Factory (Requirement intake, rule diff, test synthesis & release gate)
   - **Lab 12:** Responsible Autonomy & Safety Governance (SHA-256 rolling hash chain, state rollback & Four-Fifths fairness)
   - **Lab 13:** Discipline-Specific Agents (CS, ME, CE, EE engineering worklets mapped to NBA Criterion 5)
   - **Lab 14:** Capstone Project Studio (University-wide batch orchestration & NBA/NAAC Tier-1 readiness index)

2. **`Agenti AI Report.pdf`**  
   The complete 36-page Faculty Appraisal Management System Project Report covering system analysis, architecture, UML diagrams, module breakdowns, testing results, and output demonstrations.

3. **`Project worklet.pdf`**  
   The consolidated Lab Worklet Review & Evaluation Sheet covering all Hands-on Labs (1 to 14), including the Team Introduction page and the Marks Summary sheet.

---

## 🚀 Quick Start Guide

### 1. Environment Setup
```bash
cd faculty-appraisal-agentic-ai
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Database Seeding & Verification
```bash
python run.py seed
python run.py test
```

### 3. Launching the Interfaces
```bash
# Launch Interactive Streamlit Dashboard
python run.py dashboard

# Or launch FastAPI REST Backend
python run.py api
```
