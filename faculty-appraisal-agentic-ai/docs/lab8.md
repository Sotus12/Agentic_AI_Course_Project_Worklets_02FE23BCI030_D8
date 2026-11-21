# Lab 8: Parallel Swarms & Decentralized Consensus

## 1. Concept Overview
Unlike master-worker orchestrators, **Parallel Swarms** employ coordinated peer agents operating over a shared blackboard (Message Board). Peers post independent evaluations, cross-critique each other's proposals, and resolve conflicts through consensus protocols.

## 2. Implementation in Team 8 (Faculty Appraisal)
In `app/swarm/`:
- **MessageBoard (`message_board.py`):** Decentralized shared message bus managing multi-round peer interactions.
- **Role-Based Peer Reviewers (`peers.py`):**
  1. `ResearchPeerAgent`: Evaluates publications, grants, and citations.
  2. `PedagogyPeerAgent`: Evaluates instructional metrics and student evaluations.
  3. `GovernancePeerAgent`: Evaluates institutional responsibilities.
  4. `QualityAssurancePeerAgent`: Audits overall consistency and evidence integrity.
- **AppraisalSwarm (`swarm.py`):**
  - **Round 1:** Independent Proposals posted to the Message Board.
  - **Round 2:** Peer Cross-Critiques (peers challenge high scores or trade-off imbalances).
  - **Round 3:** Conflict Resolution & Consensus Merge (applies weighted adjustments and outputs consensus scores).

## 3. Verification & Testing
Run via CLI:
```bash
python run.py swarm
```
Or via pytest:
```bash
pytest tests/test_concepts_7_to_12.py -k test_swarm
```

