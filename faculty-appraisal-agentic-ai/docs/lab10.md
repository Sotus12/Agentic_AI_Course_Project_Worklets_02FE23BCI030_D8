# Lab 10: Cloud Operations Agent

## 1. Concept Overview
A **Cloud Operations Agent** monitors live infrastructure signals, diagnoses failure signatures using root-cause analysis, and formulates remediation actions guarded by human approval gates.

## 2. Implementation in Team 8 (Faculty Appraisal)
In `app/cloud/cloud_agent.py`:
- **TelemetryProbe:** Gathers live infrastructure telemetry:
  - SQLite query response latency (ms).
  - Database file size footprint (KB).
  - Report dossier storage accumulation count.
  - Runtime audit log failure rate (%).
- **CloudOperationsAgent:**
  - **Diagnostic Engine:** Correlates warning signals to root causes (e.g., storage bloat, index fragmentation, elevated failure frequencies).
  - **Remediation Plans:** Proposes actionable self-healing procedures (`VACUUM_DATABASE`, `PRUNE_STALE_REPORTS`, `RESTART_WORKER_POOL`).
  - **Approval Gates:** Low-risk operations can execute autonomously; high-risk operations (e.g. database defragmentation, worker restart) pause for administrator sign-off.

## 3. Verification & Testing
Run via CLI:
```bash
python run.py cloud
```
Or via pytest:
```bash
pytest tests/test_concepts_7_to_12.py -k test_cloud_agent
```

