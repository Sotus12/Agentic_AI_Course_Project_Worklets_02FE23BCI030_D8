# Architecture Overview: Faculty Appraisal Management System

**Course:** Agentic AI  
**Scope:** Comprehensive Labs 1–12 (Runtime, MCP, Memory, Node Graphs, Swarms, Deep Research, Cloud Ops, SDLC, Governance)  
**Status:** Educational prototype using synthetic data only  
**Disclaimer:** *Demo Appraisal Policy — configurable; not official institutional scoring policy.*

---

## 1. High-Level System Architecture

The Faculty Appraisal Management System is structured as a multi-agent architecture powered by a generic, registry-based runtime (`OpenCLA/OpenClaw` style), an educational Model Context Protocol (MCP) connector, and scoped persistent memory.

```mermaid
graph TD
    User([User / Evaluator]) -->|Trigger Run| Dashboard[Streamlit Dashboard / FastAPI]
    Dashboard --> Coordinator[Appraisal Coordinator Orchestrator]

    subgraph "Phase 1: Parallel Evidence Collection"
        Coordinator --> Agent1[Research Data Collection Agent]
        Coordinator --> Agent2[Teaching-Learning Data Collection Agent]
        Coordinator --> Agent3[Administrative Data Collection Agent]
    end

    subgraph "Phase 2 & 3: Validation & Scoring"
        Agent1 & Agent2 & Agent3 --> Agent4[Evidence Validation Agent]
        Agent4 --> Agent5[API Calculation Agent]
    end

    subgraph "Phase 4: Synthesis & Output"
        Agent5 --> Agent6[Report Generation Agent]
        Agent6 --> Artifacts[PDF & JSON Appraisal Reports]
    end

    subgraph "OpenCLA Runtime Infrastructure (Lab 6)"
        Runtime[AgentRuntime Engine]
        Registry[SKILL_REGISTRY]
        ToolReg[ToolRegistry]
        Mem[Scoped Persistent Memory - Lab 4]
        Audit[Structured Audit Logging]
    end

    subgraph "MCP Connector Layer (Lab 5)"
        MCP[MCP Server & Client]
        FileRead[file_read Boundary Guard]
        DBQuery[db_query SELECT-Only Guard]
        APIGet[api_get Endpoint Guard]
    end

    Agent1 & Agent2 & Agent3 & Agent4 & Agent5 & Agent6 --> Runtime
    Runtime --> Registry
    Runtime --> ToolReg
    Runtime --> Mem
    Runtime --> Audit
    Runtime --> MCP
```

---

## 2. Six Domain Agents + Coordinator

| Entity | Role | Responsibilities | Agentic Cycle |
|---|---|---|---|
| **Coordinator** | Orchestrator (Infrastructure) | Coordinates parallel collection, manages state transitions, handles errors | Orchestrates pipeline |
| **Research Agent** | Domain Agent 1 | Gathers publications, conferences, patents, projects from CSVs/PDFs | Plan ➔ Act ➔ Observe ➔ Decide |
| **Teaching Agent** | Domain Agent 2 | Analyzes courses, attendance records, student evaluations, pass rates | Plan ➔ Act ➔ Observe ➔ Decide |
| **Administration Agent** | Domain Agent 3 | Extracts committee memberships, coordinator roles, institutional activities | Plan ➔ Act ➔ Observe ➔ Decide |
| **Evidence Validation Agent** | Domain Agent 4 | Validates file existence, format readability, completeness, flags duplicates | Plan ➔ Act ➔ Observe ➔ Decide |
| **API Calculation Agent** | Domain Agent 5 | Deterministically calculates scores based strictly on VALID evidence | Plan ➔ Act ➔ Observe ➔ Decide |
| **Report Generation Agent** | Domain Agent 6 | Generates PDF & JSON drafts marked "Awaiting Human Review" | Plan ➔ Act ➔ Observe ➔ Decide |

---

## 3. Core Principles & Design Decisions

1. **Deterministic Scoring (No LLM Hallucinations):** Scoring is evaluated strictly using criteria defined in `config/scoring_rules.json`.
2. **Registry-Based Runtime:** New skills can be registered dynamically without modifying any line of `AgentRuntime.run_task` or adding `if/elif` ladders.
3. **Strict Memory Isolation:** Scoped key-value store backed by SQLite isolates data per faculty identifier (`faculty:FAC001`).
4. **Security Boundaries in MCP:**
   - Database queries are restricted strictly to `SELECT`.
   - File reads are restricted to the faculty's home directory (`data/faculty/{faculty_id}`).
   - API endpoints are matched against an explicit whitelist.
5. **Human-in-the-Loop:** Appraisals are designated `DRAFT` until an authorized evaluator reviews and approves the report.
