"""
MCP Capabilities Manifest (Lab 5)
Defines the discoverable capabilities exposed by the MCP server.
"""

CAPABILITIES = {
    "capabilities": [
        {
            "name": "file_read",
            "kind": "resource",
            "description": "Read evidence files from the faculty data directory",
            "input": {
                "file_path": {"type": "string", "description": "Relative path within faculty directory"},
                "faculty_id": {"type": "string", "description": "Faculty identifier"}
            },
            "output": {
                "status": {"type": "string"},
                "content": {"type": "string"},
                "path": {"type": "string"}
            },
            "allowed_callers": [
                "research_agent", "teaching_agent", "administration_agent",
                "validation_agent", "calculation_agent", "report_agent"
            ]
        },
        {
            "name": "db_query",
            "kind": "tool",
            "description": "Execute a read-only SQL query on the appraisal database",
            "input": {
                "query": {"type": "string", "description": "SQL SELECT query"},
                "params": {"type": "array", "description": "Query parameters"}
            },
            "output": {
                "status": {"type": "string"},
                "rows": {"type": "array"},
                "row_count": {"type": "integer"}
            },
            "allowed_callers": [
                "research_agent", "teaching_agent", "administration_agent",
                "validation_agent", "calculation_agent", "report_agent"
            ],
            "constraints": ["SELECT only — UPDATE, DELETE, DROP, INSERT, ALTER are rejected"]
        },
        {
            "name": "api_get",
            "kind": "tool",
            "description": "Access safe local API endpoints for faculty and scoring data",
            "input": {
                "endpoint": {"type": "string", "description": "API endpoint path"},
                "params": {"type": "object", "description": "Optional query parameters"}
            },
            "output": {
                "status": {"type": "string"},
                "data": {"type": "object"}
            },
            "allowed_callers": [
                "research_agent", "teaching_agent", "administration_agent",
                "validation_agent", "calculation_agent", "report_agent"
            ],
            "known_endpoints": [
                "/faculty/{faculty_id}",
                "/scoring/rules",
                "/appraisal/{faculty_id}/previous"
            ]
        }
    ]
}
