# Faculty Appraisal Management System (Agentic AI)

> **Course:** Agentic AI (Comprehensive Labs 1–12 Implementation)  
> **Notice:** *This is an educational prototype using synthetic data.*  
> **Scoring Policy Disclaimer:** *Demo Appraisal Policy — configurable; not official institutional scoring policy.*

---

## 1. Problem Statement
Evaluating faculty annual performance across teaching, research, and institutional administration requires processing diverse evidence formats (papers, student feedback forms, committee appointments), validating their authenticity, applying complex evaluation rules, and compiling auditable appraisal dossiers. Manual review is labor-intensive, error-prone, and inconsistent.

## 2. Objective
Build an autonomous **Multi-Agent AI System** that collects evidence across three faculty domains, validates submissions, calculates a deterministic API appraisal score using configurable rules, and generates human-reviewable appraisal reports, demonstrating the complete set of **12 Core Concepts (Labs 1 through 12)** of the Agentic AI curriculum.

---

## 3. System Architecture & Complete 12 Core Concepts Mapping

| Course Lab | Core Concept | Implementation in This Project |
|---|---|---|
| **Lab 1** | **Agent vs Chatbot** | Autonomous domain agents executing proactive `PLAN ➔ ACT ➔ OBSERVE ➔ DECIDE` cycles; explicit exception handling. |
| **Lab 2** | **Tool-Using Agent** | 12 modular tools across files, database, arithmetic calculation, and PDF/JSON generation managed via `ToolRegistry`. |
| **Lab 3** | **Skill Creation** | 6 reusable skills with `SKILL.md` specifications and code classes loaded through dynamic `SKILL_REGISTRY`. |
| **Lab 4** | **Memory & Retrieval** | Persistent scoped memory backed by SQLite (`faculty:FAC001`) preventing cross-faculty contamination; comparative multi-session analysis. |
| **Lab 5** | **MCP-Style Connector** | Educational MCP Server exposing discoverable `CAPABILITIES` manifest (`file_read`, `db_query`, `api_get`), allowed callers, SELECT-only guards, directory traversal protection. |
| **Lab 6** | **OpenCLA Runtime** | Domain-agnostic runtime (`receive_task()`, dynamic `select_skill()`, audit logging, failure recording, extensibility without core rewrites). |
| **Lab 7** | **Node Graphs** | Explicit Directed Acyclic Graph (`StateGraph`) with parallel branches, conditional quality routing, and checkpointed `HumanGateNode`. |
| **Lab 8** | **Parallel Swarms** | Decentralized 4-peer agent collaboration over a shared `MessageBoard` with independent proposals, peer cross-critiques, and automated consensus conflict resolution. |
| **Lab 9** | **Deep Research** | Autonomous 5-phase research loop (`Question ➔ Search ➔ Extract ➔ Compare ➔ Synthesize`), bibliometric cross-referencing, Citation Truth Table, and Research Integrity Quotient. |
| **Lab 10** | **Cloud Operations** | Live telemetry signal probing (latency, storage, error rate), root-cause diagnostic engine, and self-healing remediation plans guarded by human approval gates. |
| **Lab 11** | **Agentic SDLC** | Agent-run software delivery factory: requirement intake, specification, code diff synthesis, automated test synthesis, regression runner, and release sign-off. |
| **Lab 12** | **Responsible Autonomy** | Cryptographic SHA-256 rolling hash audit chain (tamper-evident log), state snapshot & rollback engine, EEOC Four-Fifths demographic parity evaluator, and PII masking. |
| **Lab 13** | **Discipline-Specific Agents** | Tailored domain worklets for CS, ME, CE, and EE engineering disciplines with specialized weightings and NBA Criterion 5 alignment. |
| **Lab 14** | **Capstone Project Studio** | Full team-owned enterprise studio: university-wide multi-faculty batch evaluation, department performance rankings, NBA Tier-1 readiness scoring, tenure/promotion rosters, and master bundle export. |

---

## 4. The Six Domain Agents & Coordinator

### Domain Agents
1. **Research Data Collection Agent (`research_agent.py`):** Collects publications, conferences, patents, and funded research grants.
2. **Teaching-Learning Data Collection Agent (`teaching_agent.py`):** Analyzes course loads, student evaluations, monthly attendance, and pass rates.
3. **Administrative Data Collection Agent (`administration_agent.py`):** Gathers committee memberships, coordinator roles, and institutional event responsibilities.
4. **Evidence Validation Agent (`validation_agent.py`):** Checks evidence completeness, verifies file integrity, detects duplicates, and assigns `VALID`, `INVALID`, or `NEEDS_REVIEW`.
5. **API Calculation Agent (`api_calculation_agent.py`):** Deterministically calculates appraisal scores from strictly `VALID` evidence using `config/scoring_rules.json`. *(Note: "API" refers to faculty appraisal scoring, not REST APIs).*
6. **Report Generation Agent (`report_agent.py`):** Generates formal PDF and JSON draft appraisal documents marked *"Awaiting Human Review"*.

### Coordinator (Infrastructure Orchestrator)
The **Coordinator (`coordinator.py`)** is orchestration infrastructure (not counted among the 6 domain agents). It executes Research, Teaching, and Administration data collection in parallel threads, pipelines results through Validation, Scoring, and Reporting, tracks execution duration, and records the overall run state.

---

## 5. Technology Stack

- **Language:** Python 3.10+
- **Agent Runtime:** OpenCLA/OpenClaw-style registry architecture
- **Connector:** Model Context Protocol (MCP) educational server pattern
- **Backend API:** FastAPI & Uvicorn
- **Dashboard UI:** Streamlit
- **Persistence & Audit:** SQLite (normalized relational schema & key-value memory)
- **Document Generation:** `fpdf2` (PDF) and Python `json`
- **Data Parsing:** `pandas` and standard `csv`
- **Test Framework:** `pytest`

---

## 6. Project Directory Structure

```text
faculty-appraisal-agentic-ai/
├── app/
│   ├── agents/               # 6 Domain Agents + BaseAgent + Coordinator
│   │   ├── base_agent.py
│   │   ├── research_agent.py
│   │   ├── teaching_agent.py
│   │   ├── administration_agent.py
│   │   ├── validation_agent.py
│   │   ├── api_calculation_agent.py
│   │   ├── report_agent.py
│   │   └── coordinator.py
│   ├── tools/                # Reusable Tools (Files, DB, Calc, Report)
│   │   ├── file_tools.py
│   │   ├── database_tools.py
│   │   ├── calculation_tools.py
│   │   └── report_tools.py
│   ├── skills/               # Reusable Skills with SKILL.md specs
│   │   ├── base_skill.py
│   │   ├── research_appraisal/
│   │   ├── teaching_appraisal/
│   │   ├── administration_appraisal/
│   │   ├── evidence_validation/
│   │   ├── api_calculation/
│   │   └── report_generation/
│   ├── runtime/              # OpenCLA/OpenClaw Runtime Engine
│   │   ├── runtime.py
│   │   ├── skill_registry.py
│   │   ├── tool_registry.py
│   │   ├── memory.py
│   │   └── audit.py
│   ├── mcp/                  # MCP-Style Server & Client
│   │   ├── server.py
│   │   ├── client.py
│   │   ├── capabilities.py
│   │   └── security.py
│   ├── database/             # SQLite database layer & seed script
│   │   ├── schema.sql
│   │   ├── database.py
│   │   └── seed.py
│   └── api/                  # FastAPI REST endpoints
│       └── main.py
├── dashboard/                # Streamlit UI
│   └── streamlit_app.py
├── config/                   # Configurable Scoring Rules
│   └── scoring_rules.json
├── data/faculty/             # Synthetic faculty data (FAC001)
├── reports/                  # Generated PDF and JSON reports
├── tests/                    # Pytest automated test suite (24 tests)
├── docs/                     # Lab documentation & demo scripts
│   ├── architecture.md
│   ├── lab1.md to lab6.md
│   ├── demo-script.md
│   └── viva.md
├── requirements.txt
├── README.md
└── run.py                    # Unified CLI launcher
```

---

## 7. Installation & Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed Database with Synthetic Demo Data
```bash
python run.py seed
```

### 3. Launch Streamlit Dashboard
```bash
python run.py dashboard
```
*Access the interactive interface at `http://localhost:8501`.*

### 4. Optional: Run FastAPI Backend
```bash
python run.py api
```
*Access REST API docs at `http://127.0.0.1:8000/docs`.*

---

## 8. Running the Automated Test Suite

Run all 24 unit and integration tests:
```bash
python run.py test
```
*Or directly via pytest:*
```bash
python -m pytest -v
```

All 24 tests validate:
- Lab 2 Tool execution & permission rejection
- Lab 4 Scoped memory isolation (no cross-faculty leakage)
- Lab 5 MCP manifest discovery, SELECT-only queries, path traversal rejection, unauthorized caller rejection
- Lab 6 OpenCLA runtime execution, audit logging, and **dynamic skill registration without modifying runtime core**
- Deterministic scoring bounds and cap verification
- Full end-to-end multi-agent pipeline orchestration.

---

## 9. Interactive Dashboard Features

The Streamlit dashboard includes 12 purpose-built views:
1. **Dashboard:** Profile overview for Dr. Ananya Rao (`FAC001`), one-click **RUN APPRAISAL PIPELINE**, and executive score summary metrics.
2. **Evidence:** Filterable inventory of collected items with status badges (`VALID`, `INVALID`, `NEEDS REVIEW`) and validation explanations.
3. **Agent Trace:** Live multi-agent execution pipeline trace, individual agent reasoning loops (`PLAN ➔ ACT ➔ OBSERVE ➔ DECIDE`), and persistent SQLite `audit_logs`.
4. **Score Breakdown:** Complete transparent arithmetic breakdown for Research (40), Teaching (40), and Administration (20).
5. **Report & Human Review:** Download generated PDF/JSON appraisal dossiers and perform Human-in-the-Loop **Approve Draft** actions.
6. **Lab 5 MCP Inspector:** Interactive viva tool to test server capability discovery, valid SELECT queries, and adversarial SQL / path traversal rejections.
7. **Lab 7 Node Graph:** Live compiled Mermaid DAG visualization, step-by-step state machine execution, and checkpointed Human Review Gate.
8. **Lab 8 Swarm Consensus:** 4-peer decentralized collaboration, independent proposals, cross-critique message board, and consensus conflict resolution.
9. **Lab 9 Deep Research:** 5-phase research loop, citation inflation check, Scopus/WoS Q1 verification, and Research Integrity Quotient.
10. **Lab 10 Cloud Operations:** Live telemetry probe (latency, storage, error rate), root-cause diagnostics, and approval-gated self-healing remediation.
11. **Lab 11 Agentic SDLC:** Policy requirement intake, automatic code diff & test synthesis, verification test runner, and lead architect sign-off gate.
12. **Lab 12 Responsible Autonomy:** SHA-256 rolling hash chain verification, point-in-time state rollback, EEOC Four-Fifths fairness benchmark, and PII masking.
13. **Lab 13 Discipline Agents:** Auto-detection and evaluation across CS, Mechanical, Civil, and Electrical engineering domains with NBA Criterion 5 compliance.
14. **Lab 14 Capstone Studio:** Executive university-scale studio with multi-faculty batch evaluation, department performance rankings, NBA Tier-1 readiness index, tenure/promotion rosters, and master bundle export.

---

## 10. Scope & Academic Notice
- **Implemented Scope:** Complete Labs 1 through 14 implemented, tested with 35 unit/integration tests, and accessible via CLI and Streamlit dashboard.
- **Synthetic Data:** Fictional faculty records across engineering departments for demonstration.
- **Demo Scoring:** The formulas in `config/scoring_rules.json` demonstrate configurable weights and do not claim to reflect official university appraisal regulations.
