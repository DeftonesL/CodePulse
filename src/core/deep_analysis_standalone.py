import ast
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class ControlFlowNode:
    pass
    id: int
    type: str
    code: str
    line: int
    successors: List[int] = field(default_factory=list)
    predecessors: List[int] = field(default_factory=list)

class SimpleGraph:
    pass
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, node_id, **attrs):
        self.nodes[node_id] = attrs
        
    def add_edge(self, src, dst):
        self.edges.append((src, dst))
        
    def number_of_nodes(self):
        return len(self.nodes)
    
    def number_of_edges(self):
        return len(self.edges)
    
    def successors(self, node):
        return [dst for src, dst in self.edges if src == node]
    
    def predecessors(self, node):
        return [src for src, dst in self.edges if dst == node]
    
    def in_degree(self, node):
        return len([e for e in self.edges if e[1] == node])
    
    def out_degree(self, node):
        return len([e for e in self.edges if e[0] == node])

class DeepAnalysisEngine:
    pass
    
    def __init__(self):
        self.cfg = SimpleGraph()
        self.dfg = SimpleGraph()
        self.call_graph = SimpleGraph()
        self.node_counter = 0
        
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            return {'error': str(e)}
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {'error': f'Syntax error: {e}'}
        
        # Build graphs
        self.build_control_flow_graph(tree)
        self.build_data_flow_graph(tree)
        self.build_call_graph(tree)
        
        # Analyze
        results = {
            'control_flow_analysis': self._analyze_control_flow(),
            'data_flow_analysis': self._analyze_data_flow(),
            'structural_analysis': self._analyze_structure(tree),
            'dependency_analysis': self._analyze_dependencies(),
            'complexity_metrics': self._calculate_advanced_complexity(),
            'code_quality_score': 0.0
        }
        
        results['code_quality_score'] = self._calculate_quality_score(results)
        
        return results
    
    def build_control_flow_graph(self, tree: ast.AST):
        self.cfg = SimpleGraph()
        self.node_counter = 0
        
        def visit_node(node, parent_id=None):
            current_id = self.node_counter
            self.node_counter += 1
            
            self.cfg.add_node(current_id, 
                            type=type(node).__name__,
                            line=getattr(node, 'lineno', 0))
            
            if parent_id is not None:
                self.cfg.add_edge(parent_id, current_id)
            
            if isinstance(node, ast.If):
                for stmt in node.body:
                    visit_node(stmt, current_id)
                if node.orelse:
                    for stmt in node.orelse:
                        visit_node(stmt, current_id)
            
            elif isinstance(node, (ast.While, ast.For)):
                loop_start = self.node_counter
                for stmt in node.body:
                    visit_node(stmt, current_id)
                if loop_start < self.node_counter:
                    self.cfg.add_edge(self.node_counter - 1, current_id)
            
            elif isinstance(node, ast.Try):
                for stmt in node.body:
                    visit_node(stmt, current_id)
                for handler in node.handlers:
                    for stmt in handler.body:
                        visit_node(stmt, current_id)
            else:
                for child in ast.iter_child_nodes(node):
                    visit_node(child, current_id)
            
            return current_id
        
        for node in ast.iter_child_nodes(tree):
            visit_node(node)
    
    def build_data_flow_graph(self, tree: ast.AST):
        self.dfg = SimpleGraph()
        definitions = defaultdict(list)
        uses = defaultdict(list)
        
        class DataFlowVisitor(ast.NodeVisitor):
            def __init__(self, defs, use):
                self.definitions = defs
                self.uses = use
            
            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.definitions[target.id].append(node.lineno)
                
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
        
        for var in set(list(definitions.keys()) + list(uses.keys())):
            self.dfg.add_node(var, 
                            definitions=definitions[var],
                            uses=uses[var])
    
    def build_call_graph(self, tree: ast.AST):
        self.call_graph = SimpleGraph()
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions[node.name] = node
                self.call_graph.add_node(node.name)
        
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
        if len(self.cfg.nodes) > 0:
            root_nodes = [n for n in self.cfg.nodes if self.cfg.in_degree(n) == 0]
            if root_nodes:
                reachable = set()
                stack = list(root_nodes)
                while stack:
                    node = stack.pop()
                    if node not in reachable:
                        reachable.add(node)
                        stack.extend(self.cfg.successors(node))
                
                unreachable = set(self.cfg.nodes.keys()) - reachable
                if unreachable:
                    issues.append({
                        'type': 'unreachable_code',
                        'severity': 'warning',
                        'message': f'Found {len(unreachable)} unreachable code blocks'
                    })
        
        # Detect potential infinite loops
        cycles = self._find_cycles()
        for cycle in cycles:
            has_exit = False
            for node in cycle:
                successors = self.cfg.successors(node)
                if any(s not in cycle for s in successors):
                    has_exit = True
                    break
            
            if not has_exit:
                issues.append({
                    'type': 'potential_infinite_loop',
                    'severity': 'error',
                    'message': 'Detected potential infinite loop'
                })
        
        branch_nodes = [n for n in self.cfg.nodes if self.cfg.out_degree(n) > 1]
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
            'cyclomatic_complexity': len(cycles) + 1 if cycles else 1
        }
    
    def _find_cycles(self) -> List[List[int]]:
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.cfg.successors(node):
                if neighbor not in visited:
                    dfs(neighbor, path[:])
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:])
            
            rec_stack.remove(node)
        
        for node in self.cfg.nodes:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def _analyze_data_flow(self) -> Dict[str, Any]:
        issues = []
        
        for var, data in self.dfg.nodes.items():
            definitions = data.get('definitions', [])
            uses = data.get('uses', [])
            
            if definitions and not uses:
                issues.append({
                    'type': 'unused_variable',
                    'severity': 'info',
                    'variable': var,
                    'message': f'Variable "{var}" defined but never used'
                })
            
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
        node_counts = defaultdict(int)
        for node in ast.walk(tree):
            node_counts[type(node).__name__] += 1
        
        functions = node_counts.get('FunctionDef', 0)
        classes = node_counts.get('ClassDef', 0)
        loops = node_counts.get('For', 0) + node_counts.get('While', 0)
        conditions = node_counts.get('If', 0)
        
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
        
        cycles = self._find_call_cycles()
        if cycles:
            issues.append({
                'type': 'circular_dependency',
                'severity': 'warning',
                'count': len(cycles),
                'message': f'Found {len(cycles)} circular dependencies'
            })
        
        if len(self.call_graph.nodes) > 0:
            degrees = [self.call_graph.in_degree(n) + self.call_graph.out_degree(n) 
                      for n in self.call_graph.nodes]
            avg_coupling = sum(degrees) / len(degrees) if degrees else 0
            
            if avg_coupling > 5:
                issues.append({
                    'type': 'high_coupling',
                    'severity': 'warning',
                    'message': f'High average coupling: {avg_coupling:.1f}'
                })
        else:
            avg_coupling = 0
        
        return {
            'issues': issues,
            'total_functions': self.call_graph.number_of_nodes(),
            'function_calls': self.call_graph.number_of_edges(),
            'circular_dependencies': len(cycles),
            'average_coupling': round(avg_coupling, 2)
        }
    
    def _find_call_cycles(self) -> List[List[str]]:
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.call_graph.successors(node):
                if neighbor not in visited:
                    dfs(neighbor, path[:])
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:])
            
            rec_stack.remove(node)
        
        for node in self.call_graph.nodes:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def _calculate_advanced_complexity(self) -> Dict[str, Any]:
        if self.cfg.number_of_nodes() > 0:
            graph_complexity = self.cfg.number_of_edges() / self.cfg.number_of_nodes()
        else:
            graph_complexity = 0
        
        if self.dfg.number_of_nodes() > 0:
            info_flow = self.dfg.number_of_edges() / self.dfg.number_of_nodes()
        else:
            info_flow = 0
        
        combined = graph_complexity * 0.4 + info_flow * 0.3
        
        return {
            'graph_complexity': round(graph_complexity, 2),
            'information_flow_complexity': round(info_flow, 2),
            'combined_complexity_score': round(combined, 2)
        }
    
    def _calculate_quality_score(self, results: Dict) -> float:
        score = 100.0
        
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
        
        complexity = results.get('complexity_metrics', {})
        combined = complexity.get('combined_complexity_score', 0)
        if combined > 5:
            score -= (combined - 5) * 5
        
        return max(0, min(100, score))

if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python deep_analysis_standalone.py <file.py>")
        sys.exit(1)
    
    engine = DeepAnalysisEngine()
    results = engine.analyze_file(sys.argv[1])
    
    print(json.dumps(results, indent=2))
