"""
MCP Security Module (Lab 5)
Enforces allowed callers, safe SQL, safe file paths, and known endpoints.
"""
import re
import os

# Allowed callers for MCP capabilities
ALLOWED_CALLERS = {
    "research_agent",
    "teaching_agent",
    "administration_agent",
    "validation_agent",
    "calculation_agent",
    "report_agent",
}

# Unsafe SQL patterns
UNSAFE_SQL_PATTERNS = re.compile(
    r"\b(UPDATE|DELETE|DROP|INSERT|ALTER|TRUNCATE|CREATE|REPLACE|EXEC|EXECUTE|GRANT|REVOKE)\b",
    re.IGNORECASE
)

# Known API endpoints (patterns)
KNOWN_ENDPOINTS = [
    r"^/faculty/[A-Za-z0-9]+$",
    r"^/scoring/rules$",
    r"^/appraisal/[A-Za-z0-9]+/previous$",
]

# Safe base directory for file_read
SAFE_BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "faculty"
)


def check_caller(caller: str) -> dict:
    """Check if a caller is authorized to use MCP capabilities."""
    if caller in ALLOWED_CALLERS:
        return {"authorized": True}
    return {
        "authorized": False,
        "error": f"Unauthorized caller: '{caller}'. Allowed callers: {sorted(ALLOWED_CALLERS)}"
    }


def check_sql_safety(query: str) -> dict:
    """Check if a SQL query is safe (SELECT only)."""
    stripped = query.strip()
    if not stripped.upper().startswith("SELECT"):
        return {"safe": False, "error": f"Only SELECT queries are allowed. Rejected: {stripped[:50]}"}
    if UNSAFE_SQL_PATTERNS.search(stripped):
        # Find which unsafe keyword was matched
        match = UNSAFE_SQL_PATTERNS.search(stripped)
        return {"safe": False, "error": f"Unsafe SQL operation detected: {match.group()}. Only SELECT is allowed."}
    return {"safe": True}


def check_file_path_safety(file_path: str, faculty_id: str) -> dict:
    """Check if a file path is within the safe directory boundary."""
    base = os.path.join(SAFE_BASE_DIR, faculty_id)
    full = os.path.normpath(os.path.join(base, file_path))
    if not full.startswith(os.path.normpath(base)):
        return {
            "safe": False,
            "error": f"Path traversal rejected: '{file_path}' resolves outside allowed directory for {faculty_id}"
        }
    return {"safe": True, "resolved_path": full}


def check_endpoint(endpoint: str) -> dict:
    """Check if an API endpoint is in the known endpoints list."""
    for pattern in KNOWN_ENDPOINTS:
        if re.match(pattern, endpoint):
            return {"known": True}
    return {
        "known": False,
        "error": f"Unknown endpoint: '{endpoint}'. Known endpoints: {[p.replace(chr(92), '') for p in KNOWN_ENDPOINTS]}"
    }
