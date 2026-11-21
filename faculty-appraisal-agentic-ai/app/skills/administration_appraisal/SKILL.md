---
name: administration_appraisal
description: Collect and structure administrative evidence for faculty appraisal
version: "1.0"
---

# Administration Appraisal Skill

## Purpose
Read administrative evidence including committee memberships, coordinator roles, and institutional activities.

## Inputs
- `faculty_id` (str): The faculty identifier

## Workflow
1. Read administration CSV files: committees.csv, responsibilities.csv, activities.csv
2. Identify committee memberships
3. Identify coordinator/responsibility roles
4. Identify institutional activities
5. Return structured administrative data

## Allowed Tools
- `read_csv`
- `read_file`
- `get_evidence`

## Expected Output
```json
{
  "faculty_id": "FAC001",
  "category": "administration",
  "committees": [...],
  "coordinator_roles": [...],
  "activities": [...],
  "summary": {
    "committee_memberships": 2,
    "coordinator_roles": 1,
    "institutional_activities": 3
  }
}
```

## Constraints
- Only read files within the faculty's data directory
- Do not modify evidence

## Failure Handling
- If a CSV file is missing, report it and continue
- Return partial results with warnings
