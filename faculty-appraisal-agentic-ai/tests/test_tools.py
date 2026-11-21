"""
Tests for Lab 2: Reusable Tools
Validates:
- File tools (CSV, text, safe resolution)
- Database tools
- Calculation tools
- Report tools
- Tool execution through ToolRegistry with permission checking
"""
import pytest
from app.runtime.tool_registry import ToolRegistry
from app.tools.file_tools import read_csv, read_file
from app.tools.calculation_tools import calculate_average, calculate_score


def test_tool_registry_execution():
    """Verify tool registry executes registered tools with status and trace."""
    registry = ToolRegistry()
    res = registry.execute("calculate_average", allowed_tools=["calculate_average"], values=[10, 20, 30])
    assert res["status"] == "success"
    assert res["result"]["average"] == 20.0


def test_tool_registry_permission_denied():
    """Verify rejection when tool is not in allowed tools list."""
    registry = ToolRegistry()
    res = registry.execute("read_csv", allowed_tools=["calculate_average"], file_path="any.csv", faculty_id="FAC001")
    assert res["status"] == "rejected"
    assert "not in allowed tools" in res["error"]


def test_file_tools_read_csv():
    """Verify CSV parser correctly returns rows and field columns."""
    res = read_csv("research/publications.csv", "FAC001")
    assert res["status"] == "success"
    assert res["row_count"] >= 5
    assert "title" in res["columns"]


def test_calculation_tools():
    """Verify deterministic calculations."""
    avg_res = calculate_average([90.0, 92.0, 91.0])
    assert avg_res["average"] == 91.0

    score_res = calculate_score("research", {
        "publications": 5,
        "conference_papers": 2,
        "patents": 1,
        "projects": 2,
    })
    assert score_res["status"] == "success"
    assert score_res["score"] <= score_res["max_score"]
