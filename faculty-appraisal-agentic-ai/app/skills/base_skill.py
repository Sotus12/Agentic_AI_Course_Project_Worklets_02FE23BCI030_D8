"""
Base Skill Interface (Lab 3)
All skills implement this interface to be registered and executed by the OpenCLA/OpenClaw runtime.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseSkill(ABC):
    """Abstract Base Class for modular, registry-based skills."""

    name: str = "base_skill"
    description: str = "Base skill description"
    version: str = "1.0"
    allowed_tools: List[str] = []

    @abstractmethod
    def execute(self, task_input: Dict[str, Any], tool_registry, memory, **kwargs) -> Dict[str, Any]:
        """
        Execute skill workflow.

        Args:
            task_input: Input parameters for the task.
            tool_registry: ToolRegistry instance to invoke tools.
            memory: ScopedMemory instance for reading/writing memory.

        Returns:
            Structured result dictionary.
        """
        pass
