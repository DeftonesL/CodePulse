import ast
import re
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class PerformanceIssueType(Enum):
    pass
    INEFFICIENT_LOOP = "inefficient_loop"
    PREMATURE_OPTIMIZATION = "premature_optimization"
    MEMORY_LEAK = "memory_leak"
    N_PLUS_ONE = "n_plus_one"
    EXPENSIVE_OPERATION = "expensive_operation"
    INEFFICIENT_DATA_STRUCTURE = "inefficient_data_structure"

@dataclass
class PerformanceIssue:
    pass
    type: PerformanceIssueType
    severity: str
    title: str
    description: str
    location: str
    line: int
    estimated_impact: str  # High, Medium, Low
    recommendation: str
    code_example: str

class PerformanceAnalyzer:
    pass
    
    def __init__(self):
        self.issues: List[PerformanceIssue] = []
    
    def analyze_file(self, file_path: str) -> List[PerformanceIssue]:
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            self._detect_nested_loops(tree, file_path)
            self._detect_inefficient_operations(tree, file_path)
            self._detect_memory_issues(tree, file_path)
            self._detect_expensive_operations(tree, file_path)
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return self.issues
    
    def _detect_nested_loops(self, tree: ast.AST, file_path: str):
        
        def check_node(node, depth=0):
            if isinstance(node, (ast.For, ast.While)):
                if depth > 0:  # Nested loop
                    complexity = "O(n²)" if depth == 1 else f"O(n^{depth + 1})"
                    
                    self.issues.append(PerformanceIssue(
                        type=PerformanceIssueType.INEFFICIENT_LOOP,
                        severity="HIGH" if depth > 1 else "MEDIUM",
                        title=f"Nested Loop - {complexity} Complexity",
                        description=f"Loop nested {depth + 1} levels deep, resulting in {complexity} time complexity",
                        location=file_path,
                        line=node.lineno,
                        estimated_impact="High" if depth > 1 else "Medium",
                        recommendation=f"Consider using a more efficient algorithm or data structure. Try hash maps, sets, or preprocessing.",
                        code_example=f
                    ))
                
                for child in ast.iter_child_nodes(node):
                    check_node(child, depth + 1)
            else:
                for child in ast.iter_child_nodes(node):
                    check_node(child, depth)
        
        check_node(tree)
    
    def _detect_inefficient_operations(self, tree: ast.AST, file_path: str):
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Attribute):
                            method = child.func.attr
                            
                            if method in ['__add__', 'format'] and self._is_in_loop(child, node):
                                self.issues.append(PerformanceIssue(
                                    type=PerformanceIssueType.INEFFICIENT_LOOP,
                                    severity="MEDIUM",
                                    title="String Concatenation in Loop",
                                    description="String concatenation in loop is inefficient",
                                    location=file_path,
                                    line=child.lineno,
                                    estimated_impact="Medium",
                                    recommendation="Use join() or list comprehension instead",
                                    code_example=
                                ))
            
            if isinstance(node, ast.For):
                if isinstance(node.iter, ast.Call):
                    if isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                        for child in ast.walk(node.body[0] if node.body else node):
                            if isinstance(child, ast.Subscript):
                                self.issues.append(PerformanceIssue(
                                    type=PerformanceIssueType.INEFFICIENT_DATA_STRUCTURE,
                                    severity="LOW",
                                    title="Iterating by Index",
                                    description="Iterating by index instead of directly over items",
                                    location=file_path,
                                    line=node.lineno,
                                    estimated_impact="Low",
                                    recommendation="Iterate directly over items or use enumerate() if you need the index",
                                    code_example=
                                ))
                                break
    
    def _detect_memory_issues(self, tree: ast.AST, file_path: str):
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'read' and not node.args:
                        self.issues.append(PerformanceIssue(
                            type=PerformanceIssueType.MEMORY_LEAK,
                            severity="HIGH",
                            title="Reading Entire File into Memory",
                            description="file.read() loads entire file into memory",
                            location=file_path,
                            line=node.lineno,
                            estimated_impact="High",
                            recommendation="Read file in chunks or line by line for large files",
                            code_example=
                        ))
            
            if isinstance(node, ast.ListComp):
                parent = self._get_parent(node, tree)
                if isinstance(parent, ast.For):
                    self.issues.append(PerformanceIssue(
                        type=PerformanceIssueType.MEMORY_LEAK,
                        severity="MEDIUM",
                        title="List Comprehension for Iteration Only",
                        description="Creating list when generator would suffice",
                        location=file_path,
                        line=node.lineno,
                        estimated_impact="Medium",
                        recommendation="Use generator expression instead of list comprehension",
                        code_example=
                    ))
    
    def _detect_expensive_operations(self, tree: ast.AST, file_path: str):
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            if child.func.id in ['len', 'str', 'int', 'float']:
                                self.issues.append(PerformanceIssue(
                                    type=PerformanceIssueType.EXPENSIVE_OPERATION,
                                    severity="LOW",
                                    title="Repeated Function Calls",
                                    description=f"Calling {child.func.id}() repeatedly in loop",
                                    location=file_path,
                                    line=child.lineno,
                                    estimated_impact="Low",
                                    recommendation="Cache the result if it doesn't change",
                                    code_example=f
                                ))
                                break
            
            if isinstance(node, ast.FunctionDef):
                if len(node.body) == 1:
                    stmt = node.body[0]
                    if isinstance(stmt, ast.Return):
                        complexity = self._count_operations(stmt.value)
                        if complexity > 5:
                            self.issues.append(PerformanceIssue(
                                type=PerformanceIssueType.PREMATURE_OPTIMIZATION,
                                severity="LOW",
                                title="Overly Complex One-Liner",
                                description="Function crammed into single complex expression",
                                location=file_path,
                                line=node.lineno,
                                estimated_impact="Low",
                                recommendation="Break down into multiple readable steps. Readability > micro-optimization",
                                code_example=
                            ))
    
    def _is_in_loop(self, node: ast.AST, loop: ast.AST) -> bool:
        for child in ast.walk(loop):
            if child == node:
                return True
        return False
    
    def _get_parent(self, node: ast.AST, tree: ast.AST) -> ast.AST:
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                if child == node:
                    return parent
        return None
    
    def _count_operations(self, node: ast.AST) -> int:
        count = 0
        for _ in ast.walk(node):
            count += 1
        return count
    
    def get_report(self) -> Dict[str, Any]:
        return {
            'total_issues': len(self.issues),
            'by_severity': {
                'HIGH': len([i for i in self.issues if i.severity == 'HIGH']),
                'MEDIUM': len([i for i in self.issues if i.severity == 'MEDIUM']),
                'LOW': len([i for i in self.issues if i.severity == 'LOW'])
            },
            'by_impact': {
                'High': len([i for i in self.issues if i.estimated_impact == 'High']),
                'Medium': len([i for i in self.issues if i.estimated_impact == 'Medium']),
                'Low': len([i for i in self.issues if i.estimated_impact == 'Low'])
            },
            'issues': [
                {
                    'type': i.type.value,
                    'severity': i.severity,
                    'title': i.title,
                    'line': i.line,
                    'impact': i.estimated_impact,
                    'recommendation': i.recommendation
                }
                for i in self.issues
            ]
        }

if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python performance_analyzer.py <file.py>")
        sys.exit(1)
    
    analyzer = PerformanceAnalyzer()
    issues = analyzer.analyze_file(sys.argv[1])
    
    print(f"\nFound {len(issues)} performance issues:\n")
    for issue in issues:
        print(f"[{issue.severity}] {issue.title} (Line {issue.line})")
        print(f"  Impact: {issue.estimated_impact}")
        print(f"  💡 {issue.recommendation}\n")
    
    print("\nDetailed Report:")
    print(json.dumps(analyzer.get_report(), indent=2))
