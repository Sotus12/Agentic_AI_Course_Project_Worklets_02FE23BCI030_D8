"""
Parallel Swarms Package (Lab 8 / Core Concept 8)
Decentralized role-based peer agents collaborating via a shared Message Board
with cross-critique and consensus conflict resolution.
"""
from app.swarm.message_board import MessageBoard, SwarmMessage
from app.swarm.peers import (
    ResearchPeerAgent,
    PedagogyPeerAgent,
    GovernancePeerAgent,
    QualityAssurancePeerAgent,
)
from app.swarm.swarm import AppraisalSwarm

__all__ = [
    "MessageBoard",
    "SwarmMessage",
    "ResearchPeerAgent",
    "PedagogyPeerAgent",
    "GovernancePeerAgent",
    "QualityAssurancePeerAgent",
    "AppraisalSwarm",
]

