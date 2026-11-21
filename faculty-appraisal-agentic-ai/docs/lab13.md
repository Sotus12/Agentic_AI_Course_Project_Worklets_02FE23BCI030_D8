# Lab 13: Discipline-Specific Agents (Engineering Worklets)

## 1. Concept Overview
Different academic engineering disciplines cannot be evaluated with a monolithic one-size-fits-all scoring rubric.
* In **Computer Science & AI (CS)**, scholarship centers on high-impact proceedings (IEEE, ACM, NeurIPS), open-source software artifacts, and algorithmic patents.
* In **Mechanical & Robotics Engineering (ME)**, excellence centers on physical prototyping, CAD/CAM/CAE lab maintenance, industrial fabrication consultancy, and ASME/SAE journals.
* In **Civil & Infrastructure Engineering (CE)**, value lies in structural health audits, government PWD consultancy, material testing, and field projects.
* In **Electrical & Electronics Engineering (EE)**, focus is on VLSI/embedded tape-outs, PCB design testbeds, power systems consultancy, and hardware prototypes.

## 2. Implementation in Team 8 (Faculty Appraisal)
In `app/discipline/discipline_agents.py`:
- **`DisciplineAppraisalCoordinator`**: Detects faculty department automatically and routes to the specialized discipline agent.
- **`ComputerScienceAppraisalAgent`**: Applies CS-weighted criteria mapped to **NBA Criterion 5.3** (Computing tools & software lab innovation).
- **`MechanicalAppraisalAgent`**: Applies ME-weighted criteria mapped to **NBA Criterion 5.4** (Workshop prototyping & industrial fabrication).
- **`CivilAppraisalAgent`**: Applies CE-weighted criteria mapped to **NBA Criterion 5.5** (Technical consultancy & materials testing).
- **`ElectricalAppraisalAgent`**: Applies EE-weighted criteria mapped to **NBA Criterion 5.6** (Hardware simulation testbeds & embedded systems).

## 3. Demonstration & Testing
Run via CLI:
```bash
python run.py discipline
```
Or via pytest:
```bash
pytest tests/test_labs_13_14.py -k test_discipline
```
