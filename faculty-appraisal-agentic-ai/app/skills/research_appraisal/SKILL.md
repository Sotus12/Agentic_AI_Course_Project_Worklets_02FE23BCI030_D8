---
name: research_appraisal
description: Collect and structure research evidence for faculty appraisal
version: "1.0"
---

# Research Appraisal Skill

## Purpose
Identify and collect research evidence for a faculty member, including publications, conference papers, patents, and research projects.

## Inputs
- `faculty_id` (str): The faculty identifier (e.g., "FAC001")

## Workflow
1. Read research CSV files: publications.csv, conferences.csv, patents.csv, projects.csv
2. Read any associated PDF evidence files
3. Categorize evidence by sub-category (publication, conference, patent, project)
4. Count items in each sub-category
5. Return structured research data

## Allowed Tools
- `read_csv`
- `read_pdf`
- `read_file`
- `get_evidence`

## Expected Output
```json
{
  "faculty_id": "FAC001",
  "category": "research",
  "publications": [...],
  "conferences": [...],
  "patents": [...],
  "projects": [...],
  "summary": {
    "publications_count": 5,
    "conferences_count": 2,
    "patents_count": 1,
    "projects_count": 2
  }
}
```

## Constraints
- Only read files within the faculty's data directory
- Do not modify any evidence files
- Report missing or unreadable files rather than failing silently

## Failure Handling
- If a CSV file is missing, report it and continue with available data
- If a PDF evidence file is missing, flag it for validation
- Return partial results with warnings rather than failing entirely
