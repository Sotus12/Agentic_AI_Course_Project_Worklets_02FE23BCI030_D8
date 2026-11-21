# Lab 6: OpenCLA / OpenClaw-Style Agent Runtime

## 1. Runtime Architecture

The runtime engine (`AgentRuntime`) is a **generic, domain-agnostic execution kernel**. It contains zero hard-coded faculty appraisal logic and can be repurposed for other agentic applications without architectural changes.

```text
receive_task(task_description, task_input)
    |
    v
select_skill(task_description)  <--->  SKILL_REGISTRY
    |
    v
Instantiate Skill & Resolve Allowed Tools  <--->  ToolRegistry
    |
    v
Execute Skill Workflow  <--->  ScopedMemory (Isolation)
    |
    v
Record Structured Audit Log  <--->  audit_logs (SQLite)
    |
    v
Return Structured Result (or gracefully record Failure)
```

---

## 2. Core Execution Methods

1. `receive_task(task_description, task_input, run_id, faculty_id)`:
   The single entry point. Queries `select_skill()` and delegates to `run_task()`.
2. `select_skill(task_description)`:
   Resolves intent against registered skill metadata without hard-coded conditional ladders.
3. `run_task(skill_name, task_input, run_id, faculty_id)`:
   Instantiates the skill, validates tool permissions, connects scoped memory, logs duration, catches exceptions, and persists audit logs.

---

## 3. Demonstration 1: Successful Execution Run

When a recognized task is received:
```python
result = runtime.receive_task(
    task_description="Execute research_appraisal data collection",
    task_input={"faculty_id": "FAC001"},
    faculty_id="FAC001"
)
```
- **Result:** Status `success`, skill `research_appraisal` executed, 5 publications gathered.
- **Audit Record:**
  ```json
  {
    "run_id": "RUN-ABC123",
    "task": "Execute research_appraisal data collection",
    "skill": "research_appraisal",
    "status": "success",
    "tool_calls": [{"tool": "read_csv", "status": "success"}, {"tool": "get_evidence", "status": "success"}],
    "duration_ms": 14
  }
  ```

---

## 4. Demonstration 2: Gracefully Recorded Failure Run

When an unrecognizable or invalid task is received:
```python
result = runtime.receive_task(
    task_description="Perform quantum computing trajectory prediction",
    task_input={},
    faculty_id="FAC001"
)
```
- **Result:** Status `failed`, error message generated.
- **Audit Record:**
  ```json
  {
    "run_id": "RUN-FAIL001",
    "task": "Perform quantum computing trajectory prediction",
    "skill": null,
    "status": "failed",
    "error": "No registered skill found matching task: 'Perform quantum computing trajectory prediction'",
    "duration_ms": 0
  }
  ```

---

## 5. Demonstration 3: Adding a New Skill Without Modifying Runtime Core

The instructor specifically evaluates:
> *"Can the runtime add a new skill without code rewrite?"*

We demonstrate this programmatically in `tests/test_runtime.py`:

```python
# 1. Define a brand-new skill
class CustomPatentAnalysisSkill(BaseSkill):
    name = "custom_patent_analysis"
    description = "Analyze novel patent submissions for international filings"
    allowed_tools = ["read_csv"]

    def execute(self, task_input, tool_registry, memory, **kwargs):
        return {"status": "success", "data": {"evaluated_patents": 3}}

# 2. Register it with the existing registry
skill_registry.register(CustomPatentAnalysisSkill)

# 3. Execute via runtime.receive_task()
# ZERO lines of AgentRuntime or its routing code were modified!
res = runtime.receive_task("Run custom_patent_analysis", {"patents_count": 3})
assert res["status"] == "success"
assert res["skill"] == "custom_patent_analysis"
```
