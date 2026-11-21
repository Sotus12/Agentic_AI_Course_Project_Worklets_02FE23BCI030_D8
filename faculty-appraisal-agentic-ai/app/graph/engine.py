"""
Node Graph Engine (Lab 7 / Core Concept 7)
Explicit Directed Acyclic Graph (DAG) runtime with:
- Stateful nodes
- Parallel branches
- Conditional decision edges
- Human review gates with checkpointing & resumption
- Mermaid flowchart generation
"""
import time
import copy
import uuid
from typing import Dict, Any, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed


class Node:
    """Base unit of computation in a node graph."""
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute node logic and return updated state fields."""
        raise NotImplementedError


class ConditionEdge:
    """Evaluates state to choose between true_target and false_target."""
    def __init__(
        self,
        source: str,
        true_target: str,
        false_target: str,
        condition_fn: Callable[[Dict[str, Any]], bool],
        description: str = "",
    ):
        self.source = source
        self.true_target = true_target
        self.false_target = false_target
        self.condition_fn = condition_fn
        self.description = description

    def evaluate(self, state: Dict[str, Any]) -> str:
        return self.true_target if self.condition_fn(state) else self.false_target


class ParallelBranchNode(Node):
    """Executes multiple sub-nodes concurrently and merges their state updates."""
    def __init__(self, name: str, branch_nodes: List[Node], description: str = ""):
        super().__init__(name, description)
        self.branch_nodes = branch_nodes

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        merged_updates: Dict[str, Any] = {}
        branch_traces: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=max(1, len(self.branch_nodes))) as executor:
            future_to_node = {
                executor.submit(node.execute, copy.deepcopy(state)): node
                for node in self.branch_nodes
            }
            for future in as_completed(future_to_node):
                node = future_to_node[future]
                start_t = time.time()
                try:
                    res = future.result()
                    duration = int((time.time() - start_t) * 1000)
                    merged_updates.update(res)
                    branch_traces.append({
                        "node": node.name,
                        "status": "success",
                        "duration_ms": duration,
                        "keys_updated": list(res.keys()),
                    })
                except Exception as exc:
                    branch_traces.append({
                        "node": node.name,
                        "status": "failed",
                        "error": str(exc),
                    })
                    merged_updates[f"error_{node.name}"] = str(exc)

        merged_updates[f"{self.name}_branch_trace"] = branch_traces
        return merged_updates


class HumanGateNode(Node):
    """
    Halts graph execution to allow explicit human review and sign-off.
    Can be configured to auto-approve in unattended mode or wait for human signal.
    """
    def __init__(self, name: str, review_topic: str = "Appraisal Review", description: str = ""):
        super().__init__(name, description)
        self.review_topic = review_topic

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        human_approved = state.get("human_approved", False)
        auto_mode = state.get("auto_advance_human_gate", False)

        if auto_mode or human_approved:
            return {
                "gate_status": "APPROVED",
                "gate_approved_by": state.get("reviewer_name", "Authorized Human Evaluator (Auto-Approved)"),
                "gate_passed_at": time.time(),
            }

        # Otherwise signal that gate has paused the workflow
        return {
            "gate_status": "PAUSED_AWAITING_HUMAN",
            "gate_topic": self.review_topic,
            "gate_paused_at": time.time(),
        }


class StateGraph:
    """
    Compiled Directed Acyclic Graph orchestrator managing node execution,
    state flow, conditional routing, checkpoints, and visualization.
    """
    def __init__(self, name: str = "AgenticWorkflowGraph"):
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, str] = {}  # source -> target
        self.conditional_edges: Dict[str, ConditionEdge] = {}
        self.entry_point: Optional[str] = None
        self.finish_points: set = set()
        self.checkpoints: Dict[str, Dict[str, Any]] = {}

    def add_node(self, node: Node) -> "StateGraph":
        self.nodes[node.name] = node
        return self

    def set_entry_point(self, node_name: str) -> "StateGraph":
        if node_name not in self.nodes:
            raise ValueError(f"Entry point '{node_name}' must be added as a node first.")
        self.entry_point = node_name
        return self

    def add_edge(self, source: str, target: str) -> "StateGraph":
        if source not in self.nodes or target not in self.nodes:
            raise ValueError(f"Both {source} and {target} must exist in graph nodes.")
        self.edges[source] = target
        return self

    def add_conditional_edge(self, condition_edge: ConditionEdge) -> "StateGraph":
        self.conditional_edges[condition_edge.source] = condition_edge
        return self

    def add_finish_point(self, node_name: str) -> "StateGraph":
        self.finish_points.add(node_name)
        return self

    def run(
        self,
        initial_state: Dict[str, Any],
        max_steps: int = 50,
        checkpoint_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute the graph from entry point (or resumed checkpoint).
        """
        run_id = initial_state.get("run_id", f"GRAPH-{uuid.uuid4().hex[:6].upper()}")
        state = copy.deepcopy(initial_state)
        state["run_id"] = run_id
        current_node = state.get("current_node", self.entry_point)

        execution_history: List[Dict[str, Any]] = []
        step_count = 0
        status = "RUNNING"

        while current_node and step_count < max_steps:
            step_count += 1
            node = self.nodes.get(current_node)
            if not node:
                raise RuntimeError(f"Encountered unknown node in execution: '{current_node}'")

            start_t = time.time()
            try:
                node_updates = node.execute(state)
                duration_ms = int((time.time() - start_t) * 1000)
                state.update(node_updates)

                # Check if this node is a paused human gate
                if node_updates.get("gate_status") == "PAUSED_AWAITING_HUMAN":
                    status = "PAUSED_FOR_HUMAN"
                    state["current_node"] = current_node
                    execution_history.append({
                        "step": step_count,
                        "node": current_node,
                        "status": "paused",
                        "duration_ms": duration_ms,
                        "message": "Workflow paused at human review gate. Awaiting external sign-off.",
                    })
                    # Save checkpoint
                    save_ckpt_id = checkpoint_id or f"CKPT-{run_id}"
                    self.checkpoints[save_ckpt_id] = {
                        "checkpoint_id": save_ckpt_id,
                        "run_id": run_id,
                        "node": current_node,
                        "state": copy.deepcopy(state),
                        "saved_at": time.time(),
                    }
                    break

                execution_history.append({
                    "step": step_count,
                    "node": current_node,
                    "status": "success",
                    "duration_ms": duration_ms,
                    "updates": list(node_updates.keys()),
                })

            except Exception as exc:
                duration_ms = int((time.time() - start_t) * 1000)
                status = "FAILED"
                state["error"] = str(exc)
                execution_history.append({
                    "step": step_count,
                    "node": current_node,
                    "status": "failed",
                    "error": str(exc),
                    "duration_ms": duration_ms,
                })
                break

            # If node is registered as a terminal point, stop
            if current_node in self.finish_points:
                status = "COMPLETED"
                break

            # Determine next node via conditional edges or standard edges
            if current_node in self.conditional_edges:
                cond_edge = self.conditional_edges[current_node]
                next_node = cond_edge.evaluate(state)
            elif current_node in self.edges:
                next_node = self.edges[current_node]
            else:
                # No outgoing edge = terminus
                status = "COMPLETED"
                break

            current_node = next_node

        state["execution_history"] = execution_history
        state["graph_status"] = status
        state["total_steps"] = step_count

        return state

    def resume(self, checkpoint_id: str, human_approval: bool, approver_name: str = "Faculty Reviewer") -> Dict[str, Any]:
        """Resume execution from a human gate checkpoint."""
        ckpt = self.checkpoints.get(checkpoint_id)
        if not ckpt:
            raise ValueError(f"No checkpoint found with ID: '{checkpoint_id}'")

        resumed_state = copy.deepcopy(ckpt["state"])
        resumed_state["human_approved"] = human_approval
        resumed_state["reviewer_name"] = approver_name
        # Advance from current paused node to its next edge
        paused_node = ckpt["node"]
        if paused_node in self.conditional_edges:
            next_node = self.conditional_edges[paused_node].evaluate(resumed_state)
        else:
            next_node = self.edges.get(paused_node)

        resumed_state["current_node"] = next_node
        return self.run(resumed_state)

    def to_mermaid(self) -> str:
        """Export the graph structure to a Mermaid flowchart diagram."""
        lines = ["flowchart TD"]
        for name, node in self.nodes.items():
            desc = f"<br/><small>{node.description}</small>" if node.description else ""
            if isinstance(node, HumanGateNode):
                lines.append(f'    {name}{{"🚪 {name}{desc}"}}:::gate')
            elif isinstance(node, ParallelBranchNode):
                lines.append(f'    {name}["⚡ {name} (Parallel Branch){desc}"]:::parallel')
            else:
                lines.append(f'    {name}["⚙️ {name}{desc}"]:::standard')

        for src, dst in self.edges.items():
            lines.append(f"    {src} --> {dst}")

        for src, c_edge in self.conditional_edges.items():
            lines.append(f'    {src} -->|True: {c_edge.description}| {c_edge.true_target}')
            lines.append(f'    {src} -->|False| {c_edge.false_target}')

        lines.append("    classDef gate fill:#FEF3C7,stroke:#D97706,stroke-width:2px;")
        lines.append("    classDef parallel fill:#E0E7FF,stroke:#4F46E5,stroke-width:2px;")
        lines.append("    classDef standard fill:#F3F4F6,stroke:#4B5563,stroke-width:1px;")
        return "\n".join(lines)

