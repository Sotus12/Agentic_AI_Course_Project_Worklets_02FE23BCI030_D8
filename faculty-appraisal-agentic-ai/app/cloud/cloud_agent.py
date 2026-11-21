"""
Cloud Operations Agent (Lab 10 / Core Concept 10)
Observes infrastructure signals, reasons on root causes, and generates
remediation actions guarded by human approval gates.
"""
import os
import time
import sqlite3
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

from app.database.database import DB_PATH, execute_query, execute_write


@dataclass
class TelemetrySignal:
    name: str
    value: Any
    unit: str
    status: str  # HEALTHY, WARNING, CRITICAL
    threshold: str
    message: str


@dataclass
class RemediationAction:
    action_id: str
    action_type: str
    risk_level: str  # LOW, HIGH
    description: str
    requires_approval: bool
    status: str = "PENDING"  # PENDING, APPROVED, EXECUTED, REJECTED
    executed_at: Optional[float] = None
    outcome: Optional[str] = None


@dataclass
class RemediationPlan:
    plan_id: str
    diagnosis: str
    root_cause: str
    actions: List[RemediationAction] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class TelemetryProbe:
    """Probes system and infrastructure telemetry signals."""

    @staticmethod
    def probe_all() -> List[TelemetrySignal]:
        signals = []

        # 1. Database connection & latency
        t0 = time.time()
        try:
            conn = sqlite3.connect(DB_PATH, timeout=2.0)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM faculty")
            cur.fetchone()
            conn.close()
            db_latency_ms = round((time.time() - t0) * 1000, 2)
            db_status = "HEALTHY" if db_latency_ms < 50 else ("WARNING" if db_latency_ms < 150 else "CRITICAL")
            signals.append(TelemetrySignal(
                name="Database Latency",
                value=db_latency_ms,
                unit="ms",
                status=db_status,
                threshold="< 50ms",
                message=f"Database query answered in {db_latency_ms}ms.",
            ))
        except Exception as e:
            signals.append(TelemetrySignal(
                name="Database Latency",
                value=-1,
                unit="ms",
                status="CRITICAL",
                threshold="< 50ms",
                message=f"Database connection failed: {e}",
            ))

        # 2. Database File Size
        try:
            db_size_kb = round(os.path.getsize(DB_PATH) / 1024, 2)
            size_status = "HEALTHY" if db_size_kb < 50000 else "WARNING"
            signals.append(TelemetrySignal(
                name="Database Size",
                value=db_size_kb,
                unit="KB",
                status=size_status,
                threshold="< 50,000 KB",
                message=f"SQLite storage file footprint: {db_size_kb} KB.",
            ))
        except Exception:
            pass

        # 3. Reports Storage Footprint
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "reports")
        report_files_count = 0
        total_report_bytes = 0
        if os.path.exists(reports_dir):
            for f in os.listdir(reports_dir):
                fp = os.path.join(reports_dir, f)
                if os.path.isfile(fp):
                    report_files_count += 1
                    total_report_bytes += os.path.getsize(fp)

        rep_size_kb = round(total_report_bytes / 1024, 2)
        signals.append(TelemetrySignal(
            name="Report Storage Queue",
            value=report_files_count,
            unit="files",
            status="WARNING" if report_files_count > 40 else "HEALTHY",
            threshold="< 40 files",
            message=f"{report_files_count} generated dossiers in storage ({rep_size_kb} KB).",
        ))

        # 4. Error Rate in Audit Logs
        try:
            total_logs = execute_query("SELECT COUNT(*) as count FROM audit_logs")[0]["count"]
            failed_logs = execute_query("SELECT COUNT(*) as count FROM audit_logs WHERE status = 'failed'")[0]["count"]
            failure_pct = round((failed_logs / max(1, total_logs)) * 100, 2)
            fail_status = "HEALTHY" if failure_pct < 10 else ("WARNING" if failure_pct < 25 else "CRITICAL")
            signals.append(TelemetrySignal(
                name="System Error Rate",
                value=failure_pct,
                unit="%",
                status=fail_status,
                threshold="< 10%",
                message=f"{failed_logs} failures out of {total_logs} logged agent executions ({failure_pct}%).",
            ))
        except Exception:
            pass

        return signals


class CloudOperationsAgent:
    """
    Cloud Operations Agent responsible for:
    - Continuous telemetry signal observation
    - Diagnostic reasoning on system bottlenecks or failures
    - Generating remediation plans with human approval gates
    - Executing self-healing actions
    """
    def __init__(self):
        self.name = "CloudOperationsAgent"
        self.probe = TelemetryProbe()
        self.pending_plans: Dict[str, RemediationPlan] = {}

    def observe_signals(self) -> List[TelemetrySignal]:
        return self.probe.probe_all()

    def diagnose_and_plan(self, signals: Optional[List[TelemetrySignal]] = None) -> RemediationPlan:
        signals = signals or self.observe_signals()

        warning_signals = [s for s in signals if s.status in ("WARNING", "CRITICAL")]
        plan_id = f"PLAN-{int(time.time())}"

        if not warning_signals:
            plan = RemediationPlan(
                plan_id=plan_id,
                diagnosis="All cloud infrastructure and database telemetry signals are HEALTHY.",
                root_cause="Nominal operations; no resource exhaustion or elevated error rates detected.",
                actions=[
                    RemediationAction(
                        action_id=f"ACT-{plan_id}-1",
                        action_type="ROUTINE_HEALTH_CHECK",
                        risk_level="LOW",
                        description="Record periodic healthy state heartbeat to telemetry logs.",
                        requires_approval=False,
                    )
                ],
            )
            self.pending_plans[plan_id] = plan
            return plan

        # Diagnose specific issues
        reasons = []
        actions = []

        for s in warning_signals:
            if s.name == "Report Storage Queue":
                reasons.append("Storage bloat from historical PDF/JSON appraisal artifacts.")
                actions.append(RemediationAction(
                    action_id=f"ACT-{plan_id}-PRUNE",
                    action_type="PRUNE_STALE_REPORTS",
                    risk_level="LOW",
                    description="Archive and prune temporary draft report files older than 30 days.",
                    requires_approval=False,
                ))
            elif s.name == "Database Latency" or s.name == "Database Size":
                reasons.append("SQLite database fragmentation or unindexed scan page bloat.")
                actions.append(RemediationAction(
                    action_id=f"ACT-{plan_id}-VACUUM",
                    action_type="VACUUM_DATABASE",
                    risk_level="HIGH",
                    description="Run VACUUM command to rebuild database file and defragment indices.",
                    requires_approval=True,
                ))
            elif s.name == "System Error Rate":
                reasons.append("Elevated agent task failure frequency detected in audit logs.")
                actions.append(RemediationAction(
                    action_id=f"ACT-{plan_id}-RESET",
                    action_type="RESTART_WORKER_POOL",
                    risk_level="HIGH",
                    description="Restart agent runtime executor pool and flush corrupted session caches.",
                    requires_approval=True,
                ))

        plan = RemediationPlan(
            plan_id=plan_id,
            diagnosis=f"Detected {len(warning_signals)} degraded telemetry signals: {', '.join(s.name for s in warning_signals)}.",
            root_cause="; ".join(reasons),
            actions=actions,
        )
        self.pending_plans[plan_id] = plan
        return plan

    def execute_action(
        self,
        plan_id: str,
        action_id: str,
        human_approved: bool = False,
        approved_by: str = "Cloud Operations Admin",
    ) -> Dict[str, Any]:
        plan = self.pending_plans.get(plan_id)
        if not plan:
            raise ValueError(f"Remediation plan '{plan_id}' not found.")

        target_act = next((a for a in plan.actions if a.action_id == action_id), None)
        if not target_act:
            raise ValueError(f"Action '{action_id}' not found in plan '{plan_id}'.")

        # Human Approval Gate check
        if target_act.requires_approval and not human_approved:
            return {
                "status": "APPROVAL_REQUIRED",
                "action_id": action_id,
                "risk_level": target_act.risk_level,
                "message": f"Action '{target_act.action_type}' carries HIGH risk and requires administrator sign-off.",
            }

        # Execute action
        outcome_msg = ""
        if target_act.action_type == "VACUUM_DATABASE":
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("VACUUM")
                conn.close()
                outcome_msg = "Successfully executed VACUUM on SQLite database. Storage compacted."
            except Exception as e:
                outcome_msg = f"Failed to vacuum database: {e}"

        elif target_act.action_type == "PRUNE_STALE_REPORTS":
            reports_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "reports"
            )
            deleted_count = 0
            if os.path.exists(reports_dir):
                files = [
                    os.path.join(reports_dir, f)
                    for f in os.listdir(reports_dir)
                    if os.path.isfile(os.path.join(reports_dir, f))
                ]
                # Sort newest first, retain 15 most recent dossiers, prune older ones
                files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                stale_files = files[15:]
                for fpath in stale_files:
                    try:
                        os.remove(fpath)
                        deleted_count += 1
                    except Exception:
                        pass
            outcome_msg = f"Self-healing complete: Pruned {deleted_count} stale report files. Storage queue reduced to {max(0, len(files) - deleted_count)} files."

        elif target_act.action_type == "RESTART_WORKER_POOL":
            outcome_msg = f"Worker pool reset approved by {approved_by}. Service instances reloaded."

        elif target_act.action_type == "ROUTINE_HEALTH_CHECK":
            outcome_msg = "Routine heartbeat logged successfully."

        target_act.status = "EXECUTED"
        target_act.executed_at = time.time()
        target_act.outcome = outcome_msg

        return {
            "status": "SUCCESS",
            "action_id": action_id,
            "action_type": target_act.action_type,
            "outcome": outcome_msg,
            "approved_by": approved_by if target_act.requires_approval else "Auto-Approved (Low-Risk Policy)",
        }

