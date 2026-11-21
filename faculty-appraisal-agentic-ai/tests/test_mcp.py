"""
Tests for Lab 5: MCP-Style Connector and Security Boundaries
Validates:
- Capability manifest discovery
- Authorized callers
- Read-only db_query enforcement (SELECT permitted; UPDATE/DELETE rejected)
- Directory boundary enforcement (path traversal rejected)
- Known API endpoint restrictions
"""
import pytest
from app.mcp.server import MCPServer
from app.mcp.client import MCPClient


@pytest.fixture
def mcp():
    server = MCPServer()
    client = MCPClient(server)
    return client


def test_mcp_capability_discovery(mcp):
    """Test that capabilities can be discovered dynamically."""
    caps = mcp.discover()
    assert "capabilities" in caps
    cap_names = mcp.list_capabilities()
    assert "file_read" in cap_names
    assert "db_query" in cap_names
    assert "api_get" in cap_names


def test_mcp_authorized_db_query(mcp):
    """Test authorized caller performing valid SELECT."""
    res = mcp.call(
        capability_name="db_query",
        caller="research_agent",
        inputs={"query": "SELECT faculty_id, name FROM faculty WHERE faculty_id = ?", "params": ["FAC001"]},
    )
    assert res["status"] == "success"
    assert len(res["rows"]) >= 1
    assert res["rows"][0]["faculty_id"] == "FAC001"


def test_mcp_reject_unsafe_sql_update(mcp):
    """Test rejection of unsafe SQL UPDATE query."""
    res = mcp.call(
        capability_name="db_query",
        caller="research_agent",
        inputs={"query": "UPDATE faculty SET name = 'Hacked' WHERE faculty_id = 'FAC001'", "params": []},
    )
    assert res["status"] == "rejected"
    assert "Only SELECT" in res["error"] or "Unsafe SQL" in res["error"]


def test_mcp_reject_unsafe_sql_delete(mcp):
    """Test rejection of unsafe SQL DELETE query."""
    res = mcp.call(
        capability_name="db_query",
        caller="research_agent",
        inputs={"query": "DELETE FROM faculty WHERE faculty_id = 'FAC001'", "params": []},
    )
    assert res["status"] == "rejected"
    assert "Only SELECT" in res["error"] or "Unsafe SQL" in res["error"]


def test_mcp_reject_unauthorized_caller(mcp):
    """Test rejection of unauthorized caller identity."""
    res = mcp.call(
        capability_name="db_query",
        caller="rogue_external_agent",
        inputs={"query": "SELECT * FROM faculty", "params": []},
    )
    assert res["status"] == "rejected"
    assert "Unauthorized caller" in res["error"]


def test_mcp_safe_file_read(mcp):
    """Test authorized file read within safe boundary."""
    res = mcp.call(
        capability_name="file_read",
        caller="research_agent",
        inputs={"file_path": "research/publications.csv", "faculty_id": "FAC001"},
    )
    assert res["status"] == "success"
    assert "Deep Learning" in res["content"]


def test_mcp_reject_path_traversal(mcp):
    """Test rejection of adversarial path traversal out of directory bounds."""
    res = mcp.call(
        capability_name="file_read",
        caller="research_agent",
        inputs={"file_path": "../../../etc/passwd", "faculty_id": "FAC001"},
    )
    assert res["status"] == "rejected"
    assert "outside allowed directory" in res["error"] or "Path traversal" in res["error"]


def test_mcp_known_api_endpoint(mcp):
    """Test access to known allowed API endpoint."""
    res = mcp.call(
        capability_name="api_get",
        caller="calculation_agent",
        inputs={"endpoint": "/scoring/rules"},
    )
    assert res["status"] == "success"
    assert "research" in res["data"]


def test_mcp_reject_unknown_api_endpoint(mcp):
    """Test rejection of unknown API endpoint."""
    res = mcp.call(
        capability_name="api_get",
        caller="calculation_agent",
        inputs={"endpoint": "/internal/secret/keys"},
    )
    assert res["status"] == "rejected"
    assert "Unknown endpoint" in res["error"]
