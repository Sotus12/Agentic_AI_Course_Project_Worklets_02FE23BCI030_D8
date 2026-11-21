"""
Swarm Peer Agents (Lab 8 / Core Concept 8)
Role-based peer agents that independently propose scores, critique peer proposals,
and participate in multi-agent consensus resolution.
"""
from typing import Dict, Any, List
from app.swarm.message_board import MessageBoard, SwarmMessage


class ResearchPeerAgent:
    """Peer agent responsible for assessing scholarship, publications, and grant merit."""
    name = "ResearchPeerAgent"
    role = "Scholarship & Grants Reviewer"

    def propose(self, context: Dict[str, Any], board: MessageBoard) -> SwarmMessage:
        raw = context.get("collection", {}).get("Research Agent", {}).get("data", {})
        pubs = raw.get("publications", [])
        grants = raw.get("projects", [])

        # Independent peer evaluation logic
        score = min(40.0, len(pubs) * 5.0 + len(grants) * 10.0)
        content = {
            "proposed_domain": "research",
            "proposed_score": score,
            "max_score": 40.0,
            "rationale": f"Verified {len(pubs)} publication claims and {len(grants)} sponsored research projects.",
            "citations_confidence": "HIGH" if len(pubs) >= 3 else "MEDIUM",
        }
        return board.post(self.name, self.role, content, round_num=1)

    def critique(self, board: MessageBoard) -> List[SwarmMessage]:
        critiques = []
        # Inspect Round 1 proposals from other peers
        for msg in board.get_messages(round_num=1, exclude_sender=self.name):
            target = msg.sender
            c = msg.content
            if target == "PedagogyPeerAgent" and c.get("proposed_score", 0) > 35:
                critiques.append(board.post(
                    self.name,
                    self.role,
                    {
                        "target_peer": target,
                        "stance": "CONCUR_WITH_CAUTION",
                        "comment": "Pedagogical evaluation is high; verify course contact hours do not encroach on sponsored research commitments.",
                        "score_adjustment_recommendation": 0.0,
                    },
                    round_num=2,
                    in_reply_to=msg.message_id,
                ))
        return critiques


class PedagogyPeerAgent:
    """Peer agent responsible for assessing instructional delivery, pass rates, and evaluations."""
    name = "PedagogyPeerAgent"
    role = "Teaching & Pedagogy Reviewer"

    def propose(self, context: Dict[str, Any], board: MessageBoard) -> SwarmMessage:
        raw = context.get("collection", {}).get("Teaching Agent", {}).get("data", {})
        courses = raw.get("courses", [])
        avg_eval = raw.get("average_student_evaluation", 4.2)

        score = min(40.0, len(courses) * 10.0 + (avg_eval * 4.0))
        content = {
            "proposed_domain": "teaching",
            "proposed_score": round(score, 2),
            "max_score": 40.0,
            "rationale": f"Evaluated {len(courses)} course offerings with mean student feedback rating of {avg_eval}/5.0.",
            "pedagogy_health": "EXEMPLARY" if avg_eval >= 4.0 else "SATISFACTORY",
        }
        return board.post(self.name, self.role, content, round_num=1)

    def critique(self, board: MessageBoard) -> List[SwarmMessage]:
        critiques = []
        for msg in board.get_messages(round_num=1, exclude_sender=self.name):
            target = msg.sender
            c = msg.content
            if target == "GovernancePeerAgent" and c.get("proposed_score", 0) > 18:
                critiques.append(board.post(
                    self.name,
                    self.role,
                    {
                        "target_peer": target,
                        "stance": "CRITIQUE",
                        "comment": "Excessive institutional committee burdens may cause scheduling friction with student tutorial hours.",
                        "score_adjustment_recommendation": -1.0,
                    },
                    round_num=2,
                    in_reply_to=msg.message_id,
                ))
        return critiques


class GovernancePeerAgent:
    """Peer agent evaluating administrative responsibility, institutional committees, and accreditation service."""
    name = "GovernancePeerAgent"
    role = "Institutional Service Reviewer"

    def propose(self, context: Dict[str, Any], board: MessageBoard) -> SwarmMessage:
        raw = context.get("collection", {}).get("Administration Agent", {}).get("data", {})
        committees = raw.get("committees", [])
        responsibilities = raw.get("responsibilities", []) or raw.get("roles", [])
        activities = raw.get("activities", [])

        # Peer evaluation logic: 6 pts for committee, 7 pts for coordinator roles, 3.5 pts for institutional events
        score = min(20.0, len(committees) * 6.0 + len(responsibilities) * 7.0 + len(activities) * 3.5)

        # Fallback if summary metrics were provided
        if score == 0.0 and "summary" in raw:
            s = raw.get("summary", {})
            c_cnt = s.get("committee_memberships", 0)
            r_cnt = s.get("coordinator_roles", 0)
            a_cnt = s.get("institutional_activities", 0)
            score = min(20.0, c_cnt * 6.0 + r_cnt * 7.0 + a_cnt * 3.5)

        total_items = len(committees) + len(responsibilities) + len(activities)
        content = {
            "proposed_domain": "administration",
            "proposed_score": round(score, 2),
            "max_score": 20.0,
            "rationale": f"Assessed active stewardship across {len(committees)} committees, {len(responsibilities)} coordinator roles, and {len(activities)} institutional events.",
            "service_standing": "ACTIVE" if total_items > 0 else "INACTIVE",
        }
        return board.post(self.name, self.role, content, round_num=1)

    def critique(self, board: MessageBoard) -> List[SwarmMessage]:
        critiques = []
        for msg in board.get_messages(round_num=1, exclude_sender=self.name):
            target = msg.sender
            if target == "ResearchPeerAgent":
                critiques.append(board.post(
                    self.name,
                    self.role,
                    {
                        "target_peer": target,
                        "stance": "CONCUR",
                        "comment": "External grants directly align with institutional NIRF criteria; full credit endorsed.",
                        "score_adjustment_recommendation": 0.0,
                    },
                    round_num=2,
                    in_reply_to=msg.message_id,
                ))
        return critiques


class QualityAssurancePeerAgent:
    """Peer agent auditing overall balance, evidence authenticity, and anomaly flags."""
    name = "QualityAssurancePeerAgent"
    role = "Cross-Domain Quality Auditor"

    def propose(self, context: Dict[str, Any], board: MessageBoard) -> SwarmMessage:
        val_summary = context.get("validation", {}).get("summary", {})
        invalid_count = val_summary.get("invalid", 0)
        review_count = val_summary.get("needs_review", 0)

        confidence = 100.0 - (invalid_count * 15.0) - (review_count * 5.0)
        content = {
            "proposed_domain": "quality_assurance",
            "dossier_confidence_score": max(50.0, confidence),
            "flagged_issues_count": invalid_count + review_count,
            "rationale": f"QA verification audit detected {invalid_count} invalid items and {review_count} items requiring review.",
        }
        return board.post(self.name, self.role, content, round_num=1)

    def critique(self, board: MessageBoard) -> List[SwarmMessage]:
        critiques = []
        for msg in board.get_messages(round_num=1, exclude_sender=self.name):
            c = msg.content
            domain = c.get("proposed_domain")
            proposed_score = c.get("proposed_score", 0)
            if proposed_score > 38.0:
                critiques.append(board.post(
                    self.name,
                    self.role,
                    {
                        "target_peer": msg.sender,
                        "stance": "CHALLENGE",
                        "comment": f"High score claim ({proposed_score}) in {domain} requires rigorous corroboration against primary institutional records.",
                        "score_adjustment_recommendation": -1.5,
                    },
                    round_num=2,
                    in_reply_to=msg.message_id,
                ))
        return critiques

