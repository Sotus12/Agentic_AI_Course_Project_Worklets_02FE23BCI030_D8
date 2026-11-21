"""
Swarm Execution & Consensus Engine (Lab 8 / Core Concept 8)
Orchestrates multi-round decentralized peer collaboration, cross-critique,
and automated conflict resolution without a central controller.
"""
import time
from typing import Dict, Any, List
from app.swarm.message_board import MessageBoard
from app.swarm.peers import (
    ResearchPeerAgent,
    PedagogyPeerAgent,
    GovernancePeerAgent,
    QualityAssurancePeerAgent,
)


class AppraisalSwarm:
    """
    Decentralized peer-to-peer swarm orchestrator.
    Manages peer interaction rounds on the shared message board:
    1. Independent Proposal Phase
    2. Cross-Critique Phase
    3. Conflict Detection & Democratic Consensus Resolution
    """
    def __init__(self):
        self.board = MessageBoard("Faculty Appraisal Peer Swarm")
        self.peers = [
            ResearchPeerAgent(),
            PedagogyPeerAgent(),
            GovernancePeerAgent(),
            QualityAssurancePeerAgent(),
        ]

    def run_swarm(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.board.clear()
        start_time = time.time()

        # -------------------------------------------------------------
        # Round 1: Independent Peer Proposals
        # -------------------------------------------------------------
        round_1_proposals = {}
        for peer in self.peers:
            msg = peer.propose(context, self.board)
            round_1_proposals[peer.name] = msg.content

        # -------------------------------------------------------------
        # Round 2: Peer Cross-Critiques
        # -------------------------------------------------------------
        round_2_critiques = []
        for peer in self.peers:
            critique_msgs = peer.critique(self.board)
            for c_msg in critique_msgs:
                round_2_critiques.append(c_msg.to_dict())

        # -------------------------------------------------------------
        # Round 3: Conflict Detection & Consensus Merge
        # -------------------------------------------------------------
        # Tally score adjustments proposed in Round 2
        adjustments_by_peer = {}
        for crit in round_2_critiques:
            target = crit["content"].get("target_peer")
            adj = crit["content"].get("score_adjustment_recommendation", 0.0)
            adjustments_by_peer[target] = adjustments_by_peer.get(target, 0.0) + adj

        # Resolve consensus scores per domain
        research_prop = round_1_proposals.get("ResearchPeerAgent", {}).get("proposed_score", 30.0)
        teaching_prop = round_1_proposals.get("PedagogyPeerAgent", {}).get("proposed_score", 30.0)
        admin_prop = round_1_proposals.get("GovernancePeerAgent", {}).get("proposed_score", 15.0)

        # Apply peer adjustments
        consensus_research = round(max(0.0, min(40.0, research_prop + adjustments_by_peer.get("ResearchPeerAgent", 0.0))), 2)
        consensus_teaching = round(max(0.0, min(40.0, teaching_prop + adjustments_by_peer.get("PedagogyPeerAgent", 0.0))), 2)
        consensus_admin = round(max(0.0, min(20.0, admin_prop + adjustments_by_peer.get("GovernancePeerAgent", 0.0))), 2)
        consensus_total = round(consensus_research + consensus_teaching + consensus_admin, 2)

        conflicts_resolved = [
            {
                "target": peer_name,
                "proposed": round_1_proposals.get(peer_name, {}).get("proposed_score"),
                "peer_adjustment": adjustments_by_peer.get(peer_name, 0.0),
                "resolution": "Applied weighted peer critique adjustment",
            }
            for peer_name in adjustments_by_peer
            if adjustments_by_peer[peer_name] != 0.0
        ]

        # Post final resolution message to board
        self.board.post(
            sender="ConsensusEngine",
            role="Decentralized Mediator",
            content={
                "consensus_scores": {
                    "research": consensus_research,
                    "teaching": consensus_teaching,
                    "administration": consensus_admin,
                    "total": consensus_total,
                },
                "conflicts_resolved_count": len(conflicts_resolved),
                "consensus_reached": True,
            },
            round_num=3,
        )

        duration_ms = int((time.time() - start_time) * 1000)

        return {
            "status": "CONSENSUS_REACHED",
            "duration_ms": duration_ms,
            "round_1_proposals": round_1_proposals,
            "round_2_critiques": round_2_critiques,
            "conflicts_resolved": conflicts_resolved,
            "consensus_scores": {
                "research": consensus_research,
                "teaching": consensus_teaching,
                "administration": consensus_admin,
                "total": consensus_total,
            },
            "message_board_trace": self.board.get_board_summary(),
        }

