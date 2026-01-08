import ast
import networkx as nx
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
import re
import hashlib

@dataclass
class ControlFlowNode:
    pass
    id: int
    type: str  # 'statement', 'condition', 'loop', 'return', 'exception'
    code: str
    line: int
    successors: List[int] = field(default_factory=list)
    predecessors: List[int] = field(default_factory=list)
    
    
@dataclass
class DataFlowNode:
    pass
    variable: str
    definition_line: int
    uses: List[int] = field(default_factory=list)
    kills: List[int] = field(default_factory=list)

class DeepAnalysisEngine:
    pass
    
    def __init__(self):
        self.cfg = nx.DiGraph()  # Control flow graph
        self.dfg = nx.DiGraph()  # Data flow graph
        self.call_graph = nx.DiGraph()
        self.node_counter = 0
        
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        
        # Build graphs
        self.build_control_flow_graph(tree)
        self.build_data_flow_graph(tree)
        self.build_call_graph(tree)
        
        # Analyze graphs
        results = {
            'control_flow_analysis': self._analyze_control_flow(),
            'data_flow_analysis': self._analyze_data_flow(),
            'structural_analysis': self._analyze_structure(tree),
            'dependency_analysis': self._analyze_dependencies(),
            'complexity_metrics': self._calculate_advanced_complexity(),
            'code_quality_score': 0.0  # Will be calculated
        }
        
        # Calculate overall quality score
        results['code_quality_score'] = self._calculate_quality_score(results)
        
        return results
    
    def build_control_flow_graph(self, tree: ast.AST):
        self.cfg.clear()
        self.node_counter = 0
        
        def visit_node(node, parent_id=None):
            current_id = self.node_counter
            self.node_counter += 1
            
            # Add node to graph
            self.cfg.add_node(current_id, 
                            type=type(node).__name__,
                            line=getattr(node, 'lineno', 0))
            
            # Connect to parent
            if parent_id is not None:
                self.cfg.add_edge(parent_id, current_id)
            
            # Handle control flow structures
            if isinstance(node, ast.If):
                # True branch
                true_branch_id = self.node_counter
                for stmt in node.body:
                    visit_node(stmt, current_id)
                
                # False branch (else)
                if node.orelse:
                    false_branch_id = self.node_counter
                    for stmt in node.orelse:
                        visit_node(stmt, current_id)
            
            elif isinstance(node, (ast.While, ast.For)):
                # Loop body
                loop_body_id = self.node_counter
                for stmt in node.body:
                    visit_node(stmt, current_id)
                
                # Add back edge (loop)
                if loop_body_id < self.node_counter:
                    self.cfg.add_edge(self.node_counter - 1, current_id)
            
            elif isinstance(node, ast.Try):
                # Try block
                for stmt in node.body:
                    visit_node(stmt, current_id)
                
                # Exception handlers
                for handler in node.handlers:
                    for stmt in handler.body:
                        visit_node(stmt, current_id)
            
            else:
                # Regular statement
                for child in ast.iter_child_nodes(node):
                    visit_node(child, current_id)
            
            return current_id
        
        for node in ast.iter_child_nodes(tree):
            visit_node(node)
    
    def build_data_flow_graph(self, tree: ast.AST):
        self.dfg.clear()
        
        definitions = defaultdict(list)  # var -> [line numbers]
        uses = defaultdict(list)
        
        class DataFlowVisitor(ast.NodeVisitor):
            def __init__(self, defs, use):
                self.definitions = defs
                self.uses = use
            
            def visit_Assign(self, node):
                # Variable definition
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.definitions[target.id].append(node.lineno)
                
                # Right side uses
                for child in ast.walk(node.value):
                    if isinstance(child, ast.Name):
                        self.uses[child.id].append(node.lineno)
                
                self.generic_visit(node)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    self.uses[node.id].append(node.lineno)
                
                self.generic_visit(node)
        
        visitor = DataFlowVisitor(definitions, uses)
        visitor.visit(tree)
        
        # Build graph
        for var in set(list(definitions.keys()) + list(uses.keys())):
            self.dfg.add_node(var, 
                            definitions=definitions[var],
                            uses=uses[var])
        
        # Add edges for data dependencies
        for var in definitions:
            for def_line in definitions[var]:
                for use_line in uses[var]:
                    if use_line > def_line:
                        # Data flows from definition to use
                        self.dfg.add_edge(f"{var}@{def_line}", 
                                        f"{var}@{use_line}")
    
    def build_call_graph(self, tree: ast.AST):
        self.call_graph.clear()
        
        functions = {}  # name -> node
        
        # Find all function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
                self.call_graph.add_node(node.name)
        
        # Find calls
        for func_name, func_node in functions.items():
            for node in ast.walk(func_node):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        called = node.func.id
                        if called in functions:
                            self.call_graph.add_edge(func_name, called)
    
    def _analyze_control_flow(self) -> Dict[str, Any]:
        issues = []
        
        # Find unreachable nodes
        if self.cfg.nodes():
            root_nodes = [n for n in self.cfg.nodes() if self.cfg.in_degree(n) == 0]
            if root_nodes:
                reachable = set()
                for root in root_nodes:
                    reachable.update(nx.descendants(self.cfg, root))
                    reachable.add(root)
                
                unreachable = set(self.cfg.nodes()) - reachable
                if unreachable:
                    issues.append({
                        'type': 'unreachable_code',
                        'severity': 'warning',
                        'message': f'Found {len(unreachable)} unreachable code blocks'
                    })
        
        # Detect infinite loops
        try:
            cycles = list(nx.simple_cycles(self.cfg))
            for cycle in cycles:
                # Check if there's an exit from the cycle
                has_exit = False
                for node in cycle:
                    successors = list(self.cfg.successors(node))
                    if any(s not in cycle for s in successors):
                        has_exit = True
                        break
                
                if not has_exit:
                    issues.append({
                        'type': 'potential_infinite_loop',
                        'severity': 'error',
                        'message': 'Detected potential infinite loop'
                    })
        except (ValueError, TypeError, KeyError) as e:
            # Log error but continue analysis
            pass
        
        # Analyze branching complexity
        branch_nodes = [n for n in self.cfg.nodes() 
                       if self.cfg.out_degree(n) > 1]
        
        if len(branch_nodes) > 10:
            issues.append({
                'type': 'high_branching',
                'severity': 'warning',
                'message': f'High branching complexity: {len(branch_nodes)} decision points'
            })
        
        return {
            'issues': issues,
            'total_nodes': self.cfg.number_of_nodes(),
            'total_edges': self.cfg.number_of_edges(),
            'branch_points': len(branch_nodes),
            'cyclomatic_complexity': len(cycles) + 1 if 'cycles' in locals() else 1
        }
    
    def _analyze_data_flow(self) -> Dict[str, Any]:
        issues = []
        
        for var, data in self.dfg.nodes(data=True):
            definitions = data.get('definitions', [])
            uses = data.get('uses', [])
            
            # Unused variable
            if definitions and not uses:
                issues.append({
                    'type': 'unused_variable',
                    'severity': 'info',
                    'variable': var,
                    'message': f'Variable "{var}" defined but never used'
                })
            
            # Used before definition
            if uses and definitions:
                first_use = min(uses)
                first_def = min(definitions)
                if first_use < first_def:
                    issues.append({
                        'type': 'use_before_definition',
                        'severity': 'error',
                        'variable': var,
                        'message': f'Variable "{var}" used before definition'
                    })
        
        return {
            'issues': issues,
            'total_variables': self.dfg.number_of_nodes(),
            'data_dependencies': self.dfg.number_of_edges()
        }
    
    def _analyze_structure(self, tree: ast.AST) -> Dict[str, Any]:
        # Count different node types
        node_counts = defaultdict(int)
        for node in ast.walk(tree):
            node_counts[type(node).__name__] += 1
        
        # Calculate structural metrics
        functions = node_counts.get('FunctionDef', 0)
        classes = node_counts.get('ClassDef', 0)
        loops = node_counts.get('For', 0) + node_counts.get('While', 0)
        conditions = node_counts.get('If', 0)
        
        # My own formula based on code structure
        sci = (
            functions * 1.0 +
            classes * 2.0 +
            loops * 1.5 +
            conditions * 1.2
        ) / max(functions + classes + loops + conditions, 1)
        
        return {
            'functions': functions,
            'classes': classes,
            'loops': loops,
            'conditions': conditions,
            'structural_complexity_index': round(sci, 2),
            'node_type_distribution': dict(node_counts)
        }
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        issues = []
        
        # Find circular dependencies
        try:
            cycles = list(nx.simple_cycles(self.call_graph))
            if cycles:
                issues.append({
                    'type': 'circular_dependency',
                    'severity': 'warning',
                    'count': len(cycles),
                    'message': f'Found {len(cycles)} circular dependencies'
                })
        except (ValueError, TypeError, AttributeError) as e:
            cycles = []
        
        # Calculate coupling metrics
        if self.call_graph.nodes():
            avg_coupling = sum(self.call_graph.degree(n) 
                             for n in self.call_graph.nodes()) / self.call_graph.number_of_nodes()
            
            if avg_coupling > 5:
                issues.append({
                    'type': 'high_coupling',
                    'severity': 'warning',
                    'message': f'High average coupling: {avg_coupling:.1f} connections per function'
                })
        else:
            avg_coupling = 0
        
        # Calculate dependency depth
        try:
            if self.call_graph.nodes():
                longest_path = max(
                    nx.dag_longest_path_length(self.call_graph.subgraph(c))
                    for c in nx.weakly_connected_components(self.call_graph)
                    if nx.is_directed_acyclic_graph(self.call_graph.subgraph(c))
                )
            else:
                longest_path = 0
        except (ValueError, TypeError, nx.NetworkXError) as e:
            longest_path = 0
        
        return {
            'issues': issues,
            'total_functions': self.call_graph.number_of_nodes(),
            'function_calls': self.call_graph.number_of_edges(),
            'circular_dependencies': len(cycles),
            'average_coupling': round(avg_coupling, 2),
            'max_dependency_depth': longest_path
        }
    
    def _calculate_advanced_complexity(self) -> Dict[str, Any]:
        # Graph complexity metrics
        if self.cfg.nodes():
            graph_complexity = (
                self.cfg.number_of_edges() / 
                max(self.cfg.number_of_nodes(), 1)
            )
        else:
            graph_complexity = 0
        
        # Information flow complexity
        if self.dfg.nodes():
            info_flow_complexity = (
                self.dfg.number_of_edges() / 
                max(self.dfg.number_of_nodes(), 1)
            )
        else:
            info_flow_complexity = 0
        
        # Call depth complexity
        if self.call_graph.nodes():
            call_depth = nx.dag_longest_path_length(self.call_graph) if nx.is_directed_acyclic_graph(self.call_graph) else 0
        else:
            call_depth = 0
        
        # Combined complexity score (my formula)
        combined = (
            graph_complexity * 0.4 +
            info_flow_complexity * 0.3 +
            call_depth * 0.3
        )
        
        return {
            'graph_complexity': round(graph_complexity, 2),
            'information_flow_complexity': round(info_flow_complexity, 2),
            'call_depth': call_depth,
            'combined_complexity_score': round(combined, 2)
        }
    
    def _calculate_quality_score(self, results: Dict) -> float:
        score = 100.0
        
        # Penalize based on issues
        for analysis in ['control_flow_analysis', 'data_flow_analysis', 'dependency_analysis']:
            if analysis in results:
                issues = results[analysis].get('issues', [])
                for issue in issues:
                    if issue['severity'] == 'error':
                        score -= 10
                    elif issue['severity'] == 'warning':
                        score -= 5
                    elif issue['severity'] == 'info':
                        score -= 2
        
        # Penalize based on complexity
        complexity = results.get('complexity_metrics', {})
        combined = complexity.get('combined_complexity_score', 0)
        
        if combined > 5:
            score -= (combined - 5) * 5
        
        # Penalize based on coupling
        deps = results.get('dependency_analysis', {})
        coupling = deps.get('average_coupling', 0)
        
        if coupling > 3:
            score -= (coupling - 3) * 3
        
        return max(0, min(100, score))

# Example usage
if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python deep_analysis.py <file.py>")
        sys.exit(1)
    
    engine = DeepAnalysisEngine()
    results = engine.analyze_file(sys.argv[1])
    
    print(json.dumps(results, indent=2))
