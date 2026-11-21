# Lab 2: Tool-Using Agents & Tool Registry

## 1. Overview of Tools

Agents in this project do not directly manipulate SQLite databases or the host filesystem. Instead, all operations are brokered through **auditable, permission-gated tools** managed by `ToolRegistry`.

---

## 2. Tool Inventory

### A. File Tools (`app/tools/file_tools.py`)
- `read_file(file_path, faculty_id)`: Safely reads text documents within faculty boundary.
- `read_pdf(file_path, faculty_id)`: Extracts text content from evidence PDF files.
- `read_csv(file_path, faculty_id)`: Parses CSV spreadsheets into structured dictionaries.
- `read_xlsx(file_path, faculty_id)`: Parses Excel spreadsheets using pandas/openpyxl.

### B. Database Tools (`app/tools/database_tools.py`)
- `query_faculty_data(faculty_id)`: Fetches faculty bio and department data.
- `get_evidence(faculty_id, category)`: Queries evidence items from SQLite.
- `get_validation_results(faculty_id, run_id)`: Retrieves validation records for run.
- `save_validation_result(evidence_id, faculty_id, run_id, status, reason)`: Records validation outcome.
- `save_appraisal_result(...)`: Persists calculated scores and JSON breakdowns.
- `get_previous_appraisal(faculty_id)`: Fetches historical session scores for comparative analysis.

### C. Calculation Tools (`app/tools/calculation_tools.py`)
- `calculate_average(values)`: Computes deterministic arithmetic means.
- `calculate_score(category, evidence_data)`: Computes category scores using `config/scoring_rules.json`.

### D. Report Tools (`app/tools/report_tools.py`)
- `generate_pdf(report_data, faculty_id, run_id)`: Compiles formatted formal PDF appraisal document.
- `generate_json(report_data, faculty_id, run_id)`: Generates full structured JSON artifact.

---

## 3. Sample Auditable Tool Trace

During execution of the `research_appraisal` skill, the following tool trace is recorded:

```json
[
  {
    "tool": "read_csv",
    "status": "success",
    "inputs": {"file_path": "research/publications.csv", "faculty_id": "FAC001"},
    "duration_ms": 2
  },
  {
    "tool": "read_csv",
    "status": "success",
    "inputs": {"file_path": "research/patents.csv", "faculty_id": "FAC001"},
    "duration_ms": 1
  },
  {
    "tool": "get_evidence",
    "status": "success",
    "inputs": {"faculty_id": "FAC001", "category": "research"},
    "duration_ms": 3
  }
]
```

## 4. Permission Gating
Each skill specifies its `allowed_tools` list. If a skill attempts to invoke a tool outside its allowed list, the `ToolRegistry` rejects the call:
```python
res = tool_registry.execute("drop_table", allowed_tools=["read_csv"])
# Result: {"status": "rejected", "error": "Tool 'drop_table' is not in allowed tools..."}
```
