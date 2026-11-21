# Lab 9: Deep Research Agent

## 1. Concept Overview
A **Deep Research Agent** implements a repeatable, autonomous 5-phase research loop:
1. **Question Formulation:** Synthesizes targeted search hypotheses and queries.
2. **Search & Retrieval:** Queries indexing authorities and knowledgebases.
3. **Information Extraction:** Parses structured metadata, citation counts, and journal quartiles.
4. **Comparative Analysis:** Cross-references claimed metrics vs verified data to detect discrepancies.
5. **Synthesis:** Produces an Evidence Verification Matrix and calculates an overall Integrity Quotient.

## 2. Implementation in Team 8 (Faculty Appraisal)
In `app/research/deep_research.py`:
- `ScholarlyIndexDatabase`: Verified reference index of peer-reviewed journals (Scopus, Web of Science, IEEE Xplore, ACM DL).
- `DeepResearchAgent`:
  - Formulates 3 bibliometric queries per publication claim.
  - Queries indexing databases to retrieve impact factors and verified citation counts.
  - Detects citation inflation and unindexed venues.
  - Generates the **Evidence Verification Matrix (Citation Truth Table)** and computes the **Research Integrity Quotient** (0–100%).

## 3. Verification & Testing
Run via CLI:
```bash
python run.py research
```
Or via pytest:
```bash
pytest tests/test_concepts_7_to_12.py -k test_deep_research
```

