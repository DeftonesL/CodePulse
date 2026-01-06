import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import networkx as nx

@dataclass
class CrossFileIssue:
    pass
    type: str
    severity: str
    files_involved: List[str]
    description: str
    impact: str
    suggestion: str
    metrics: Dict[str, Any] = field(default_factory=dict)

class ArchitectureAnalyzer:
    pass
    
    def __init__(self):
        self.dependency_graph = nx.DiGraph()
        self.module_graph = nx.DiGraph()
        self.issues = []
        self.metrics = {}
        
    def analyze_project(self, root_path: str) -> Dict[str, Any]:
        python_files = self._find_python_files(root_path)
        
        # Build graphs
        self._build_dependency_graph(python_files)
        self._build_module_graph(python_files)
        
        # Detect issues
        self._detect_circular_dependencies()
        self._detect_god_modules()
        self._detect_unstable_dependencies()
        self._detect_feature_clusters()
        self._calculate_architecture_metrics()
        
        return {
            'files_analyzed': len(python_files),
            'total_dependencies': self.dependency_graph.number_of_edges(),
            'architecture_score': self._calculate_architecture_score(),
            'issues': [
                {
                    'type': i.type,
                    'severity': i.severity,
                    'files': i.files_involved,
                    'description': i.description,
                    'impact': i.impact,
                    'suggestion': i.suggestion
                }
                for i in self.issues
            ],
            'metrics': self.metrics
        }
    
    def _find_python_files(self, root_path: str) -> List[str]:
        files = []
        for root, _, filenames in os.walk(root_path):
            if '__pycache__' in root or 'venv' in root or '.git' in root:
                continue
            for filename in filenames:
                if filename.endswith('.py'):
                    files.append(os.path.join(root, filename))
        return files
    
    def _build_dependency_graph(self, files: List[str]):
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=file_path)
                
                self.dependency_graph.add_node(file_path)
                
                # Extract imports
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        imported_modules = self._extract_imports(node)
                        for module in imported_modules:
                            # Try to resolve to file
                            resolved = self._resolve_import(module, file_path, files)
                            if resolved:
                                self.dependency_graph.add_edge(file_path, resolved)
            except:
                continue
    
    def _build_module_graph(self, files: List[str]):
        modules = defaultdict(list)
        
        for file_path in files:
            module_name = self._get_module_name(file_path)
            modules[module_name].append(file_path)
            self.module_graph.add_node(module_name)
        
        # Add edges based on file dependencies
        for src, dst in self.dependency_graph.edges():
            src_module = self._get_module_name(src)
            dst_module = self._get_module_name(dst)
            if src_module != dst_module:
                self.module_graph.add_edge(src_module, dst_module)
    
    def _extract_imports(self, node: ast.AST) -> List[str]:
        imports = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        return imports
    
    def _resolve_import(self, module: str, current_file: str, all_files: List[str]) -> str:
        current_dir = os.path.dirname(current_file)
        
        # Relative import
        if module.startswith('.'):
            module_path = os.path.join(current_dir, module.replace('.', '/') + '.py')
            if module_path in all_files:
                return module_path
        
        # Absolute import within project
        for file_path in all_files:
            if module.replace('.', '/') in file_path:
                return file_path
        
        return None
    
    def _get_module_name(self, file_path: str) -> str:
        return os.path.dirname(file_path).split('/')[-1] or 'root'
    
    def _detect_circular_dependencies(self):
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            
            for cycle in cycles:
                if len(cycle) > 1:
                    self.issues.append(CrossFileIssue(
                        type="Circular Dependency",
                        severity="HIGH",
                        files_involved=cycle,
                        description=f"Circular dependency chain: {' → '.join([os.path.basename(f) for f in cycle])}",
                        impact="Cannot test modules independently. Changes propagate unpredictably.",
                        suggestion="Break cycle using dependency injection or interface abstraction."
                    ))
        except:
            pass
    
    def _detect_god_modules(self):
        for node in self.module_graph.nodes():
            in_degree = self.module_graph.in_degree(node)
            out_degree = self.module_graph.out_degree(node)
            
            if out_degree > 10:
                self.issues.append(CrossFileIssue(
                    type="God Module",
                    severity="HIGH",
                    files_involved=[node],
                    description=f"Module '{node}' depends on {out_degree} other modules",
                    impact="High coupling makes changes difficult and risky.",
                    suggestion="Split module into smaller, focused components.",
                    metrics={'dependencies': out_degree}
                ))
            
            if in_degree > 15:
                self.issues.append(CrossFileIssue(
                    type="Hub Module",
                    severity="MEDIUM",
                    files_involved=[node],
                    description=f"Module '{node}' is depended on by {in_degree} other modules",
                    impact="Changes here affect many modules. High blast radius.",
                    suggestion="Ensure stability. Consider splitting if responsibilities are mixed.",
                    metrics={'dependents': in_degree}
                ))
    
    def _detect_unstable_dependencies(self):
        stabilities = {}
        
        for node in self.module_graph.nodes():
            fan_in = self.module_graph.in_degree(node)
            fan_out = self.module_graph.out_degree(node)
            
            if fan_in + fan_out > 0:
                stability = fan_out / (fan_in + fan_out)
                stabilities[node] = stability
        
        for src, dst in self.module_graph.edges():
            src_stability = stabilities.get(src, 0.5)
            dst_stability = stabilities.get(dst, 0.5)
            
            # Stable (low I) depending on unstable (high I)
            if src_stability < 0.3 and dst_stability > 0.7:
                self.issues.append(CrossFileIssue(
                    type="Unstable Dependency",
                    severity="MEDIUM",
                    files_involved=[src, dst],
                    description=f"Stable module '{src}' depends on unstable module '{dst}'",
                    impact="Unstable dependencies can cause ripple effects.",
                    suggestion="Depend on abstractions, not concretions. Use interfaces.",
                    metrics={'src_stability': src_stability, 'dst_stability': dst_stability}
                ))
    
    def _detect_feature_clusters(self):
        try:
            # Find strongly connected components
            components = list(nx.strongly_connected_components(self.dependency_graph))
            
            for component in components:
                if len(component) >= 5:  # At least 5 files
                    # Check if isolated from rest
                    external_deps = 0
                    for node in component:
                        for neighbor in self.dependency_graph.successors(node):
                            if neighbor not in component:
                                external_deps += 1
                    
                    if external_deps < 3:  # Few external dependencies
                        self.issues.append(CrossFileIssue(
                            type="Feature Cluster",
                            severity="INFO",
                            files_involved=list(component),
                            description=f"Found isolated cluster of {len(component)} files",
                            impact="Could be extracted to separate module/package.",
                            suggestion="Consider extracting as independent module for better organization."
                        ))
        except:
            pass
    
    def _calculate_architecture_metrics(self):
        # Modularity
        try:
            modularity = nx.algorithms.community.modularity(
                self.module_graph.to_undirected(),
                nx.algorithms.community.greedy_modularity_communities(
                    self.module_graph.to_undirected()
                )
            )
        except:
            modularity = 0.0
        
        # Average clustering coefficient
        try:
            clustering = nx.average_clustering(self.dependency_graph.to_undirected())
        except:
            clustering = 0.0
        
        # Density
        density = nx.density(self.dependency_graph)
        
        self.metrics = {
            'modularity': round(modularity, 3),
            'clustering_coefficient': round(clustering, 3),
            'density': round(density, 3),
            'total_modules': self.module_graph.number_of_nodes(),
            'total_files': self.dependency_graph.number_of_nodes(),
            'total_dependencies': self.dependency_graph.number_of_edges()
        }
    
    def _calculate_architecture_score(self) -> float:
        score = 100.0
        
        # Penalize based on issues
        for issue in self.issues:
            if issue.severity == 'HIGH':
                score -= 15
            elif issue.severity == 'MEDIUM':
                score -= 8
            elif issue.severity == 'LOW':
                score -= 3
        
        # Bonus for good modularity
        modularity = self.metrics.get('modularity', 0)
        if modularity > 0.5:
            score += 10
        
        # Penalize high density (too coupled)
        density = self.metrics.get('density', 0)
        if density > 0.3:
            score -= density * 20
        
        return max(0, min(100, score))

class CodeDuplicationAnalyzer:
    pass
    
    def __init__(self, min_lines: int = 6):
        self.min_lines = min_lines
        self.duplications = []
        
    def analyze_duplication(self, files: List[str]) -> Dict[str, Any]:
        file_hashes = {}
        
        # Hash code blocks from all files
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [l.strip() for l in f.readlines() if l.strip() and not l.strip().startswith('#')]
                
                file_hashes[file_path] = self._hash_code_blocks(lines)
            except:
                continue
        
        # Find duplicates across files
        hash_to_files = defaultdict(list)
        for file_path, hashes in file_hashes.items():
            for hash_val, line_range in hashes:
                hash_to_files[hash_val].append((file_path, line_range))
        
        # Report duplications
        for hash_val, occurrences in hash_to_files.items():
            if len(occurrences) > 1:
                self.duplications.append({
                    'files': [
                        {'file': f, 'lines': lines}
                        for f, lines in occurrences
                    ],
                    'size': occurrences[0][1][1] - occurrences[0][1][0],
                    'severity': 'HIGH' if len(occurrences) > 2 else 'MEDIUM'
                })
        
        total_duplicated = sum(d['size'] * (len(d['files']) - 1) for d in self.duplications)
        
        return {
            'total_duplications': len(self.duplications),
            'duplicated_lines': total_duplicated,
            'duplications': self.duplications[:10]  # Top 10
        }
    
    def _hash_code_blocks(self, lines: List[str]) -> List[Tuple[str, Tuple[int, int]]]:
        import hashlib
        hashes = []
        
        for i in range(len(lines) - self.min_lines + 1):
            block = '\n'.join(lines[i:i+self.min_lines])
            hash_val = hashlib.md5(block.encode()).hexdigest()
            hashes.append((hash_val, (i, i + self.min_lines)))
        
        return hashes

if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python cross_file_analysis.py <project_path>")
        sys.exit(1)
    
    analyzer = ArchitectureAnalyzer()
    results = analyzer.analyze_project(sys.argv[1])
    
    print("="*70)
    print("CROSS-FILE ARCHITECTURE ANALYSIS")
    print("="*70)
    print(f"\nFiles Analyzed: {results['files_analyzed']}")
    print(f"Architecture Score: {results['architecture_score']:.1f}/100")
    print(f"\nMetrics:")
    for key, value in results['metrics'].items():
        print(f"  {key}: {value}")
    
    print(f"\nIssues Found: {len(results['issues'])}")
    for issue in results['issues'][:5]:
        print(f"\n[{issue['severity']}] {issue['type']}")
        print(f"  {issue['description']}")
        print(f"  💡 {issue['suggestion']}")
