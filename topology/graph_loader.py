"""
CANONICAL TOPOLOGY GRAPH LOADER
Single source of truth for all validation checks
Authority: IMMUTABLE
Generated: 2026-02-07
"""

from pathlib import Path
from typing import Dict, Set, List, Optional
from dataclasses import dataclass, field
from enum import Enum

# Enumerations matching schema

class NodeClass(Enum):
    COVENANT_ROOT = "COVENANT_ROOT"
    PRINCIPLE_MODULE = "PRINCIPLE_MODULE"
    OPERATIONAL_MODE_ENFORCER = "OPERATIONAL_MODE_ENFORCER"
    GUARDIAN_SYSTEM = "GUARDIAN_SYSTEM"
    CORRESPONDENCE_BRIDGE = "CORRESPONDENCE_BRIDGE"
    FORGIVENESS_MODULE = "FORGIVENESS_MODULE"
    VIOLATION_LOG = "VIOLATION_LOG"
    EVIDENCE_ARTIFACT = "EVIDENCE_ARTIFACT"
    INFRASTRUCTURE_REGISTRY = "INFRASTRUCTURE_REGISTRY"
    DOCUMENTATION_INDEX = "DOCUMENTATION_INDEX"

class Authority(Enum):
    IMMUTABLE = 4
    EXTERNAL_ONLY = 3
    VALIDATED = 2
    UNRESTRICTED = 1

class ConstraintLayer(Enum):
    LOGOS = "LOGOS"
    CHALCEDON = "CHALCEDON"
    GRACE = "GRACE"
    KENOSIS = "KENOSIS"
    AGAPE = "AGAPE"
    COMPOSITE = "COMPOSITE"
    NONE = "NONE"

class Verification(Enum):
    NONE = 0
    HASH_CHAIN = 1
    CORRESPONDENCE = 2
    SIGNATURE = 3
    FALSIFIABLE = 4

class Temporal(Enum):
    GENESIS = 0
    FOUNDATION = 1
    SUBSTRATE = 2
    OVERLAY = 3
    EPHEMERAL = 4

class EdgeClass(Enum):
    COVENANT_BINDING = "COVENANT_BINDING"
    DEPENDENCY_IMPORT = "DEPENDENCY_IMPORT"
    VERIFICATION_CHAIN = "VERIFICATION_CHAIN"
    MODE_RESTRICTION = "MODE_RESTRICTION"
    GUARDIAN_WATCH = "GUARDIAN_WATCH"
    CORRESPONDENCE_MAPPING = "CORRESPONDENCE_MAPPING"
    VIOLATION_REFERENCE = "VIOLATION_REFERENCE"
    SPATIAL_CONTAINMENT = "SPATIAL_CONTAINMENT"

class Directionality(Enum):
    UNI = "UNI"
    BI = "BI"

# Graph structures

@dataclass(frozen=True)
class Node:
    """Immutable node in topology graph"""
    node_id: str
    node_class: NodeClass
    authority: Authority
    constraint_layer: Set[ConstraintLayer]
    verification: Verification
    temporal: Temporal
    operational_mode_binding: Optional[Set[str]] = None

@dataclass(frozen=True)
class Edge:
    """Immutable edge in topology graph"""
    edge_id: str
    source: str
    target: str
    edge_class: EdgeClass
    directionality: Directionality
    axis_binding: Set[str]

@dataclass
class TopologyGraph:
    """Canonical topology graph - single source of truth"""
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: Dict[str, Edge] = field(default_factory=dict)
    covenant_root_id: Optional[str] = None
    zones: Dict[str, Set[str]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate graph after loading"""
        self._validate()
    
    def _validate(self):
        """Enforce graph constraints"""
        # Must have exactly one covenant root
        roots = [n for n in self.nodes.values() if n.node_class == NodeClass.COVENANT_ROOT]
        if len(roots) == 0:
            raise ValueError("GRAPH_INVALID: No COVENANT_ROOT node found")
        if len(roots) > 1:
            raise ValueError(f"GRAPH_INVALID: Multiple COVENANT_ROOT nodes found: {[n.node_id for n in roots]}")
        
        self.covenant_root_id = roots[0].node_id
        
        # All edges must reference existing nodes
        for edge in self.edges.values():
            if edge.source not in self.nodes:
                raise ValueError(f"GRAPH_INVALID: Edge {edge.edge_id} references non-existent source: {edge.source}")
            if edge.target not in self.nodes:
                raise ValueError(f"GRAPH_INVALID: Edge {edge.edge_id} references non-existent target: {edge.target}")
    
    def get_node(self, node_id: str) -> Node:
        """Get node by ID (raises if not found)"""
        if node_id not in self.nodes:
            raise KeyError(f"NODE_NOT_FOUND: {node_id}")
        return self.nodes[node_id]
    
    def get_edges_from(self, node_id: str) -> List[Edge]:
        """Get all outgoing edges from node"""
        return [e for e in self.edges.values() if e.source == node_id]
    
    def get_edges_to(self, node_id: str) -> List[Edge]:
        """Get all incoming edges to node"""
        return [e for e in self.edges.values() if e.target == node_id]
    
    def get_covenant_root(self) -> Node:
        """Get the covenant root node"""
        if not self.covenant_root_id:
            raise ValueError("GRAPH_INVALID: No covenant root set")
        return self.get_node(self.covenant_root_id)


class GraphLoader:
    """Loads canonical topology graph from repository"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()
    
    def load(self) -> TopologyGraph:
        """Load complete topology graph"""
        graph = TopologyGraph()
        
        # Load nodes
        self._load_nodes(graph)
        
        # Load edges
        self._load_edges(graph)
        
        # Load zones
        self._load_zones(graph)
        
        return graph
    
    def _load_nodes(self, graph: TopologyGraph):
        """Load all nodes from repository structure"""
        
        # Covenant root
        covenant_path = self.repo_root / "covenant.yaml"
        if covenant_path.exists():
            graph.nodes["covenant.yaml"] = Node(
                node_id="covenant.yaml",
                node_class=NodeClass.COVENANT_ROOT,
                authority=Authority.EXTERNAL_ONLY,
                constraint_layer={ConstraintLayer.COMPOSITE},
                verification=Verification.HASH_CHAIN,
                temporal=Temporal.GENESIS
            )
        
        # Principle modules
        src_dir = self.repo_root / "src"
        if src_dir.exists():
            principles_path = src_dir / "principles.py"
            if principles_path.exists():
                graph.nodes["src/principles.py"] = Node(
                    node_id="src/principles.py",
                    node_class=NodeClass.PRINCIPLE_MODULE,
                    authority=Authority.VALIDATED,
                    constraint_layer={ConstraintLayer.LOGOS, ConstraintLayer.CHALCEDON, 
                                     ConstraintLayer.GRACE, ConstraintLayer.KENOSIS, 
                                     ConstraintLayer.AGAPE},
                    verification=Verification.CORRESPONDENCE,
                    temporal=Temporal.FOUNDATION
                )
            
            # Operational modes
            modes_path = src_dir / "operational_modes.py"
            if modes_path.exists():
                graph.nodes["src/operational_modes.py"] = Node(
                    node_id="src/operational_modes.py",
                    node_class=NodeClass.OPERATIONAL_MODE_ENFORCER,
                    authority=Authority.VALIDATED,
                    constraint_layer={ConstraintLayer.NONE},
                    verification=Verification.HASH_CHAIN,
                    temporal=Temporal.FOUNDATION
                )
            
            # Infrastructure
            infra_path = src_dir / "infrastructure.py"
            if infra_path.exists():
                graph.nodes["src/infrastructure.py"] = Node(
                    node_id="src/infrastructure.py",
                    node_class=NodeClass.INFRASTRUCTURE_REGISTRY,
                    authority=Authority.VALIDATED,
                    constraint_layer={ConstraintLayer.KENOSIS},
                    verification=Verification.HASH_CHAIN,
                    temporal=Temporal.FOUNDATION
                )
    
    def _load_edges(self, graph: TopologyGraph):
        """Load all edges from repository structure"""
        
        # Covenant bindings
        if "covenant.yaml" in graph.nodes and "src/principles.py" in graph.nodes:
            edge_id = "covenant.yaml::src/principles.py::COVENANT_BINDING"
            graph.edges[edge_id] = Edge(
                edge_id=edge_id,
                source="covenant.yaml",
                target="src/principles.py",
                edge_class=EdgeClass.COVENANT_BINDING,
                directionality=Directionality.UNI,
                axis_binding={"AUTHORITY", "CONSTRAINT_LAYER"}
            )
        
        # Dependency imports (detected from code analysis)
        # This would be populated by analyzing import statements
        # For now, minimal example
        
    def _load_zones(self, graph: TopologyGraph):
        """Load zone definitions"""
        graph.zones["zone_1_immutable"] = {"covenant.yaml"}
        graph.zones["zone_2_foundation"] = {
            "src/principles.py",
            "src/operational_modes.py", 
            "src/infrastructure.py"
        }


def load_topology_graph(repo_root: str) -> TopologyGraph:
    """
    Load canonical topology graph
    Single entry point for all validation checks
    """
    loader = GraphLoader(Path(repo_root))
    return loader.load()


if __name__ == '__main__':
    import sys
    
    repo = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    try:
        graph = load_topology_graph(repo)
        print(f"GRAPH_LOADED: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
        print(f"COVENANT_ROOT: {graph.covenant_root_id}")
        
        for node_id, node in graph.nodes.items():
            print(f"  {node_id}: {node.node_class.value}")
            
    except Exception as e:
        print(f"GRAPH_LOAD_FAILED: {e}")
        sys.exit(1)
