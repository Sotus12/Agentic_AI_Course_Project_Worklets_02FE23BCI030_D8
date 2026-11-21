# Professor Demo Script: Faculty Appraisal Management System

**Target Duration:** 5–10 Minutes  
**Demonstrators:** Student Presentation Team  
**Scope:** Labs 1 through 6 (Agentic AI Course Project)

---

## Demo Step-by-Step Flow

### Step 1: Problem Statement & Architecture (1 Minute)
- **Say:** *"Professor, we are presenting our Faculty Appraisal Management System. Unlike chatbots or simple CRUD apps, our prototype implements an Agentic AI architecture satisfying Labs 1 to 6."*
- **Show:** Open `docs/architecture.md` or display the system diagram. Mention the **6 domain agents** (Research, Teaching, Administration, Validation, Scoring, Report) and the **Coordinator** orchestrator.
- **Multi-Faculty Demonstration:** Point out the 3 synthetic faculty candidates available via the sidebar selector:
  1. **Dr. Ananya Rao (FAC001):** Associate Professor, Computer Science and AI (Score: 94.0/100)
  2. **Dr. Rajesh Kumar (FAC002):** Professor, Electronics & Communication (Score: 81.0/100)
  3. **Dr. Sneha Patil (FAC003):** Assistant Professor, Mechanical & Robotics (Score: 61.0/100)
- **Note:** Clarify upfront: *"All data is synthetic and scoring rules are configurable demo rules, not official institutional policy."*

### Step 2: Launch System & Start Pipeline (1.5 Minutes)
- **Command:** `python run.py dashboard` (starts Streamlit at `http://localhost:8501`).
- **Show View 1 (Dashboard):** Point out Dr. Ananya Rao's profile.
- **Action:** Click **"🚀 RUN APPRAISAL PIPELINE"**.
- **Point Out:** Watch the Coordinator trigger the parallel execution across Research, Teaching, and Administration, followed by Validation, API Scoring, and Report Generation.

### Step 3: View Results & Scores (1.5 Minutes)
- **Show Metrics:**
  - Research: `36.0 / 40`
  - Teaching: `38.0 / 40`
  - Administration: `20.0 / 20`
  - Total: `94.0 / 100`
- **Show Evidence Summary:** `18 VALID`, `1 NEEDS_REVIEW`, `0 INVALID`.
- **Show View 4 (Score Breakdown):** Explain that the scoring is **100% deterministic** calculated from `config/scoring_rules.json` — zero LLM hallucinations.

### Step 4: Inspect Evidence & Validation (1 Minute)
- **Show View 2 (Evidence):**
  - Show a `VALID` publication with verified file.
  - Show the `NEEDS_REVIEW` conference paper (`CONF001`) where the agent detected missing verification documentation.
  - Explain how the validation agent prevents unverified data from inflating scores.

### Step 5: Agent Trace & Lab 1/Lab 6 Demonstration (1.5 Minutes)
- **Show View 3 (Agent Trace):**
  - **Tab 1 (Pipeline Trace):** Show the coordinator's parallel worker thread execution and completion timestamps.
  - **Tab 2 (Agentic Loop):** Show explicit `PLAN ➔ ACT ➔ OBSERVE ➔ DECIDE` steps for each agent.
  - **Tab 3 (Runtime Audit Log):** Show the persistent SQLite records in the `audit_logs` table tracking tool executions and run durations.

### Step 6: Lab 5 MCP Connector & Security Boundary Test (1.5 Minutes)
- **Show View 6 (Lab 5 MCP Inspector):**
  - **Action 1:** Click **"🔍 Discover Server Capabilities"**. Show the discoverable JSON manifest with `file_read`, `db_query`, `api_get`.
  - **Action 2:** Select **"Unsafe UPDATE/DELETE Query"** and click **"🧪 Execute MCP Test"**. Show immediate rejection: `Only SELECT queries are allowed`.
  - **Action 3:** Select **"Path Traversal Attempt"**. Show immediate rejection: `Path traversal rejected outside allowed directory`.

### Step 7: Reports & Human-In-The-Loop Review (1 Minute)
- **Show View 5 (Report):**
  - Show the draft status: `Status: DRAFT — Awaiting Human Review`.
  - Click **"Download PDF Report"** and open the generated PDF with full breakdowns and warnings.
  - Demonstrate the Human-in-the-Loop action: Enter reviewer name and click **"✅ Approve Draft Appraisal"**. Show status change to `APPROVED`.

### Step 8: Conclude & Run Automated Test Suite (30 Seconds)
- **Command:** `python run.py test`
- **Show:** All 24 tests passing in under 1 second, confirming:
  - Memory isolation (Lab 4)
  - MCP security guards (Lab 5)
  - OpenCLA runtime dynamic skill registration without code modification (Lab 6).
