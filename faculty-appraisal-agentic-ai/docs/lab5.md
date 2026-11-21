# Lab 5: Model Context Protocol (MCP) Style Connector

## 1. Overview of the Educational MCP Pattern

Following the course Lab 5 reference, the project implements a simplified Model Context Protocol (MCP) connector layer.

The architecture decouples clients from hard-coded server operations through **dynamic capability discovery**, structured payloads, and strict security guards.

```text
MCP Server
    |
    +-- Capabilities Manifest (Discoverable)
    +-- Security Guard (Callers, SELECT-only, Directory Boundary, Known Endpoints)
    |
    +-- file_read
    +-- db_query
    +-- api_get
```

---

## 2. Capabilities Manifest (`app/mcp/capabilities.py`)

The MCP Server exposes a discoverable manifest:

```json
{
  "capabilities": [
    {
      "name": "file_read",
      "kind": "resource",
      "description": "Read evidence files from the faculty data directory",
      "allowed_callers": ["research_agent", "teaching_agent", "..."],
      "input": {"file_path": {"type": "string"}, "faculty_id": {"type": "string"}}
    },
    {
      "name": "db_query",
      "kind": "tool",
      "description": "Execute a read-only SQL query on the appraisal database",
      "allowed_callers": ["research_agent", "teaching_agent", "..."],
      "constraints": ["SELECT only — UPDATE, DELETE, DROP are rejected"]
    },
    {
      "name": "api_get",
      "kind": "tool",
      "description": "Access safe local API endpoints",
      "known_endpoints": ["/faculty/{faculty_id}", "/scoring/rules", "/appraisal/{faculty_id}/previous"]
    }
  ]
}
```

---

## 3. Client Capability Discovery

The `MCPClient` does not hard-code capability addresses. It queries the server's manifest before invoking capabilities:

```python
client = MCPClient(server)
capabilities = client.discover()  # Discovers file_read, db_query, api_get
result = client.call("db_query", caller="research_agent", inputs={"query": "SELECT * FROM faculty"})
```

---

## 4. Security Enforcement & Boundary Rejection Tests

### Test 1: Authorized SELECT Query (Success)
- **Request:**
  ```json
  {"capability": "db_query", "caller": "research_agent", "query": "SELECT name FROM faculty WHERE faculty_id = 'FAC001'"}
  ```
- **Response:**
  ```json
  {"status": "success", "rows": [{"name": "Dr. Ananya Rao"}], "row_count": 1}
  ```

### Test 2: Unsafe SQL UPDATE/DELETE Rejection
- **Request:**
  ```json
  {"capability": "db_query", "caller": "research_agent", "query": "UPDATE faculty SET name = 'Attacker'"}
  ```
- **Response:**
  ```json
  {"status": "rejected", "error": "Only SELECT queries are allowed. Unsafe SQL operation detected: UPDATE."}
  ```

### Test 3: Unauthorized Caller Rejection
- **Request:**
  ```json
  {"capability": "db_query", "caller": "unauthorized_external_bot", "query": "SELECT * FROM faculty"}
  ```
- **Response:**
  ```json
  {"status": "rejected", "error": "Unauthorized caller: 'unauthorized_external_bot'."}
  ```

### Test 4: Path Traversal Attack Rejection
- **Request:**
  ```json
  {"capability": "file_read", "caller": "research_agent", "file_path": "../../../system/secret.txt", "faculty_id": "FAC001"}
  ```
- **Response:**
  ```json
  {"status": "rejected", "error": "Path traversal rejected: resolves outside allowed directory for FAC001."}
  ```

### Test 5: Unknown API Endpoint Rejection
- **Request:**
  ```json
  {"capability": "api_get", "caller": "research_agent", "endpoint": "/admin/delete_all"}
  ```
- **Response:**
  ```json
  {"status": "rejected", "error": "Unknown endpoint: '/admin/delete_all'."}
  ```
