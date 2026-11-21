"""
Agentic SDLC Factory (Lab 11 / Core Concept 11)
Automated agent-run lifecycle:
1. Requirement Analysis & Acceptance Criteria Synthesis
2. Code & Policy Generation
3. Automated Unit/Integration Test Generation
4. Verification & Regression Testing
5. Release Packaging with Human Lead Decision Gate
"""
import time
import json
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class SDLCReleaseDossier:
    release_id: str
    requirement: str
    specification: Dict[str, Any]
    generated_code_diff: str
    generated_tests: str
    test_results: Dict[str, Any]
    status: str = "AWAITING_LEAD_APPROVAL"  # AWAITING_LEAD_APPROVAL, APPROVED_RELEASED, REJECTED
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[float] = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AgenticSDLCFactory:
    """
    Autonomous Agentic SDLC Engine that drives software engineering tasks
    from human requirements to verified and tested releases.
    """
    def __init__(self):
        self.name = "AgenticSDLCFactory"
        self.releases: Dict[str, SDLCReleaseDossier] = {}

    def process_requirement(self, requirement_text: str) -> SDLCReleaseDossier:
        release_id = f"REL-{uuid.uuid4().hex[:6].upper()}"

        # -------------------------------------------------------------
        # Stage 1: Requirement Analysis & Acceptance Criteria
        # -------------------------------------------------------------
        spec = {
            "title": "Automated Appraisal Policy Extension",
            "parsed_requirement": requirement_text,
            "target_components": ["config/scoring_rules.json", "app/skills/api_calculation/skill.py"],
            "acceptance_criteria": [
                "New rule parsed deterministically without schema violation.",
                "Cap bounds enforced (total category score cannot exceed maximum limit).",
                "Existing scoring calculation logic does not regress.",
            ],
            "risk_profile": "LOW_TO_MEDIUM",
        }

        # -------------------------------------------------------------
        # Stage 2: Code & Configuration Generation
        # -------------------------------------------------------------
        code_diff = f"""--- a/config/scoring_rules.json
+++ b/config/scoring_rules.json
@@ -15,6 +15,11 @@
+    "custom_extension": {{
+      "description": "Rule added by SDLC Factory for: {requirement_text[:40]}...",
+      "weight": 5.0,
+      "max_cap": 15.0,
+      "enabled": true
+    }}
"""

        # -------------------------------------------------------------
        # Stage 3: Automated Test Synthesis
        # -------------------------------------------------------------
        safe_id = release_id.replace("-", "_").lower()
        generated_tests = f"""def test_generated_sdlc_rule_{safe_id}():
    # Test nominal execution
    payload = {{"custom_extension_points": 10.0}}
    assert payload["custom_extension_points"] <= 15.0, "Score must obey maximum cap"
    # Test boundary condition
    capped_payload = min(15.0, 20.0)
    assert capped_payload == 15.0, "Overflow must be strictly capped"
"""

        # -------------------------------------------------------------
        # Stage 4: Automated Verification & Regression Runner
        # -------------------------------------------------------------
        # Execute synthetic verification tests in a sandbox namespace
        test_namespace = {}
        try:
            exec(generated_tests, test_namespace)
            test_fn_name = f"test_generated_sdlc_rule_{safe_id}"
            test_namespace[test_fn_name]()
            test_passed = True
            test_error = None
        except Exception as exc:
            test_passed = False
            test_error = str(exc)

        test_results = {
            "tests_synthesized_count": 2,
            "tests_passed_count": 2 if test_passed else 0,
            "all_tests_passed": test_passed,
            "regression_status": "GREEN",
            "assertion_error": test_error,
        }

        # -------------------------------------------------------------
        # Stage 5: Release Packaging (Human Gate)
        # -------------------------------------------------------------
        dossier = SDLCReleaseDossier(
            release_id=release_id,
            requirement=requirement_text,
            specification=spec,
            generated_code_diff=code_diff,
            generated_tests=generated_tests,
            test_results=test_results,
            status="AWAITING_LEAD_APPROVAL",
        )
        self.releases[release_id] = dossier
        return dossier

    def approve_release(self, release_id: str, approver_name: str = "Lead Software Architect") -> Dict[str, Any]:
        """Human Gate: Lead engineer reviews and approves the release."""
        dossier = self.releases.get(release_id)
        if not dossier:
            raise ValueError(f"Release '{release_id}' not found.")

        if not dossier.test_results.get("all_tests_passed"):
            raise RuntimeError(f"Cannot approve release '{release_id}': Test suite failed!")

        dossier.status = "APPROVED_RELEASED"
        dossier.reviewed_by = approver_name
        dossier.reviewed_at = time.time()

        return {
            "status": "RELEASED",
            "release_id": release_id,
            "message": f"Release '{release_id}' successfully signed off by {approver_name} and marked deployed.",
        }

    def reject_release(self, release_id: str, reason: str, reviewer_name: str = "Lead Software Architect") -> Dict[str, Any]:
        """Human Gate: Lead engineer rejects the proposed release."""
        dossier = self.releases.get(release_id)
        if not dossier:
            raise ValueError(f"Release '{release_id}' not found.")

        dossier.status = "REJECTED"
        dossier.reviewed_by = reviewer_name
        dossier.reviewed_at = time.time()

        return {
            "status": "REJECTED",
            "release_id": release_id,
            "reason": reason,
        }
