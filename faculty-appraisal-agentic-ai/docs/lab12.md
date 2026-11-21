# Lab 12: Responsible Autonomy & Safety Governance

## 1. Concept Overview
**Responsible Autonomy** enforces strict enterprise safety guardrails, auditability, fairness, state rollback capabilities, and data privacy to prevent harm, bias, and unauthorized mutations.

## 2. Implementation in Team 8 (Faculty Appraisal)
In `app/governance/responsible_autonomy.py`:
- **Cryptographic Rolling Hash Audit Chain (SHA-256):**
  - Maintains a blockchain-style rolling hash chain (`Block_N = SHA-256(Block_N-1 + Timestamp + Event + Payload)`).
  - Provides mathematical tamper-evidence: any unauthorized edit in database history breaks the hash chain.
  - `verify_audit_chain()` evaluates integrity across all historical blocks.
- **State Rollback Engine:**
  - Creates point-in-time state snapshots (`create_state_snapshot`).
  - Executes instant state rollbacks (`rollback_to_snapshot`) for disputed appraisals.
- **Algorithmic Fairness Benchmark:**
  - Evaluates institutional scoring distributions across departments using the standard EEOC Four-Fifths Rule (Disparate Impact Ratio >= 0.80).
- **PII Privacy Masking:**
  - Regular-expression redaction filter masking emails, phone numbers, and confidential medical/personal identifiers.
- **Autonomous Risk Tier Classifier:**
  - Classifies appraisals into Low, Medium, High, and Critical risk tiers.

## 3. Verification & Testing
Run via CLI:
```bash
python run.py governance
```
Or via pytest:
```bash
pytest tests/test_concepts_7_to_12.py -k test_responsible_autonomy
```

