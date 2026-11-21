# Lab 4: Memory & Scoped Retrieval

## 1. Why Scoped Structured Memory (No Vector Database)?

In educational faculty appraisal management, records (such as publications, courses, and scores) are **structured, deterministic entities**. Introducing vector databases, embeddings, or semantic search for Labs 1–6 would introduce unnecessary complexity, token cost, and potential hallucinations.

Instead, the system utilizes a **scoped persistent key-value store backed by SQLite** with JSON serialization.

---

## 2. Memory Structure & Schema

The underlying SQLite table isolates memory namespaces:

```sql
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope TEXT NOT NULL,       -- e.g. 'faculty:FAC001'
    key TEXT NOT NULL,         -- e.g. 'profile', 'current_appraisal_result'
    value TEXT NOT NULL,       -- Structured JSON payload
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scope, key)
);
```

---

## 3. Scoped Isolation (Preventing Data Leaks)

Each faculty context is segregated using `memory.scope(user_id)`:

```python
memory_sys = ScopedMemory()

# Scope for Faculty 001
mem_fac1 = memory_sys.scope("FAC001")
mem_fac1.set("profile", {"name": "Dr. Ananya Rao", "department": "AI"})
mem_fac1.set("current_score", 94.0)

# Scope for Faculty 002
mem_fac2 = memory_sys.scope("FAC002")
mem_fac2.set("current_score", 76.5)

# Verification:
assert mem_fac1.get("current_score") == 94.0
assert mem_fac2.get("current_score") == 76.5
assert mem_fac2.get("profile") is None  # Zero cross-contamination!
```

---

## 4. Key Memory Categories

1. **Faculty Profile Memory (`profile`):** Name, ID, designation, department, joining date.
2. **Current Appraisal State (`current_appraisal_result`):** Intermediate and finalized category scores, evidence item counts, and status flags.
3. **Previous Appraisal Memory (`previous_appraisal`):** Past academic year results (e.g. 2025-26 score = 74/100) used for automated comparative analysis in reports:
   - *Previous Score:* 74.0
   - *Current Score:* 94.0
   - *Delta:* +20.0 points
