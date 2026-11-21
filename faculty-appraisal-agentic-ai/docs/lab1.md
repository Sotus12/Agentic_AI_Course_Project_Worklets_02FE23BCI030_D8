# Lab 1: Agent vs Chatbot Architecture

## 1. Conceptual Distinction

| Dimension | Chatbot (Conversational Model) | Agentic AI System (Multi-Agent System) |
|---|---|---|
| **Objective** | Generate single-turn conversational text | Accomplish complex multi-step goals autonomously |
| **Execution Loop** | Input Prompt ➔ Next-token Prediction ➔ Output | Plan ➔ Act (Tool/Skill) ➔ Observe ➔ Decide / Handle Exception |
| **Tool Usage** | None or strictly passive (e.g. basic browsing) | Proactive tool execution (filesystem, databases, calculators, compilers) |
| **State & Memory** | Ephemeral chat window context | Scoped, persistent state across tasks and multi-year sessions |
| **Error Handling** | Hallucinates or replies with generic apologies | Observes failure, adjusts plan, re-validates, or flags for review |
| **Collaboration** | Monolithic prompt response | Specialized domain agents acting in parallel with orchestration |

---

## 2. Agentic Workflow in This Project

In the Faculty Appraisal Management System, the 6 domain agents operate through structured reasoning phases:

1. **PLAN:** The agent analyzes the goal, identifies needed data sources, and selects the appropriate skill.
   - *Example:* `Research Agent` plans to read publications, conferences, and patents.
2. **ACT:** The agent dispatches execution to a registered runtime skill that invokes sandboxed tools.
   - *Example:* Skill calls `read_csv` and `read_pdf`.
3. **OBSERVE:** The agent examines intermediate tool outputs and checks for anomalies.
   - *Example:* Observes that `CONF001` lacks an attached verification document.
4. **DECIDE:** The agent draws conclusions, updates scoped memory, and passes structured flags downstream.
   - *Example:* Flags missing evidence to the `Evidence Validation Agent`, which assigns `NEEDS_REVIEW` status.

---

## 3. Example Execution Trace (Observable in Dashboard)

```text
[Research Agent]
  🔵 PLAN    : Plan to collect research data for faculty FAC001. Target files: publications, conferences, patents, projects.
  🟣 ACT     : Invoking 'research_appraisal' skill via Agent Runtime.
  🟢 OBSERVE : Retrieved 5 publications, 2 conferences, 1 patents, 2 projects. Detected 1 unattached publication files.
  🟠 DECIDE  : Flagged 1 publications with missing file references for validation review. Structured dataset ready.

[Evidence Validation Agent]
  🔵 PLAN    : Plan to validate all collected evidence items for faculty FAC001.
  🟣 ACT     : Invoking 'evidence_validation' skill via Agent Runtime.
  🟢 OBSERVE : Validation completed: 18 VALID, 0 INVALID, 1 NEEDS_REVIEW.
  🟠 DECIDE  : Validation complete. Filtered only VALID evidence items for deterministic API scoring. Noted 1 items requiring human verification.
```
