"""
MCP Server (Lab 5)
Simplified educational MCP-style server exposing discoverable capabilities.
Implements: file_read, db_query, api_get with security enforcement.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.mcp.capabilities import CAPABILITIES
from app.mcp.security import (
    check_caller, check_sql_safety, check_file_path_safety, check_endpoint
)
from app.database.database import execute_query
from app.tools.file_tools import read_file as _read_file


class MCPServer:
    """
    Simplified MCP-style server.
    Exposes a discoverable CAPABILITIES manifest.
    Client discovers capabilities rather than hard-coding names.
    """

    def __init__(self):
        self._capabilities = CAPABILITIES
        self._handlers = {
            "file_read": self._handle_file_read,
            "db_query": self._handle_db_query,
            "api_get": self._handle_api_get,
        }

    def discover(self) -> dict:
        """
        Return the capabilities manifest for client discovery.
        The client uses this to learn what the server can do.
        """
        return self._capabilities

    def call(self, capability_name: str, caller: str, inputs: dict) -> dict:
        """
        Call a capability by name.

        Args:
            capability_name: Name of the capability to invoke
            caller: Identity of the calling agent
            inputs: Structured inputs for the capability

        Returns:
            Structured response dict
        """
        # 1. Check capability exists
        cap = self._find_capability(capability_name)
        if not cap:
            return {
                "status": "rejected",
                "error": f"Unknown capability: '{capability_name}'. "
                         f"Available: {[c['name'] for c in self._capabilities['capabilities']]}"
            }

        # 2. Check caller authorization
        auth = check_caller(caller)
        if not auth["authorized"]:
            return {"status": "rejected", "error": auth["error"]}

        # 3. Check caller is in this capability's allowed list
        allowed = cap.get("allowed_callers", [])
        if allowed and caller not in allowed:
            return {
                "status": "rejected",
                "error": f"Caller '{caller}' is not allowed for capability '{capability_name}'. "
                         f"Allowed: {allowed}"
            }

        # 4. Dispatch to handler
        handler = self._handlers.get(capability_name)
        if not handler:
            return {"status": "error", "error": f"No handler for capability '{capability_name}'"}

        return handler(inputs)

    def _find_capability(self, name: str) -> dict:
        """Find a capability by name in the manifest."""
        for cap in self._capabilities["capabilities"]:
            if cap["name"] == name:
                return cap
        return None

    def _handle_file_read(self, inputs: dict) -> dict:
        """Handle file_read capability — reads evidence files safely."""
        file_path = inputs.get("file_path", "")
        faculty_id = inputs.get("faculty_id", "")

        if not file_path or not faculty_id:
            return {"status": "error", "error": "file_path and faculty_id are required"}

        # Check path safety
        safety = check_file_path_safety(file_path, faculty_id)
        if not safety["safe"]:
            return {"status": "rejected", "error": safety["error"]}

        # Read the file
        return _read_file(file_path, faculty_id)

    def _handle_db_query(self, inputs: dict) -> dict:
        """Handle db_query capability — SELECT-only database access."""
        query = inputs.get("query", "")
        params = inputs.get("params", [])

        if not query:
            return {"status": "error", "error": "query is required"}

        # Check SQL safety
        safety = check_sql_safety(query)
        if not safety["safe"]:
            return {"status": "rejected", "error": safety["error"]}

        # Execute query
        try:
            rows = execute_query(query, tuple(params))
            return {"status": "success", "rows": rows, "row_count": len(rows)}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _handle_api_get(self, inputs: dict) -> dict:
        """Handle api_get capability — safe local API endpoints."""
        endpoint = inputs.get("endpoint", "")

        if not endpoint:
            return {"status": "error", "error": "endpoint is required"}

        # Check endpoint is known
        ep_check = check_endpoint(endpoint)
        if not ep_check["known"]:
            return {"status": "rejected", "error": ep_check["error"]}

        # Route to internal data
        try:
            return self._route_api(endpoint)
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _route_api(self, endpoint: str) -> dict:
        """Route API endpoint to internal data retrieval."""
        parts = endpoint.strip("/").split("/")

        # /faculty/{faculty_id}
        if len(parts) == 2 and parts[0] == "faculty":
            faculty_id = parts[1]
            rows = execute_query("SELECT * FROM faculty WHERE faculty_id = ?", (faculty_id,))
            if rows:
                return {"status": "success", "data": rows[0]}
            return {"status": "error", "error": f"Faculty {faculty_id} not found"}

        # /scoring/rules
        if parts == ["scoring", "rules"]:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "config", "scoring_rules.json"
            )
            with open(config_path, "r") as f:
                rules = json.load(f)
            return {"status": "success", "data": rules}

        # /appraisal/{faculty_id}/previous
        if len(parts) == 3 and parts[0] == "appraisal" and parts[2] == "previous":
            faculty_id = parts[1]
            rows = execute_query(
                "SELECT * FROM appraisal_results WHERE faculty_id = ? ORDER BY created_at DESC LIMIT 1",
                (faculty_id,)
            )
            if rows:
                result = dict(rows[0])
                if result.get("score_breakdown"):
                    result["score_breakdown"] = json.loads(result["score_breakdown"])
                return {"status": "success", "data": result}
            return {"status": "success", "data": None, "message": "No previous appraisal"}

        return {"status": "error", "error": f"Unhandled endpoint: {endpoint}"}
