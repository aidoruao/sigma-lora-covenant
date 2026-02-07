"""
TOPOLOGY VALIDATION ENGINE (REFACTORED)
All checks consume single canonical graph
Authority: IMMUTABLE
Generated: 2026-02-07
"""

from pathlib import Path
from typing import Dict, Set, List
from topology.graph_loader import load_topology_graph, TopologyGraph, Node, Edge
from topology.graph_loader import NodeClass, Authority, Verification, Temporal

class TopologyValidator:
    """Validation checks for topology structure"""
    
    def __init__(self, repo_root: Path):
        self.root = Path(repo_root)
        # Load canonical graph once
        self.graph = load_topology_graph(str(self.root))
    
    # STEP 3: IMPLEMENT ONLY 3 CHECKS
    
    # CHECK 1: INVARIANT_001 - Root Reachability
    def check_root_reachability(self) -> bool:
        """
        All nodes must be reachable from COVENANT_ROOT via BFS/DFS
        NO EXCEPTIONS
        """
        root_id = self.graph.covenant_root_id
        if not root_id:
            return False
        
        # BFS from root
        visited: Set[str] = set()
        queue: List[str] = [root_id]
        visited.add(root_id)
        
        while queue:
            current = queue.pop(0)
            
            # Get all outgoing edges
            for edge in self.graph.get_edges_from(current):
                if edge.target not in visited:
                    visited.add(edge.target)
                    queue.append(edge.target)
        
        # All nodes must be visited
        all_node_ids = set(self.graph.nodes.keys())
        unreachable = all_node_ids - visited
        
        if unreachable:
            self._first_violation = f"UNREACHABLE_NODES: {unreachable}"
            return False
        
        return True
    
    # CHECK 2: INVARIANT_004 - Verification Monotonicity
    def check_verification_monotonicity(self) -> bool:
        """
        VERIFICATION_REQUIREMENT can only increase along paths
        Ordering: NONE < HASH_CHAIN < CORRESPONDENCE
        FAIL IMMEDIATELY on any decrease
        """
        # Define strict enum ordering
        verification_order = {
            Verification.NONE: 0,
            Verification.HASH_CHAIN: 1,
            Verification.CORRESPONDENCE: 2,
            Verification.SIGNATURE: 3,
            Verification.FALSIFIABLE: 4
        }
        
        # Check all edges
        for edge in self.graph.edges.values():
            source_node = self.graph.get_node(edge.source)
            target_node = self.graph.get_node(edge.target)
            
            source_level = verification_order[source_node.verification]
            target_level = verification_order[target_node.verification]
            
            # Verification can increase or stay same, never decrease
            if target_level < source_level:
                self._first_violation = f"VERIFICATION_DECREASE: {edge.source} ({source_node.verification.value}) -> {edge.target} ({target_node.verification.value})"
                return False
        
        return True
    
    # CHECK 3: FORBIDDEN_001 - Authority Escalation Cycle
    def check_no_authority_escalation_cycle(self) -> bool:
        """
        Detect any cycle where authority level increases
        Graph-theoretic proof only (no semantics)
        """
        # Define authority ordering (lower number = higher authority)
        authority_order = {
            Authority.IMMUTABLE: 4,
            Authority.EXTERNAL_ONLY: 3,
            Authority.VALIDATED: 2,
            Authority.UNRESTRICTED: 1
        }
        
        # Detect cycles using DFS
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        path_authority: List[int] = []
        
        def has_escalation_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            
            node = self.graph.get_node(node_id)
            current_authority = authority_order[node.authority]
            path_authority.append(current_authority)
            
            # Check all neighbors
            for edge in self.graph.get_edges_from(node_id):
                target_id = edge.target
                target_node = self.graph.get_node(target_id)
                target_authority = authority_order[target_node.authority]
                
                if target_id not in visited:
                    if has_escalation_cycle(target_id):
                        return True
                elif target_id in rec_stack:
                    # Cycle detected - check if authority escalates
                    if target_authority > current_authority:
                        self._first_violation = f"AUTHORITY_ESCALATION_CYCLE: {node_id} ({node.authority.value}) -> {target_id} ({target_node.authority.value})"
                        return True
            
            path_authority.pop()
            rec_stack.remove(node_id)
            return False
        
        # Check from all nodes
        for node_id in self.graph.nodes.keys():
            if node_id not in visited:
                if has_escalation_cycle(node_id):
                    return False
        
        return True
    
    # ALL OTHER CHECKS REMAIN STUBS (EXPLICIT FAILURE)
    
    def check_mode_boundary_preservation(self) -> bool:
        """STUB: NOT IMPLEMENTED"""
        raise NotImplementedError("check_mode_boundary_preservation: NOT IMPLEMENTED")
    
    def check_constraint_layer_additivity(self) -> bool:
        """STUB: NOT IMPLEMENTED"""
        raise NotImplementedError("check_constraint_layer_additivity: NOT IMPLEMENTED")
    
    def check_temporal_ordering_consistency(self) -> bool:
        """STUB: NOT IMPLEMENTED"""
        raise NotImplementedError("check_temporal_ordering_consistency: NOT IMPLEMENTED")
    
    def check_correspondence_bijection(self) -> bool:
        """STUB: NOT IMPLEMENTED"""
        raise NotImplementedError("check_correspondence_bijection: NOT IMPLEMENTED")
    
    def check_guardian_non_interference(self) -> bool:
        """STUB: NOT IMPLEMENTED"""
        raise NotImplementedError("check_guardian_non_interference: NOT IMPLEMENTED")
    
    def check_violation_log_immutability(self) -> bool:
        """STUB: NOT IMPLEMENTED"""
        raise NotImplementedError("check_violation_log_immutability: NOT IMPLEMENTED")
    
    def check_spatial_orthogonality(self) -> bool:
        """STUB: NOT IMPLEMENTED"""
        raise NotImplementedError("check_spatial_orthogonality: NOT IMPLEMENTED")


def run_validation(repo_root: str) -> Dict[str, any]:
    """Execute implemented validation checks only"""
    validator = TopologyValidator(Path(repo_root))
    validator._first_violation = None
    
    results = {}
    
    # Run only implemented checks
    try:
        results['ROOT_REACHABILITY'] = validator.check_root_reachability()
        violation_1 = validator._first_violation
    except Exception as e:
        results['ROOT_REACHABILITY'] = False
        violation_1 = str(e)
    
    validator._first_violation = None
    try:
        results['VERIFICATION_MONOTONICITY'] = validator.check_verification_monotonicity()
        violation_2 = validator._first_violation
    except Exception as e:
        results['VERIFICATION_MONOTONICITY'] = False
        violation_2 = str(e)
    
    validator._first_violation = None
    try:
        results['NO_AUTHORITY_ESCALATION_CYCLE'] = validator.check_no_authority_escalation_cycle()
        violation_3 = validator._first_violation
    except Exception as e:
        results['NO_AUTHORITY_ESCALATION_CYCLE'] = False
        violation_3 = str(e)
    
    return {
        'checks': results,
        'violations': {
            'ROOT_REACHABILITY': violation_1 if not results.get('ROOT_REACHABILITY') else None,
            'VERIFICATION_MONOTONICITY': violation_2 if not results.get('VERIFICATION_MONOTONICITY') else None,
            'NO_AUTHORITY_ESCALATION_CYCLE': violation_3 if not results.get('NO_AUTHORITY_ESCALATION_CYCLE') else None,
        }
    }


if __name__ == '__main__':
    import sys
    
    repo = sys.argv[1] if len(sys.argv) > 1 else '.'
    results = run_validation(repo)
    
    print("\nTOPOLOGY VALIDATION RESULTS")
    print("=" * 60)
    
    for check_name, result in results['checks'].items():
        status = "YES" if result else "NO"
        print(f"{check_name}: {status}")
        
        if not result:
            violation = results['violations'].get(check_name)
            if violation:
                print(f"  VIOLATION: {violation}")
    
    print("\n")
