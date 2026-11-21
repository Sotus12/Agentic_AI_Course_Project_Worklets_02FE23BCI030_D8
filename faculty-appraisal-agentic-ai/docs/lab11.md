# Lab 11: Agentic SDLC Factory

## 1. Concept Overview
An **Agentic SDLC Factory** delegates software engineering lifecycle stages to autonomous agents: parsing human requirements, generating code changes, synthesizing unit/boundary tests, executing regression verification, and preparing release packages for human sign-off.

## 2. Implementation in Team 8 (Faculty Appraisal)
In `app/sdlc/sdlc_factory.py`:
- `AgenticSDLCFactory`:
  1. **Requirement Intake:** Parses faculty policy extension requests (e.g., "Add NBA Criterion 5.2 patent commercialization weighting").
  2. **Specification & Code Generation:** Generates schema updates and code diffs for `scoring_rules.json`.
  3. **Automated Test Synthesis:** Generates assertion test cases verifying cap boundaries and nominal points.
  4. **Automated Verification Runner:** Sandboxes and executes generated tests to guarantee zero regressions.
  5. **Human Lead Gate:** Compiles an `SDLCReleaseDossier` and awaits explicit human sign-off (`approve_release()`) before marking deployed.

## 3. Verification & Testing
Run via CLI:
```bash
python run.py sdlc
```
Or via pytest:
```bash
pytest tests/test_concepts_7_to_12.py -k test_agentic_sdlc
```

