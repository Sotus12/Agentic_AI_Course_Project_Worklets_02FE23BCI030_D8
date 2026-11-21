"""
OpenCLA/OpenClaw-style Agent Runtime (Lab 6)
Generic, domain-agnostic execution runtime managing skill selection,
tool execution permissions, scoped memory, and audit logging.
Contains ZERO hard-coded faculty appraisal logic. Reusable across any domain.
"""
import time
import uuid
from typing import Dict, Any, Optional

from app.runtime.skill_registry import SkillRegistry
from app.runtime.tool_registry import ToolRegistry
from app.runtime.memory import ScopedMemory
from app.runtime.audit import AuditLogger
from app.mcp.client import MCPClient


class AgentRuntime:
    """
    OpenCLA/OpenClaw-style Runtime Engine.

    Workflow:
    1. receive_task() -> accepts task description & payload
    2. select_skill() -> identifies matching skill from registry
    3. loads skill & allowed tools
    4. executes skill within scoped memory
    5. writes structured audit log
    6. records failures gracefully
    """

    def __init__(
        self,
        skill_registry: Optional[SkillRegistry] = None,
        tool_registry: Optional[ToolRegistry] = None,
        memory: Optional[ScopedMemory] = None,
        audit_logger: Optional[AuditLogger] = None,
        mcp_client: Optional[MCPClient] = None,
    ):
        self.skill_registry = skill_registry or SkillRegistry()
        self.tool_registry = tool_registry or ToolRegistry()
        self.memory = memory or ScopedMemory()
        self.audit = audit_logger or AuditLogger()
        self.mcp_client = mcp_client or MCPClient()

    def select_skill(self, task_description: str) -> Optional[str]:
        """Dynamically select appropriate skill from registry."""
        return self.skill_registry.select_skill(task_description)

    def receive_task(
        self,
        task_description: str,
        task_input: Dict[str, Any],
        run_id: Optional[str] = None,
        faculty_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Primary entrypoint: receives a user or agent task, resolves skill, and executes it.
        """
        run_id = run_id or f"RUN-{uuid.uuid4().hex[:8].upper()}"

        # 1. Dynamic Skill Selection via Registry
        selected_skill_name = self.select_skill(task_description)

        if not selected_skill_name:
            err_msg = f"No registered skill found matching task: '{task_description}'"
            self.audit.log(
                run_id=run_id,
                task=task_description,
                status="failed",
                faculty_id=faculty_id,
                skill=None,
                error=err_msg,
                duration_ms=0,
            )
            return {
                "run_id": run_id,
                "status": "failed",
                "error": err_msg,
                "skill": None,
            }

        # 2. Delegate to run_task
        return self.run_task(
            skill_name=selected_skill_name,
            task_input=task_input,
            run_id=run_id,
            faculty_id=faculty_id,
            task_description=task_description,
        )

    def run_task(
        self,
        skill_name: str,
        task_input: Dict[str, Any],
        run_id: str,
        faculty_id: Optional[str] = None,
        task_description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes a registered skill with sandboxed tool execution, scoped memory, and audit logging.
        """
        task_desc = task_description or f"Execute skill {skill_name}"
        start_time = time.time()

        # 1. Fetch skill class from registry
        skill_cls = self.skill_registry.get(skill_name)
        if not skill_cls:
            err_msg = f"Skill '{skill_name}' is not registered in SKILL_REGISTRY."
            self.audit.log(
                run_id=run_id,
                task=task_desc,
                status="failed",
                faculty_id=faculty_id,
                skill=skill_name,
                error=err_msg,
                duration_ms=0,
            )
            return {
                "run_id": run_id,
                "status": "failed",
                "error": err_msg,
                "skill": skill_name,
            }

        # 2. Instantiate skill
        skill_instance = skill_cls()

        # 3. Scope memory if user/faculty id provided
        scoped_mem = self.memory.scope(faculty_id) if faculty_id else None

        # 4. Execute skill with allowed tools
        try:
            execution_res = skill_instance.execute(
                task_input=task_input,
                tool_registry=self.tool_registry,
                memory=scoped_mem,
                mcp_client=self.mcp_client,
            )

            duration_ms = int((time.time() - start_time) * 1000)
            status = execution_res.get("status", "success")
            tool_traces = execution_res.get("tool_calls_trace", [])

            # 5. Record structured audit entry
            self.audit.log(
                run_id=run_id,
                task=task_desc,
                status=status,
                faculty_id=faculty_id,
                skill=skill_name,
                tool_calls=[{"tool": t.get("tool"), "status": t.get("status")} for t in tool_traces],
                result_summary=f"Skill {skill_name} completed successfully." if status == "success" else "Skill reported issue.",
                duration_ms=duration_ms,
            )

            return {
                "run_id": run_id,
                "status": status,
                "skill": skill_name,
                "result": execution_res.get("data"),
                "tool_traces": tool_traces,
                "duration_ms": duration_ms,
            }

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            err_msg = str(e)

            # Record failure in audit log
            self.audit.log(
                run_id=run_id,
                task=task_desc,
                status="failed",
                faculty_id=faculty_id,
                skill=skill_name,
                error=err_msg,
                duration_ms=duration_ms,
            )

            return {
                "run_id": run_id,
                "status": "failed",
                "skill": skill_name,
                "error": err_msg,
                "duration_ms": duration_ms,
            }
