# Viva Voce Preparation Guide: Agentic AI Course Project

Comprehensive question and answer guide for oral examination on Labs 1 through 6.

---

### Q1: What is an Agent? How is it different from a Chatbot?
**Answer:** A chatbot is a passive, conversational language interface that generates responses token-by-token based on conversational history. An **Agent** is an autonomous entity endowed with goals, a reasoning loop (Plan ➔ Act ➔ Observe ➔ Decide), access to external tools (databases, filesystems, calculation engines), persistent memory, and the capacity to perceive environmental outcomes and recover from failures.

### Q2: Why are there six domain agents? What is the Coordinator?
**Answer:** Each domain agent represents a distinct functional responsibility with dedicated inputs, outputs, and validation boundaries:
1. **Research Agent:** Extraction of scholarship, publications, and patents.
2. **Teaching Agent:** Analysis of pedagogical metrics, attendance, and feedback.
3. **Administration Agent:** Extraction of committee and institutional services.
4. **Evidence Validation Agent:** Independent verification of file integrity, duplicates, and completeness.
5. **API Calculation Agent:** Deterministic calculation of appraisal scores.
6. **Report Generation Agent:** Formal document synthesis (PDF/JSON).
The **Coordinator** is the orchestration infrastructure (not a domain agent) that manages parallel and sequential execution, handles state transitions, and records the complete run.

### Q3: What is the difference between a Tool and a Skill?
**Answer:**
- **Tool (Lab 2):** A low-level, atomic execution primitive (e.g. `read_csv`, `calculate_average`, `query_faculty_data`). It does not contain domain workflow logic.
- **Skill (Lab 3):** A higher-level, modular capability package (governed by a `SKILL.md` specification and implemented as a `BaseSkill`) that orchestrates multiple tools to accomplish a domain goal.

### Q4: What is Scoped Memory and why didn't you use a Vector Database?
**Answer:** Vector databases and retrieval-augmented generation (RAG) are designed for unstructured semantic similarity search across massive text corpora. In our faculty appraisal system:
1. Faculty records are structured, deterministic, and relational (CSVs, database rows, profile JSONs).
2. Appraisal scoring requires exact numerical values rather than fuzzy semantic matches.
3. A vector database would introduce unnecessary overhead, non-deterministic retrieval, and risk of hallucinations.
We implemented **Scoped Persistent Memory** backed by SQLite, strictly isolating memory by faculty ID (`faculty:FAC001`) to eliminate cross-faculty context leakage.

### Q5: What is Model Context Protocol (MCP) and why is it used?
**Answer:** MCP is an architectural protocol that standardizes how agents discover and access external data and tools. By adopting the instructor's Lab 5 simplified MCP server:
1. The client **dynamically discovers capabilities** from a manifest instead of hard-coding them.
2. The connector enforces security boundaries: rejecting unauthorized callers, rejecting non-SELECT SQL queries, and blocking path traversal attempts outside allowed faculty directories.

### Q6: Why is `db_query` restricted strictly to SELECT?
**Answer:** Principle of Least Privilege. Agents analyzing evidence only require read access. Allowing `INSERT`, `UPDATE`, or `DELETE` would allow an agent or potential prompt injection attack to modify database records or corrupt appraisal histories.

### Q7: What is an OpenCLA / OpenClaw style Runtime? How does skill selection work?
**Answer:** It is a domain-agnostic execution engine that receives tasks, resolves appropriate skills from an extensible `SKILL_REGISTRY`, loads allowed tools, provisions scoped memory, and writes audit logs. It does not use `if/elif` ladders; adding a new skill requires registering the class in `SKILL_REGISTRY` without altering the runtime core.

### Q8: What happens when an evidence file is missing or invalid?
**Answer:** The system does not crash or hallucinate data. The collection agent observes the anomaly and flags it. The `Evidence Validation Agent` marks the item as `NEEDS_REVIEW` or `INVALID`. The `API Calculation Agent` filters strictly on `VALID` items, excluding questionable evidence from the score. The `Report Generation Agent` includes an explicit warning banner in the generated PDF report.

### Q9: Why is scoring deterministic rather than LLM-generated?
**Answer:** Appraisal scores affect faculty career advancement and institutional accreditation. LLM score generation is non-deterministic and prone to drift and hallucinations. Our scoring rules are defined in `config/scoring_rules.json` and computed through explicit arithmetic functions.

### Q10: Why is Human-in-the-Loop review mandatory?
**Answer:** Agentic AI systems should assist and accelerate evaluation, but never usurp institutional governance authority. All AI-generated appraisals are marked `DRAFT — Awaiting Human Review` until an authorized human evaluator reviews and approves them.

---

---

## Labs 7 through 12 Implementation Guide & Viva Questions

### Q11: How is the Node Graph in Lab 7 implemented? What is the Human Gate?
**Answer:** In `app/graph/engine.py` and `app/graph/appraisal_graph.py`, we implemented an explicit Directed Acyclic Graph (`StateGraph`) with stateful nodes and conditional edges (`ConditionEdge`). It forks parallel data collection across 3 branches (`ParallelBranchNode`), evaluates evidence quality to conditionally route clean vs flagged dossiers, and halts at `HumanGateNode` to serialize a checkpoint (`CKPT-{id}`). Execution only resumes when an authorized human evaluator submits a sign-off signal.

### Q12: How does the Parallel Swarm in Lab 8 achieve consensus without a centralized coordinator?
**Answer:** In `app/swarm/`, 4 role-based peer agents (`ResearchPeerAgent`, `PedagogyPeerAgent`, `GovernancePeerAgent`, `QualityAssurancePeerAgent`) interact across a shared `MessageBoard`. In Round 1, peers publish independent proposals. In Round 2, peers read fellow proposals and publish cross-critiques and adjustment recommendations. In Round 3, a decentralized consensus merge reconciles score variances, logs resolved conflicts, and outputs a consensus dossier.

### Q13: What are the 5 phases of the Deep Research Agent in Lab 9?
**Answer:** In `app/research/deep_research.py`, the agent executes:
1. **Question Formulation:** Synthesizes 3 targeted bibliometric queries per publication claim.
2. **Search:** Queries scholarly indexing authorities (Scopus, WoS, IEEE, ACM).
3. **Extraction:** Retrieves verified citation counts, journal quartile (Q1-Q4), and impact factor.
4. **Comparative Analysis:** Cross-references claimed vs verified citations to detect inflation.
5. **Synthesis:** Builds an Evidence Verification Matrix and calculates a Research Integrity Quotient.

### Q14: How does the Cloud Operations Agent in Lab 10 protect against risky remediation?
**Answer:** In `app/cloud/cloud_agent.py`, the agent probes live infrastructure telemetry (latency, storage size, audit error rate). Upon diagnosing issues, it categorizes remediation actions into `LOW` risk (e.g., pruning old test reports) which can be automated, and `HIGH` risk (e.g., database compaction via VACUUM, worker resets) which strictly require an administrator approval gate before execution.

### Q15: How does the Agentic SDLC Factory in Lab 11 guarantee that generated policy changes do not cause regression?
**Answer:** In `app/sdlc/sdlc_factory.py`, upon receiving a human requirement, the agent synthesizes specifications, generated code diffs, and unit/boundary test cases. It automatically runs the test suite in a sandboxed verification runner to ensure cap enforcement and regression stability before presenting an `SDLCReleaseDossier` for human lead sign-off.

### Q16: How does Responsible Autonomy in Lab 12 provide mathematical tamper-evidence and fairness?
**Answer:** In `app/governance/responsible_autonomy.py`:
1. **Cryptographic SHA-256 Rolling Hash Chain:** Each audit event hashes `previous_hash + timestamp + event + payload`. Any database modification invalidates the hash chain.
2. **State Rollback Engine:** Can restore point-in-time snapshots for contested appraisals.
3. **Four-Fifths Rule Fairness:** Evaluates demographic parity and disparate impact across academic departments.
4. **PII Masking:** Anonymizes emails, phones, and sensitive medical/personal identifiers.

### Q17: How does Lab 13 implement Discipline-Specific Agents? Why is a single scoring rubric insufficient?
**Answer:** In `app/discipline/discipline_agents.py`, academic disciplines have fundamentally different scholarship and service profiles. Computer Science prioritizes top-tier IEEE/ACM conference proceedings and open-source models (NBA Criterion 5.3), Mechanical Engineering prioritizes physical prototyping, testing consultancy, and fabrication labs (NBA Criterion 5.4), Civil Engineering emphasizes structural audits and PWD field projects (NBA Criterion 5.5), and Electrical Engineering centers on embedded testbeds and hardware designs (NBA Criterion 5.6). `DisciplineAppraisalCoordinator` auto-detects the department and dynamically applies the appropriate discipline rubric and bonus weighting.

### Q18: What is the Capstone Project Studio in Lab 14? What decisions does it support?
**Answer:** In `app/capstone/studio.py`, the Capstone Studio scales the multi-agent system from individual evaluations to university-wide institutional governance. It batch-evaluates all faculty members, computes departmental performance rankings, scores the institution's NBA/NAAC Tier-1 Accreditation Readiness Index (0–100), and classifies faculty into Tenure & Promotion tiers: Promotion to Professor/Associate Professor (>=85), Merit Increment (75–84), Satisfactory Renewal (65–74), and Mandatory Faculty Development Mentoring (<65). All verdicts are cryptographically signed and exportable as a master accreditation dossier.
