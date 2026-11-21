-- Faculty Appraisal Management System - Database Schema
-- Educational prototype using synthetic data only.

CREATE TABLE IF NOT EXISTS faculty (
    faculty_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    designation TEXT NOT NULL,
    email TEXT,
    joining_year INTEGER,
    academic_year TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('research', 'teaching', 'administration')),
    sub_category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    file_path TEXT,
    year INTEGER,
    status TEXT DEFAULT 'pending',
    metadata TEXT,  -- JSON string for extra fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE IF NOT EXISTS validation_results (
    validation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_id INTEGER NOT NULL,
    faculty_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('VALID', 'INVALID', 'NEEDS_REVIEW')),
    reason TEXT,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evidence_id) REFERENCES evidence(evidence_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE IF NOT EXISTS appraisal_results (
    appraisal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    academic_year TEXT NOT NULL,
    research_score REAL DEFAULT 0,
    teaching_score REAL DEFAULT 0,
    administration_score REAL DEFAULT 0,
    total_score REAL DEFAULT 0,
    max_score REAL DEFAULT 100,
    score_breakdown TEXT,  -- JSON string
    status TEXT DEFAULT 'DRAFT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    approved_by TEXT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    faculty_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    task TEXT,
    status TEXT NOT NULL CHECK(status IN ('started', 'success', 'failed', 'skipped')),
    result TEXT,  -- JSON string
    error TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    run_id TEXT NOT NULL,
    faculty_id TEXT,
    task TEXT,
    skill TEXT,
    tool_calls TEXT,  -- JSON array string
    memory_access TEXT,  -- JSON string
    mcp_calls TEXT,  -- JSON string
    result_summary TEXT,
    status TEXT NOT NULL CHECK(status IN ('success', 'failed', 'partial')),
    error TEXT,
    duration_ms INTEGER
);

CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope TEXT NOT NULL,  -- e.g. 'faculty:FAC001'
    key TEXT NOT NULL,
    value TEXT NOT NULL,  -- JSON string
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scope, key)
);
