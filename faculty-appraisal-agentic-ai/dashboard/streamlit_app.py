"""
Streamlit Dashboard
Faculty Appraisal Management System (Agentic AI - Labs 1–6)
Clean, functional, and visually informative presentation for course demonstration.
"""
import os
import sys
import json
import streamlit as st

# Setup system path to import app modules
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from app.database.database import execute_query, execute_write
from app.agents.coordinator import AppraisalCoordinator
from app.runtime.audit import AuditLogger
from app.mcp.client import MCPClient

st.set_page_config(
    page_title="Faculty Appraisal Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom header styling
st.markdown(
    """
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0px; }
    .subtitle { font-size: 1.05rem; color: #4B5563; margin-bottom: 15px; }
    .demo-banner { background-color: #FEF3C7; border-left: 4px solid #F59E0B; padding: 10px 14px; border-radius: 4px; font-size: 0.9rem; color: #92400E; margin-bottom: 20px; }
    .badge-valid { background-color: #D1FAE5; color: #065F46; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
    .badge-invalid { background-color: #FEE2E2; color: #991B1B; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
    .badge-review { background-color: #FEF3C7; color: #92400E; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Top Bar / Branding
st.markdown('<div class="main-title">🎓 Faculty Appraisal Management System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Agentic AI Course Project — Labs 1–6 Demonstration (OpenCLA Runtime, MCP, Scoped Memory)</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="demo-banner">⚠️ <b>Notice:</b> Demo Appraisal Policy — configurable; not official institutional scoring policy. Educational prototype with synthetic data.</div>',
    unsafe_allow_html=True,
)

# Initialize Session State
if "coordinator" not in st.session_state:
    st.session_state.coordinator = AppraisalCoordinator()
if "last_run" not in st.session_state:
    st.session_state.last_run = None
if "audit_logger" not in st.session_state:
    st.session_state.audit_logger = AuditLogger()
if "mcp_client" not in st.session_state:
    st.session_state.mcp_client = MCPClient()

from app.graph.appraisal_graph import create_appraisal_node_graph
from app.swarm.swarm import AppraisalSwarm
from app.research.deep_research import DeepResearchAgent
from app.cloud.cloud_agent import CloudOperationsAgent
from app.sdlc.sdlc_factory import AgenticSDLCFactory
from app.governance.responsible_autonomy import ResponsibleAutonomyEngine
from app.discipline.discipline_agents import DisciplineAppraisalCoordinator
from app.capstone.studio import CapstoneProjectStudio

if "graph_engine" not in st.session_state:
    st.session_state.graph_engine = create_appraisal_node_graph()
if "swarm_engine" not in st.session_state:
    st.session_state.swarm_engine = AppraisalSwarm()
if "research_engine" not in st.session_state:
    st.session_state.research_engine = DeepResearchAgent()
if "cloud_agent" not in st.session_state:
    st.session_state.cloud_agent = CloudOperationsAgent()
if "sdlc_factory" not in st.session_state:
    st.session_state.sdlc_factory = AgenticSDLCFactory()
if "governance_engine" not in st.session_state:
    st.session_state.governance_engine = ResponsibleAutonomyEngine()
if "discipline_engine" not in st.session_state:
    st.session_state.discipline_engine = DisciplineAppraisalCoordinator()
if "studio_engine" not in st.session_state:
    st.session_state.studio_engine = CapstoneProjectStudio()

# Navigation Sidebar
st.sidebar.title("Navigation")
menu_option = st.sidebar.radio(
    "Select View",
    [
        "Dashboard",
        "Evidence",
        "Agent Trace",
        "Score Breakdown",
        "Report",
        "Lab 5 MCP Inspector",
        "Lab 7 Node Graph",
        "Lab 8 Swarm Consensus",
        "Lab 9 Deep Research",
        "Lab 10 Cloud Operations",
        "Lab 11 Agentic SDLC",
        "Lab 12 Responsible Autonomy",
        "Lab 13 Discipline Agents",
        "Lab 14 Capstone Studio",
    ],
    index=0,
)

# Fetch all registered faculty members from SQLite
faculty_list = execute_query("SELECT * FROM faculty ORDER BY faculty_id ASC")
if not faculty_list:
    faculty_list = [{
        "faculty_id": "FAC001",
        "name": "Dr. Ananya Rao",
        "department": "Computer Science and AI",
        "designation": "Associate Professor",
        "academic_year": "2026-27",
    }]

# Faculty Selector in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Select Faculty")
faculty_options = {f"{f['name']} ({f['faculty_id']})": f for f in faculty_list}
selected_faculty_label = st.sidebar.selectbox(
    "Choose Faculty Member",
    options=list(faculty_options.keys()),
    index=0
)
faculty = faculty_options[selected_faculty_label]

# Sidebar Selected Faculty Info
st.sidebar.markdown(f"**Selected:** {faculty['name']}")
st.sidebar.markdown(f"**ID:** `{faculty['faculty_id']}`")
st.sidebar.markdown(f"**Designation:** {faculty['designation']}")
st.sidebar.markdown(f"**Department:** {faculty['department']}")
st.sidebar.markdown(f"**Academic Year:** {faculty['academic_year']}")

# ==============================================================================
# VIEW 1: DASHBOARD
# ==============================================================================
if menu_option == "Dashboard":
    st.subheader("Faculty Overview & Appraisal Execution")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.info(
            f"**Candidate:** {faculty['name']} | **Designation:** {faculty['designation']} | "
            f"**Department:** {faculty['department']} | **Session:** {faculty['academic_year']}"
        )

    with col2:
        run_btn = st.button("🚀 RUN APPRAISAL PIPELINE", type="primary", use_container_width=True)

    if run_btn:
        with st.spinner("Orchestrator coordinating 6 domain agents in parallel and sequence..."):
            pipeline_result = st.session_state.coordinator.run_appraisal_pipeline(
                faculty_id=faculty["faculty_id"],
                academic_year=faculty["academic_year"],
            )
            st.session_state.last_run = pipeline_result
            st.success(f"Appraisal run {pipeline_result.get('run_id')} executed successfully in {pipeline_result.get('duration_ms')}ms!")

    # Display results if available
    latest_appraisal_rows = execute_query(
        "SELECT * FROM appraisal_results WHERE faculty_id = ? ORDER BY created_at DESC LIMIT 1",
        (faculty["faculty_id"],)
    )

    if latest_appraisal_rows:
        latest = latest_appraisal_rows[0]
        st.markdown("### Latest Appraisal Score Summary")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Research Score", f"{latest['research_score']} / 40")
        m2.metric("Teaching Score", f"{latest['teaching_score']} / 40")
        m3.metric("Administration Score", f"{latest['administration_score']} / 20")
        m4.metric("Total Score", f"{latest['total_score']} / 100")

        # Evidence Status Summary
        run_id = latest["run_id"]
        val_rows = execute_query(
            "SELECT status, count(*) as count FROM validation_results WHERE run_id = ? GROUP BY status",
            (run_id,)
        )
        val_counts = {r["status"]: r["count"] for r in val_rows}

        st.markdown("### Evidence Validation Overview")
        e1, e2, e3 = st.columns(3)
        e1.metric("✅ VALID Evidence", val_counts.get("VALID", 0))
        e2.metric("⚠️ NEEDS REVIEW", val_counts.get("NEEDS_REVIEW", 0))
        e3.metric("❌ INVALID Evidence", val_counts.get("INVALID", 0))

        st.markdown(f"**Status:** `{latest['status']}` | **Run ID:** `{latest['run_id']}`")
    else:
        st.info("No appraisal executed yet for this session. Click **'RUN APPRAISAL PIPELINE'** above to trigger the agents.")

# ==============================================================================
# VIEW 2: EVIDENCE VIEW
# ==============================================================================
elif menu_option == "Evidence":
    st.subheader("Collected Evidence & Validation Status")

    filter_cat = st.selectbox("Filter Category", ["All Categories", "Research", "Teaching", "Administration"])

    query = """
    SELECT e.evidence_id, e.category, e.sub_category, e.title, e.description,
           v.status as validation_status, v.reason
    FROM evidence e
    LEFT JOIN validation_results v ON e.evidence_id = v.evidence_id
    WHERE e.faculty_id = ?
    """
    params = [faculty["faculty_id"]]

    if filter_cat != "All Categories":
        query += " AND e.category = ?"
        params.append(filter_cat.lower())

    query += " ORDER BY e.category, e.evidence_id"
    rows = execute_query(query, tuple(params))

    if not rows:
        st.info("No evidence records found.")
    else:
        for r in rows:
            status = r.get("validation_status") or "PENDING"
            if status == "VALID":
                badge_html = f'<span class="badge-valid">VALID</span>'
            elif status == "INVALID":
                badge_html = f'<span class="badge-invalid">INVALID</span>'
            elif status == "NEEDS_REVIEW":
                badge_html = f'<span class="badge-review">NEEDS REVIEW</span>'
            else:
                badge_html = f'<span style="background:#E5E7EB;padding:3px 8px;border-radius:4px;">{status}</span>'

            with st.expander(f"[{r['category'].upper()}] {r['title']} - {status}"):
                st.markdown(f"**Sub-Category:** `{r['sub_category']}` | **Status:** {badge_html}", unsafe_allow_html=True)
                st.markdown(f"**Details:** {r.get('description') or 'No additional description'}")
                if r.get("reason"):
                    st.markdown(f"**Validation Rationale:** *{r['reason']}*")

# ==============================================================================
# VIEW 3: AGENT TRACE VIEW (CRITICAL LAB DEMONSTRATION)
# ==============================================================================
elif menu_option == "Agent Trace":
    st.subheader("🕵️ Multi-Agent Execution Trace & Audit Log")
    st.markdown("Demonstrating **Lab 1 (Agents vs Chatbots)**, **Lab 2 (Tools)**, and **Lab 6 (OpenCLA Runtime & Audit)**.")

    tab1, tab2, tab3 = st.tabs(["Active Pipeline Trace", "Agent Reasoning Steps (Plan/Act/Observe/Decide)", "Runtime Audit Log (SQLite)"])

    with tab1:
        if st.session_state.last_run:
            st.markdown(f"**Active Run ID:** `{st.session_state.last_run.get('run_id')}` | **Duration:** `{st.session_state.last_run.get('duration_ms')}ms`")

            traces = st.session_state.last_run.get("pipeline_trace", [])
            for event in traces:
                agent = event.get("agent", "Coordinator")
                status = event.get("status", "info")
                msg = event.get("message", "")

                icon = "🤖" if agent != "Coordinator" else "🧭"
                if status == "success" or status == "completed":
                    st.success(f"{icon} **{agent}** — {msg}")
                elif status == "failed":
                    st.error(f"❌ **{agent}** — {msg}")
                else:
                    st.info(f"{icon} **{agent}** — {msg}")
        else:
            st.info("Execute an appraisal run from the Dashboard to view real-time pipeline trace.")

    with tab2:
        if st.session_state.last_run and "agent_steps" in st.session_state.last_run:
            agent_steps = st.session_state.last_run["agent_steps"]
            st.markdown("### Agentic Loop (Plan ➔ Act ➔ Observe ➔ Decide)")
            for step in agent_steps:
                stage = step.get("stage")
                agent = step.get("agent")
                msg = step.get("message")
                details = step.get("details")

                stage_color = {
                    "PLAN": "🔵 **PLAN**",
                    "ACT": "🟣 **ACT**",
                    "OBSERVE": "🟢 **OBSERVE**",
                    "DECIDE": "🟠 **DECIDE**",
                }.get(stage, stage)

                st.markdown(f"{stage_color} `[{agent}]`: {msg}")
                if details:
                    st.caption(f"Details: {details}")
        else:
            st.info("Run the appraisal pipeline to view detailed step-by-step reasoning steps.")

    with tab3:
        st.markdown("### Persisted Audit Records (`audit_logs` Table)")
        audit_records = st.session_state.audit_logger.get_logs(faculty_id=faculty["faculty_id"])
        if audit_records:
            st.dataframe(audit_records, use_container_width=True)
        else:
            st.write("No audit logs recorded yet.")

# ==============================================================================
# VIEW 4: SCORE BREAKDOWN
# ==============================================================================
elif menu_option == "Score Breakdown":
    st.subheader("📊 Deterministic API Score Breakdown")
    st.caption("Configurable demo policy. Scoring is completely deterministic — no LLM hallucinations.")

    latest_appraisal_rows = execute_query(
        "SELECT * FROM appraisal_results WHERE faculty_id = ? ORDER BY created_at DESC LIMIT 1",
        (faculty["faculty_id"],)
    )

    if latest_appraisal_rows:
        latest = latest_appraisal_rows[0]
        breakdown = {}
        if latest.get("score_breakdown"):
            try:
                breakdown = json.loads(latest["score_breakdown"])
            except Exception:
                pass

        col1, col2, col3 = st.columns(3)
        col1.metric("Research", f"{latest['research_score']} / 40")
        col2.metric("Teaching", f"{latest['teaching_score']} / 40")
        col3.metric("Administration", f"{latest['administration_score']} / 20")

        st.markdown("---")
        st.markdown("### Detailed Category Calculations")

        # Research details
        with st.expander("🔬 Research Scoring Calculation (Max 40)", expanded=True):
            res_details = breakdown.get("research", {}).get("details", {})
            st.write("Criteria evaluation based on strictly VALID evidence:")
            st.json(res_details)

        # Teaching details
        with st.expander("📚 Teaching-Learning Scoring Calculation (Max 40)", expanded=True):
            teach_details = breakdown.get("teaching", {}).get("details", {})
            st.write("Course and feedback averages calculation:")
            st.json(teach_details)

        # Administration details
        with st.expander("🏛️ Administration Scoring Calculation (Max 20)", expanded=True):
            adm_details = breakdown.get("administration", {}).get("details", {})
            st.write("Institutional responsibility points:")
            st.json(adm_details)

    else:
        st.info("Please run the appraisal pipeline first.")

# ==============================================================================
# VIEW 5: REPORT & HUMAN-IN-THE-LOOP APPROVAL
# ==============================================================================
elif menu_option == "Report":
    st.subheader("📑 Formal Appraisal Report & Human Review")

    latest_appraisal_rows = execute_query(
        "SELECT * FROM appraisal_results WHERE faculty_id = ? ORDER BY created_at DESC LIMIT 1",
        (faculty["faculty_id"],)
    )

    if latest_appraisal_rows:
        latest = latest_appraisal_rows[0]
        run_id = latest["run_id"]
        status = latest["status"]

        st.markdown(f"**Appraisal ID:** `{latest['appraisal_id']}` | **Run ID:** `{run_id}`")
        if status == "APPROVED":
            st.success(f"✅ Approved by {latest.get('approved_by')} on {latest.get('approved_at')}")
        else:
            st.warning(f"⚠️ Status: **{status} — Awaiting Human Review**")

        st.markdown("### Human-In-The-Loop Review Action")
        st.caption("Under strict educational governance rules, AI drafts must be verified by authorized human evaluators before final institutional record.")

        col1, col2 = st.columns([2, 1])
        with col1:
            approver_name = st.text_input("Approver Name / Role", value="Prof. Department Head (Demo Reviewer)")
        with col2:
            if status != "APPROVED":
                if st.button("✅ Approve Draft Appraisal", type="primary"):
                    execute_write(
                        "UPDATE appraisal_results SET status = 'APPROVED', approved_by = ?, approved_at = CURRENT_TIMESTAMP WHERE appraisal_id = ?",
                        (approver_name, latest["appraisal_id"]),
                    )
                    st.success("Draft approved successfully! Recorded in permanent database history.")
                    st.rerun()

        st.markdown("---")
        st.markdown("### Download Appraisal Documents")

        pdf_path = os.path.join(BASE_DIR, "reports", f"appraisal_{faculty['faculty_id']}_{run_id}.pdf")
        json_path = os.path.join(BASE_DIR, "reports", f"appraisal_{faculty['faculty_id']}_{run_id}.json")

        d1, d2 = st.columns(2)
        with d1:
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Download PDF Report", f, file_name=f"appraisal_{faculty['faculty_id']}_{run_id}.pdf", mime="application/pdf")
            else:
                st.caption("PDF report file will be ready after pipeline run.")

        with d2:
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    st.download_button("📥 Download JSON Report", f.read(), file_name=f"appraisal_{faculty['faculty_id']}_{run_id}.json", mime="application/json")
            else:
                st.caption("JSON report file will be ready after pipeline run.")

    else:
        st.info("No reports generated yet. Execute an appraisal run to produce formal draft reports.")

# ==============================================================================
# VIEW 6: LAB 5 MCP INSPECTOR (INTERACTIVE VIVA / DEMO TESTER)
# ==============================================================================
elif menu_option == "Lab 5 MCP Inspector":
    st.subheader("🔌 Lab 5 — MCP Connector & Security Boundary Test")
    st.markdown("Test the instructor's simplified educational MCP pattern: **Manifest Discovery**, **Allowed Callers**, **Safe SQL Guard**, and **Directory Boundaries**.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 1. Discover Capabilities Manifest")
        if st.button("🔍 Discover Server Capabilities"):
            caps = st.session_state.mcp_client.discover()
            st.json(caps)

    with col2:
        st.markdown("#### 2. Test Security Boundary (Adversarial SQL / Path)")
        test_type = st.selectbox(
            "Select Security Test Case",
            [
                "Valid SELECT (Authorized Caller)",
                "Unsafe UPDATE/DELETE Query (SQL Injection Protection)",
                "Unauthorized Caller Rejection",
                "Path Traversal Attempt (Directory Boundary Protection)",
                "Unknown API Endpoint Rejection",
            ]
        )

        if st.button("🧪 Execute MCP Test"):
            if test_type == "Valid SELECT (Authorized Caller)":
                res = st.session_state.mcp_client.call(
                    capability_name="db_query",
                    caller="research_agent",
                    inputs={"query": "SELECT faculty_id, name, department FROM faculty", "params": []},
                )
                st.write("**Result (Expected Success):**")
                st.json(res)

            elif test_type == "Unsafe UPDATE/DELETE Query (SQL Injection Protection)":
                res = st.session_state.mcp_client.call(
                    capability_name="db_query",
                    caller="research_agent",
                    inputs={"query": f"DELETE FROM faculty WHERE faculty_id = '{faculty['faculty_id']}'", "params": []},
                )
                st.write("**Result (Expected Safe Rejection):**")
                st.error(f"Status: {res.get('status')} | Error: {res.get('error')}")

            elif test_type == "Unauthorized Caller Rejection":
                res = st.session_state.mcp_client.call(
                    capability_name="db_query",
                    caller="unauthorized_external_guest",
                    inputs={"query": "SELECT * FROM faculty", "params": []},
                )
                st.write("**Result (Expected Safe Rejection):**")
                st.error(f"Status: {res.get('status')} | Error: {res.get('error')}")

            elif test_type == "Path Traversal Attempt (Directory Boundary Protection)":
                res = st.session_state.mcp_client.call(
                    capability_name="file_read",
                    caller="research_agent",
                    inputs={"file_path": "../../../sensitive_passwords.txt", "faculty_id": faculty['faculty_id']},
                )
                st.write("**Result (Expected Safe Rejection):**")
                st.error(f"Status: {res.get('status')} | Error: {res.get('error')}")

            elif test_type == "Unknown API Endpoint Rejection":
                res = st.session_state.mcp_client.call(
                    capability_name="api_get",
                    caller="research_agent",
                    inputs={"endpoint": "/unauthorized/admin/backdoor"},
                )
                st.write("**Result (Expected Safe Rejection):**")
                st.error(f"Status: {res.get('status')} | Error: {res.get('error')}")

# ==============================================================================
# VIEW 7: LAB 7 NODE GRAPH (EXPLICIT DAG & HUMAN GATE)
# ==============================================================================
elif menu_option == "Lab 7 Node Graph":
    st.subheader("🕸️ Lab 7 — Agentic Node Graph Execution Engine")
    st.markdown("Explicit Directed Acyclic Graph (DAG) state machine featuring **parallel branches**, **conditional decisions**, and **checkpointed human gates**.")

    g = st.session_state.graph_engine

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 1. Compiled DAG Topology (Mermaid)")
        st.code(g.to_mermaid(), language="mermaid")

    with col2:
        st.markdown("#### 2. Execute Graph Workflow")
        auto_gate = st.checkbox("Auto-Advance Human Gate (Unattended Evaluation)", value=True)
        if st.button("▶️ Execute Appraisal Node Graph", type="primary"):
            with st.spinner("Executing DAG nodes..."):
                res = g.run({
                    "faculty_id": faculty["faculty_id"],
                    "academic_year": faculty["academic_year"],
                    "auto_advance_human_gate": auto_gate,
                }, checkpoint_id=f"CKPT-{faculty['faculty_id']}")
                st.session_state["graph_last_run"] = res

        graph_run = st.session_state.get("graph_last_run")
        if graph_run:
            st.success(f"Graph Status: **{graph_run.get('graph_status')}** | Total Steps: {graph_run.get('total_steps')}")
            st.metric("Computed API Score via Node Graph", f"{graph_run.get('total_score', 0)} / 100")
            if graph_run.get("graph_status") == "PAUSED_FOR_HUMAN":
                st.warning("Workflow PAUSED at HumanReviewGate. Checkpoint saved.")
                if st.button("✅ Human Evaluator Sign-off (Resume Graph)"):
                    res2 = g.resume(f"CKPT-{faculty['faculty_id']}", human_approval=True, approver_name="Prof. Senior Reviewer")
                    st.session_state["graph_last_run"] = res2
                    st.rerun()

    if graph_run and "execution_history" in graph_run:
        st.markdown("---")
        st.markdown("#### 3. Node Step Transition Log")
        st.dataframe(graph_run["execution_history"], use_container_width=True)

# ==============================================================================
# VIEW 8: LAB 8 PARALLEL SWARMS (PEER-TO-PEER CONSENSUS & CONFLICT RESOLUTION)
# ==============================================================================
elif menu_option == "Lab 8 Swarm Consensus":
    st.subheader("🐝 Lab 8 — Parallel Role-Based Swarm & Message Board")
    st.markdown("Decentralized peer-to-peer agent collaboration on a shared message board: **Independent Proposals ➔ Peer Cross-Critique ➔ Consensus Conflict Resolution**.")

    if st.button("🚀 Run 4-Peer Swarm Collaboration", type="primary"):
        with st.spinner("Peer agents deliberating on Message Board..."):
            coord = st.session_state.coordinator
            pipe_data = coord.run_appraisal_pipeline(faculty["faculty_id"], faculty["academic_year"])
            swarm_res = st.session_state.swarm_engine.run_swarm(pipe_data)
            st.session_state["swarm_last_run"] = swarm_res

    swarm_data = st.session_state.get("swarm_last_run")
    if swarm_data:
        m1, m2, m3, m4 = st.columns(4)
        c_scores = swarm_data.get("consensus_scores", {})
        m1.metric("Research Consensus", f"{c_scores.get('research', 0)} / 40")
        m2.metric("Teaching Consensus", f"{c_scores.get('teaching', 0)} / 40")
        m3.metric("Admin Consensus", f"{c_scores.get('administration', 0)} / 20")
        m4.metric("Total Consensus Score", f"{c_scores.get('total', 0)} / 100")

        t1, t2, t3, t4 = st.tabs(["Round 1: Proposals", "Round 2: Cross-Critiques", "Round 3: Resolved Conflicts", "Message Board Log"])
        with t1:
            st.json(swarm_data.get("round_1_proposals", {}))
        with t2:
            st.dataframe(swarm_data.get("round_2_critiques", []), use_container_width=True)
        with t3:
            st.dataframe(swarm_data.get("conflicts_resolved", []), use_container_width=True)
        with t4:
            st.json(swarm_data.get("message_board_trace", []))

# ==============================================================================
# VIEW 9: LAB 9 DEEP RESEARCH (CITATION CROSS-REFERENCING & VERIFICATION MATRIX)
# ==============================================================================
elif menu_option == "Lab 9 Deep Research":
    st.subheader("🔬 Lab 9 — Deep Research Agent (5-Phase Bibliometric Loop)")
    st.markdown("Autonomous research loop: **Question Formulation ➔ Scholarly Search ➔ Extraction ➔ Cross-Referencing ➔ Evidence Synthesis**.")

    if st.button("🔍 Launch Deep Research Citation Verification", type="primary"):
        with st.spinner("Querying scholarly indexing authorities & extracting citation metrics..."):
            res = st.session_state.research_engine.run_research_loop(faculty["faculty_id"])
            st.session_state["deep_research_last_run"] = res

    d_res = st.session_state.get("deep_research_last_run")
    if d_res:
        b_sum = d_res.get("bibliometric_summary", {})
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Research Integrity Quotient", f"{d_res.get('research_integrity_quotient', 0)}%")
        c2.metric("Verified h-index", b_sum.get("verified_h_index", 0))
        c3.metric("Scopus/WoS Q1 Publications", b_sum.get("indexed_q1_count", 0))
        c4.metric("Verified Citations", b_sum.get("total_verified_citations", 0))

        st.markdown("### 📊 Evidence Verification Matrix (Citation Truth Table)")
        st.dataframe(d_res.get("evidence_verification_matrix", []), use_container_width=True)

        with st.expander("🔎 View 5-Phase Deep Research Execution Trace", expanded=False):
            st.json(d_res.get("deep_research_trace", []))

# ==============================================================================
# VIEW 10: LAB 10 CLOUD OPERATIONS (TELEMETRY & SELF-HEALING REMEDIATION)
# ==============================================================================
elif menu_option == "Lab 10 Cloud Operations":
    st.subheader("☁️ Lab 10 — Cloud Operations & Telemetry Agent")
    st.markdown("Observe infrastructure signals, reason on root causes, and execute self-healing actions guarded by **Human Approval Gates**.")

    ca = st.session_state.cloud_agent

    # Display execution outcome banner if just healed
    if "last_cloud_action_result" in st.session_state:
        st.success(st.session_state.pop("last_cloud_action_result"))

    signals = ca.observe_signals()

    st.markdown("#### 1. Live Infrastructure & Storage Telemetry")
    sig_dicts = [
        {"Signal": s.name, "Value": f"{s.value} {s.unit}", "Threshold": s.threshold, "Status": s.status, "Diagnostic Log": s.message}
        for s in signals
    ]
    st.dataframe(sig_dicts, use_container_width=True)

    st.markdown("#### 2. Diagnostic Reasoning & Remediation Plan")
    plan = ca.diagnose_and_plan(signals)
    st.info(f"**Diagnosis:** {plan.diagnosis}\n\n**Root Cause:** {plan.root_cause}")

    st.markdown("#### 3. Action Execution & Approval Gates")
    for act in plan.actions:
        with st.expander(f"⚙️ Action: {act.action_type} (Risk: {act.risk_level})", expanded=True):
            st.write(f"**Description:** {act.description}")
            if act.requires_approval:
                st.warning("⚠️ High Risk Action: Requires Administrator approval.")
                admin_confirm = st.checkbox(f"I authorize executing {act.action_type}", key=f"auth_{act.action_id}")
                if st.button(f"Execute {act.action_type}", key=f"btn_{act.action_id}"):
                    if admin_confirm:
                        res = ca.execute_action(plan.plan_id, act.action_id, human_approved=True)
                        st.session_state["last_cloud_action_result"] = f"✅ {res['status']}: {res['outcome']}"
                        st.rerun()
                    else:
                        st.error("Approval checkbox must be checked to execute high-risk actions.")
            else:
                if st.button(f"Execute {act.action_type}", key=f"btn_{act.action_id}"):
                    res = ca.execute_action(plan.plan_id, act.action_id, human_approved=False)
                    st.session_state["last_cloud_action_result"] = f"✅ {res['status']}: {res['outcome']}"
                    st.rerun()

# ==============================================================================
# VIEW 11: LAB 11 AGENTIC SDLC (POLICY CODING, TEST SYNTHESIS & RELEASE)
# ==============================================================================
elif menu_option == "Lab 11 Agentic SDLC":
    st.subheader("🏭 Lab 11 — Agentic SDLC Factory")
    st.markdown("Autonomous software engineering factory: **Requirements ➔ Specification ➔ Code Generation ➔ Test Synthesis ➔ Regression Verification ➔ Lead Decision Gate**.")

    sdlc = st.session_state.sdlc_factory

    req_input = st.text_area(
        "Enter Policy Extension Requirement:",
        value="Add NBA Criterion 5.2: Award 5 bonus points for patents granted with commercial licensing",
    )

    if st.button("🚀 Run Agentic SDLC Pipeline", type="primary"):
        with st.spinner("Synthesizing specifications, code diffs, and verification tests..."):
            dossier = sdlc.process_requirement(req_input)
            st.session_state["sdlc_last_dossier"] = dossier

    dossier = st.session_state.get("sdlc_last_dossier")
    if dossier:
        st.success(f"Release Dossier: **{dossier.release_id}** | Status: **{dossier.status}**")
        colA, colB = st.columns(2)
        with colA:
            st.markdown("#### Generated Code & Rule Diff")
            st.code(dossier.generated_code_diff, language="diff")
        with colB:
            st.markdown("#### Synthesized Verification Tests")
            st.code(dossier.generated_tests, language="python")
            t_res = dossier.test_results
            if t_res.get("all_tests_passed"):
                st.success(f"✅ All {t_res.get('tests_passed_count')} synthesized tests PASSED! Regression Status: {t_res.get('regression_status')}")
            else:
                st.error("❌ Generated test suite failed.")

        st.markdown("---")
        st.markdown("#### Human Lead Sign-off Gate")
        lead_name = st.text_input("Lead Architect Name", value="Prof. Department Curriculum Chair")
        b1, b2 = st.columns(2)
        with b1:
            if dossier.status == "AWAITING_LEAD_APPROVAL":
                if st.button("✅ Approve & Deploy Release", type="primary"):
                    sign_res = sdlc.approve_release(dossier.release_id, lead_name)
                    st.success(sign_res["message"])
                    st.rerun()
        with b2:
            if dossier.status == "AWAITING_LEAD_APPROVAL":
                if st.button("❌ Reject Release"):
                    sdlc.reject_release(dossier.release_id, "Does not match current semester academic criteria", lead_name)
                    st.warning("Release rejected by lead.")
                    st.rerun()

# ==============================================================================
# VIEW 12: LAB 12 RESPONSIBLE AUTONOMY (SAFETY, CRYPTOGRAPHIC CHAIN & ROLLBACK)
# ==============================================================================
elif menu_option == "Lab 12 Responsible Autonomy":
    st.subheader("🛡️ Lab 12 — Responsible Autonomy, Safety & Governance")
    st.markdown("Enterprise governance controls: **SHA-256 Cryptographic Audit Chain**, **State Rollback Engine**, **Algorithmic Fairness (Four-Fifths Rule)**, and **PII Masking**.")

    gov = st.session_state.governance_engine

    t1, t2, t3, t4 = st.tabs(["Cryptographic Audit Chain", "State Rollback Engine", "Fairness & Parity", "PII Privacy Masking"])

    with t1:
        st.markdown("#### 1. Tamper-Evident SHA-256 Rolling Hash Chain")
        c_ok, c_msg = gov.verify_audit_chain()
        if c_ok:
            st.success(f"✅ {c_msg}")
        else:
            st.error(f"❌ {c_msg}")

        chain_dicts = [b.to_dict() for b in gov.chain]
        st.dataframe(chain_dicts, use_container_width=True)

    with t2:
        st.markdown("#### 2. Appraisal State Rollback Engine")
        st.write("Disputed or corrupted appraisals can be rolled back to point-in-time snapshots with full cryptographic audit trail.")
        snap_col1, snap_col2 = st.columns(2)
        with snap_col1:
            if st.button("📸 Create Current State Snapshot"):
                snap_id = gov.create_state_snapshot("RUN-MANUAL", faculty["faculty_id"], {"status": "ACTIVE_EVALUATION"})
                st.success(f"Snapshot created: `{snap_id}`")
        with snap_col2:
            snap_keys = list(gov.snapshots.keys())
            if snap_keys:
                chosen_snap = st.selectbox("Select Snapshot to Roll Back", options=snap_keys)
                if st.button("⏪ Execute State Rollback", type="primary"):
                    rb = gov.rollback_to_snapshot(chosen_snap, "Disputed appraisal review by Faculty Grievance Board")
                    st.warning(f"Rollback executed: {rb['status']} on run {rb['run_id']}")
            else:
                st.info("No snapshots saved yet. Click above to create one.")

    with t3:
        st.markdown("#### 3. Demographic Parity & Fairness Benchmark")
        fairness = gov.evaluate_fairness()
        f1, f2, f3 = st.columns(3)
        f1.metric("Evaluations Audited", fairness.total_evaluations)
        f2.metric("Disparate Impact Ratio", f"{fairness.disparate_impact_ratio:.2f}")
        f3.metric("EEOC Four-Fifths Status", fairness.demographic_parity_status)

        st.info(f"**Explanation:** {fairness.explanation}")
        st.write("**Department Mean Scores:**")
        st.json(fairness.department_means)

    with t4:
        st.markdown("#### 4. PII Masking & Privacy Sanitizer")
        test_txt = st.text_area(
            "Test Text with Sensitive PII:",
            value=f"For inquiries contact {faculty['name']} at ananya.rao@kletech.ac.in or phone 9876543210 regarding confidential medical leave records.",
        )
        if st.button("🔒 Sanitize & Mask PII"):
            sanitized = gov.sanitize_pii(test_txt)
            st.write("**Sanitized Output:**")
            st.code(sanitized)

# ==============================================================================
# VIEW 13: LAB 13 DISCIPLINE-SPECIFIC AGENTS (ENGINEERING WORKLETS)
# ==============================================================================
elif menu_option == "Lab 13 Discipline Agents":
    st.subheader("🛠️ Lab 13 — Discipline-Specific Worklet Agents (CS / ME / CE / EE)")
    st.markdown("Customized appraisal agents tailored for engineering discipline rubrics & **NBA Criterion 5** accreditation standards.")

    dac = st.session_state.discipline_engine

    st.markdown(f"**Target Faculty:** `{faculty['name']}` | **Department:** `{faculty['department']}`")
    detected_code = dac.detect_discipline(faculty["department"])
    st.info(f"🔍 **Auto-Detected Discipline:** `{detected_code}` ({dac.agents[detected_code].discipline_name})")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### 1. Discipline Worklet Profile")
        agent_obj = dac.agents[detected_code]
        st.write(f"**Discipline Code:** `{agent_obj.discipline_code}`")
        st.write(f"**Discipline Name:** {agent_obj.discipline_name}")
        st.write(f"**Accreditation Mapping:** {agent_obj.nba_criterion_focus}")

    with col2:
        st.markdown("#### 2. Run Discipline Appraisal")
        if st.button("🔬 Evaluate Discipline-Specific Rubric", type="primary"):
            with st.spinner("Applying discipline-specific weighting..."):
                coord = st.session_state.coordinator
                pipe_res = coord.run_appraisal_pipeline(faculty["faculty_id"], faculty["academic_year"])
                disc_eval = dac.evaluate_faculty(faculty, pipe_res)
                st.session_state["disc_last_eval"] = disc_eval

    disc_eval = st.session_state.get("disc_last_eval")
    if disc_eval:
        st.markdown("---")
        st.markdown("#### 3. Discipline Evaluation Results")
        m1, m2, m3, m4 = st.columns(4)
        scores = disc_eval.get("adjusted_scores", {})
        m1.metric("Adjusted Research", f"{scores.get('research', 0)} / 40")
        m2.metric("Adjusted Teaching", f"{scores.get('teaching', 0)} / 40")
        m3.metric("Adjusted Admin", f"{scores.get('administration', 0)} / 20")
        m4.metric("Discipline Total", f"{scores.get('total', 0)} / 100", delta=f"+{disc_eval.get('discipline_bonus_applied')} bonus")

        st.success(f"**NBA Accreditation Status:** {disc_eval.get('nba_compliance_status')} | {disc_eval.get('accreditation_notes')}")
        st.write(f"**Domain Weighting Focus:** {disc_eval.get('domain_weighting_focus')}")

# ==============================================================================
# VIEW 14: LAB 14 CAPSTONE PROJECT STUDIO (FULL MULTI-AGENT SYSTEM)
# ==============================================================================
elif menu_option == "Lab 14 Capstone Studio":
    st.subheader("🎓 Lab 14 — Capstone Project Studio (University Enterprise System)")
    st.markdown("Full team-owned agentic system: **Multi-Faculty Batch Orchestration ➔ Department Rankings ➔ NBA Tier-1 Readiness ➔ Tenure & Promotion Decision Support**.")

    studio = st.session_state.studio_engine

    if st.button("🚀 Launch Institutional Capstone Studio Run", type="primary"):
        with st.spinner("Orchestrating university-wide multi-agent evaluation across all departments..."):
            report = studio.run_institutional_studio(faculty.get("academic_year", "2026-27"))
            st.session_state["studio_last_report"] = report

    report = st.session_state.get("studio_last_report")
    if report:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Faculty Evaluated", report.total_faculty_evaluated)
        c2.metric("University Mean Score", f"{report.university_mean_score} / 100")
        c3.metric("NBA Tier-1 Readiness", f"{report.nba_tier1_readiness_score}%")
        c4.metric("Promotion Eligible", f"{report.promotion_eligible_count} Faculty")

        st.success(f"🏛️ **Institutional Accreditation Rating:** **{report.accreditation_grade}**")

        tab_ranks, tab_tenure, tab_export = st.tabs(["🏆 Department Rankings", "📋 Tenure & Promotion Decisions", "📦 Export Audit Bundle"])

        with tab_ranks:
            st.markdown("#### Departmental Performance & Accreditation Comparison")
            st.dataframe(report.department_rankings, use_container_width=True)

        with tab_tenure:
            st.markdown("#### Faculty Executive Tenure & Promotion Roster")
            verdicts_data = [v.to_dict() if hasattr(v, "to_dict") else v for v in report.faculty_verdicts]
            st.dataframe(verdicts_data, use_container_width=True)

        with tab_export:
            st.markdown("#### Institutional Accreditation Package")
            export_json = json.dumps(report.to_dict(), indent=2)
            st.download_button(
                "📥 Download Institutional Capstone Audit Bundle (JSON)",
                export_json,
                file_name=f"institutional_accreditation_dossier_{report.academic_year}.json",
                mime="application/json",
            )
