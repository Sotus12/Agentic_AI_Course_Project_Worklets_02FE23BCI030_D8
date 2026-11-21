"""
Base Agent Interface (Lab 1 & Lab 2)
Encapsulates agentic reasoning loop: PLAN -> ACT -> OBSERVE -> DECIDE.
Interacts with the OpenCLA/OpenClaw runtime and MCP capabilities.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time

from app.runtime.runtime import AgentRuntime


class BaseAgent(ABC):
    """
    Base domain agent implementing proactive reasoning and skill dispatch.
    Demonstrates true agentic workflow rather than static chatbots or simple CRUD.
    """

    def __init__(self, name: str, runtime: AgentRuntime):
        self.name = name
        self.runtime = runtime
        self.trace_steps: List[Dict[str, Any]] = []

    def record_step(self, stage: str, message: str, details: Optional[Dict[str, Any]] = None):
        """Record an explicit reasoning step for trace visibility."""
        self.trace_steps.append({
            "agent": self.name,
            "stage": stage,
            "message": message,
            "details": details or {},
            "timestamp": time.time(),
        })

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent's specific domain responsibility."""
        pass
