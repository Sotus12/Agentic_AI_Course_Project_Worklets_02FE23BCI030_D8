"""
Tool Registry (Lab 2 & Lab 6)
Central registry for reusable tools with execution tracking and parameter validation.
"""
from typing import Callable, Dict, Any, List, Optional
import time

from app.tools.file_tools import TOOLS as FILE_TOOLS
from app.tools.database_tools import TOOLS as DB_TOOLS
from app.tools.calculation_tools import TOOLS as CALC_TOOLS
from app.tools.report_tools import TOOLS as REPORT_TOOLS


class ToolRegistry:
    """Registry that holds all executable tools and tracks execution."""

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register all default tools across file, database, calculation, and report modules."""
        for tool_set in [FILE_TOOLS, DB_TOOLS, CALC_TOOLS, REPORT_TOOLS]:
            for name, meta in tool_set.items():
                self.register(
                    name=name,
                    func=meta["function"],
                    description=meta.get("description", ""),
                    inputs=meta.get("inputs", []),
                )

    def register(self, name: str, func: Callable, description: str = "", inputs: Optional[List[str]] = None):
        """Register a new tool dynamically."""
        self._tools[name] = {
            "function": func,
            "description": description,
            "inputs": inputs or [],
        }

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve tool metadata."""
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())

    def execute(self, tool_name: str, allowed_tools: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Execute a registered tool with security boundary and audit tracing.

        Args:
            tool_name: Name of the tool to execute.
            allowed_tools: Optional list of tools permitted for the active caller/skill.
            **kwargs: Arguments to pass to the tool.

        Returns:
            Dict containing tool execution result, duration, and status.
        """
        start_time = time.time()

        if tool_name not in self._tools:
            return {
                "tool": tool_name,
                "status": "error",
                "error": f"Tool '{tool_name}' is not registered.",
                "duration_ms": 0,
            }

        if allowed_tools is not None and tool_name not in allowed_tools:
            return {
                "tool": tool_name,
                "status": "rejected",
                "error": f"Tool '{tool_name}' is not in allowed tools for this context: {allowed_tools}",
                "duration_ms": 0,
            }

        tool_meta = self._tools[tool_name]
        func = tool_meta["function"]

        try:
            result = func(**kwargs)
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "tool": tool_name,
                "status": "success" if not (isinstance(result, dict) and result.get("status") == "error") else "error",
                "result": result,
                "duration_ms": duration_ms,
            }
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "tool": tool_name,
                "status": "error",
                "error": str(e),
                "duration_ms": duration_ms,
            }
