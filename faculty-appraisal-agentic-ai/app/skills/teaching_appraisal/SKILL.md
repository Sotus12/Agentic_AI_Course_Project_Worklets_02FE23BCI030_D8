---
name: teaching_appraisal
description: Collect and structure teaching-learning evidence for faculty appraisal
version: "1.0"
---

# Teaching-Learning Appraisal Skill

## Purpose
Read and analyze teaching data including courses taught, attendance, student feedback, and academic results.

## Inputs
- `faculty_id` (str): The faculty identifier

## Workflow
1. Read teaching CSV files: courses.csv, attendance.csv, feedback.csv, results.csv
2. Analyze course load
3. Calculate average attendance percentage
4. Calculate average feedback score
5. Calculate average pass rate
6. Return structured teaching data

## Allowed Tools
- `read_csv`
- `read_file`
- `get_evidence`
- `calculate_average`

## Expected Output
```json
{
  "faculty_id": "FAC001",
  "category": "teaching",
  "courses": [...],
  "summary": {
    "courses_taught": 3,
    "avg_attendance_pct": 91.0,
    "avg_feedback_score": 4.3,
    "avg_pass_rate_pct": 88.3
  }
}
```

## Constraints
- Use only validated data from CSV files
- Calculate averages deterministically
- Do not fabricate or estimate missing data

## Failure Handling
- If a CSV file is missing, report it and continue with available data
- If data is malformed, flag for review
- Return partial results with warnings
