---
name: evidence_validation
description: Validate evidence items for completeness, readability, and duplicates
version: "1.0"
---

# Evidence Validation Skill

## Purpose
Validate all collected evidence items, checking file existence, readability, required information, and duplicates.

## Inputs
- `faculty_id` (str): The faculty identifier
- `run_id` (str): The current appraisal run ID
- `evidence_items` (list): List of evidence records to validate

## Workflow
1. For each evidence item:
   a. Check if file_path exists and is readable (if provided)
   b. Check required fields are present (title, description)
   c. Check for duplicate evidence (same title + category)
   d. Determine status: VALID, INVALID, or NEEDS_REVIEW
   e. Record reason for the status
2. Save validation results to database
3. Return validation summary

## Allowed Tools
- `read_file`
- `read_pdf`
- `get_evidence`
- `save_validation_result`

## Expected Output
```json
{
  "faculty_id": "FAC001",
  "run_id": "APP-2026-001",
  "total": 19,
  "valid": 15,
  "invalid": 2,
  "needs_review": 2,
  "details": [...]
}
```

## Constraints
- Every evidence item must receive a validation status
- Validation must be deterministic and repeatable

## Failure Handling
- If evidence cannot be read, mark as NEEDS_REVIEW with explanation
- If file is missing but evidence has valid metadata, mark as NEEDS_REVIEW
- If required fields are missing, mark as INVALID
