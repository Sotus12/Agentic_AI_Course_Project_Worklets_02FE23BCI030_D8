---
name: api_calculation
description: Calculate configurable appraisal scores using validated evidence
version: "1.0"
---

# API Calculation Skill

## Purpose
Load configurable scoring rules and calculate deterministic appraisal scores using ONLY validated evidence. "API" here refers to the faculty appraisal scoring concept, NOT Application Programming Interface.

## Inputs
- `faculty_id` (str): The faculty identifier
- `run_id` (str): The current appraisal run ID
- `validated_evidence` (dict): Structured evidence that passed validation

## Workflow
1. Load scoring rules from config/scoring_rules.json
2. Filter to only VALID evidence items
3. Calculate research score
4. Calculate teaching score
5. Calculate administration score
6. Calculate total score
7. Generate score breakdown with explanations
8. Save appraisal result to database

## Allowed Tools
- `calculate_score`
- `calculate_average`
- `get_validation_results`
- `save_appraisal_result`
- `get_previous_appraisal`

## Expected Output
```json
{
  "faculty_id": "FAC001",
  "research_score": 35.0,
  "teaching_score": 36.5,
  "administration_score": 20.0,
  "total_score": 91.5,
  "max_score": 100,
  "breakdown": {...}
}
```

## Constraints
- Use ONLY validated (VALID status) evidence for scoring
- Scoring must be deterministic — same inputs produce same outputs
- Do not use an LLM to generate or invent scores
- Clearly label as DEMO scoring policy

## Failure Handling
- If no validated evidence exists for a category, score that category as 0
- If scoring rules are missing, return error
