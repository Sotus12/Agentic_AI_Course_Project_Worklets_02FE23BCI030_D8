---
name: report_generation
description: Generate PDF and JSON appraisal reports from scored evidence
version: "1.0"
---

# Report Generation Skill

## Purpose
Retrieve faculty profile, validated evidence, and appraisal scores to generate PDF and JSON reports.

## Inputs
- `faculty_id` (str): The faculty identifier
- `run_id` (str): The current appraisal run ID

## Workflow
1. Retrieve faculty profile
2. Retrieve validated evidence
3. Retrieve appraisal result and score breakdown
4. Retrieve previous appraisal for comparison
5. Generate JSON appraisal report
6. Generate PDF appraisal report
7. Return report paths

## Allowed Tools
- `query_faculty_data`
- `get_validation_results`
- `get_previous_appraisal`
- `generate_pdf`
- `generate_json`

## Expected Output
```json
{
  "faculty_id": "FAC001",
  "pdf_path": "reports/appraisal_FAC001_APP-2026-001.pdf",
  "json_path": "reports/appraisal_FAC001_APP-2026-001.json",
  "status": "DRAFT"
}
```

## Constraints
- Report must include all score breakdowns, validation summary, and warnings
- Report status must be "DRAFT — Awaiting Human Review"
- Do not automatically finalize the appraisal

## Failure Handling
- If appraisal data is incomplete, generate report with available data and include warnings
- If PDF generation fails, still attempt JSON generation
