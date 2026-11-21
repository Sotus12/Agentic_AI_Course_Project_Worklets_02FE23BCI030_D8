"""
Swarm Message Board (Lab 8 / Core Concept 8)
Shared blackboard / message broker for decentralized peer agents.
Enables peer-to-peer publication, topic subscriptions, and message threads.
"""
import time
import uuid
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class SwarmMessage:
    sender: str
    role: str
    topic: str
    content: Dict[str, Any]
    round_num: int
    message_id: str = field(default_factory=lambda: f"MSG-{uuid.uuid4().hex[:6].upper()}")
    timestamp: float = field(default_factory=time.time)
    in_reply_to: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MessageBoard:
    """
    Decentralized shared blackboard where peer agents publish artifacts,
    read fellow peers' proposals, and post peer-review critiques.
    """
    def __init__(self, topic: str = "Faculty Appraisal Peer Consensus"):
        self.topic = topic
        self.messages: List[SwarmMessage] = []

    def post(
        self,
        sender: str,
        role: str,
        content: Dict[str, Any],
        round_num: int,
        in_reply_to: Optional[str] = None,
    ) -> SwarmMessage:
        msg = SwarmMessage(
            sender=sender,
            role=role,
            topic=self.topic,
            content=content,
            round_num=round_num,
            in_reply_to=in_reply_to,
        )
        self.messages.append(msg)
        return msg

    def get_messages(
        self,
        round_num: Optional[int] = None,
        sender: Optional[str] = None,
        exclude_sender: Optional[str] = None,
    ) -> List[SwarmMessage]:
        result = self.messages
        if round_num is not None:
            result = [m for m in result if m.round_num == round_num]
        if sender is not None:
            result = [m for m in result if m.sender == sender]
        if exclude_sender is not None:
            result = [m for m in result if m.sender != exclude_sender]
        return result

    def get_board_summary(self) -> List[Dict[str, Any]]:
        return [m.to_dict() for m in self.messages]

    def clear(self):
        self.messages.clear()

