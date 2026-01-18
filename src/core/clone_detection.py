import ast
import difflib
from typing import List, Dict, Set, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict
import hashlib

@dataclass
class CodeClone:
    pass
    type: str  # Type 1, 2, 3, or 4
    file1: str
    file2: str
    lines1: Tuple[int, int]
    lines2: Tuple[int, int]
    similarity: float
    size: int  # Lines of code
    severity: str

class CloneDetector:
    pass
    
    def __init__(self, min_lines: int = 10):  # Increased from 6
        self.min_lines = min_lines
        self.clones = []
        self.min_same_file_lines = 15  # Higher threshold for same-file clones
        
    def detect_clones_in_file(self, file_path: str) -> List[CodeClone]:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        self._detect_type1_clones(lines, file_path)
        
        try:
            tree = ast.parse(''.join(lines))
            self._detect_type2_clones(tree, file_path)
        except (SyntaxError, ValueError) as e:
            pass
        
        return self.clones
    
    def detect_clones_between_files(
        self, 
        file1: str, 
        file2: str
    ) -> List[CodeClone]:
        with open(file1, 'r', encoding='utf-8') as f:
            lines1 = f.readlines()
        
        with open(file2, 'r', encoding='utf-8') as f:
            lines2 = f.readlines()
        
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        
        for match in matcher.get_matching_blocks():
            if match.size >= self.min_lines:
                similarity = self._calculate_similarity(
                    lines1[match.a:match.a + match.size],
                    lines2[match.b:match.b + match.size]
                )
                
                self.clones.append(CodeClone(
                    type='Type 1',
                    file1=file1,
                    file2=file2,
                    lines1=(match.a + 1, match.a + match.size),
                    lines2=(match.b + 1, match.b + match.size),
                    similarity=similarity,
                    size=match.size,
                    severity='HIGH' if match.size > 20 else 'MEDIUM'
                ))
        
        return self.clones
    
    def _detect_type1_clones(self, lines: List[str], file_path: str):
        normalized = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                normalized.append(stripped)
        
        window_hashes = defaultdict(list)
        
        for i in range(len(normalized) - self.min_lines + 1):
            window = normalized[i:i + self.min_lines]
            window_hash = self._hash_code_block(window)
            window_hashes[window_hash].append(i)
        
        for hash_val, positions in window_hashes.items():
            if len(positions) > 1:
                for j in range(len(positions)):
                    for k in range(j + 1, len(positions)):
                        clone_size = self.min_lines
                        
                        if clone_size < self.min_same_file_lines:
                            continue
                        
                        self.clones.append(CodeClone(
                            type='Type 1',
                            file1=file_path,
                            file2=file_path,
                            lines1=(positions[j] + 1, positions[j] + self.min_lines),
                            lines2=(positions[k] + 1, positions[k] + self.min_lines),
                            similarity=100.0,
                            size=self.min_lines,
                            severity='HIGH'
                        ))
    
    def _detect_type2_clones(self, tree: ast.AST, file_path: str):
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
        
        for i in range(len(functions)):
            for j in range(i + 1, len(functions)):
                similarity = self._compare_ast_structure(
                    functions[i],
                    functions[j]
                )
                
                if similarity > 0.80:  # 80% similar
                    self.clones.append(CodeClone(
                        type='Type 2',
                        file1=file_path,
                        file2=file_path,
                        lines1=(functions[i].lineno, functions[i].end_lineno or functions[i].lineno),
                        lines2=(functions[j].lineno, functions[j].end_lineno or functions[j].lineno),
                        similarity=similarity * 100,
                        size=functions[i].end_lineno - functions[i].lineno if functions[i].end_lineno else 1,
                        severity='MEDIUM'
                    ))
    
    def _hash_code_block(self, lines: List[str]) -> str:
        combined = ''.join(lines)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _calculate_similarity(self, block1: List[str], block2: List[str]) -> float:
        matcher = difflib.SequenceMatcher(None, block1, block2)
        return matcher.ratio()
    
    def _compare_ast_structure(
        self, 
        node1: ast.AST, 
        node2: ast.AST
    ) -> float:
        struct1 = self._get_ast_fingerprint(node1)
        struct2 = self._get_ast_fingerprint(node2)
        
        if not struct1 or not struct2:
            return 0.0
        
        matcher = difflib.SequenceMatcher(None, struct1, struct2)
        return matcher.ratio()
    
    def _get_ast_fingerprint(self, node: ast.AST) -> str:
        fingerprint = []
        
        for child in ast.walk(node):
            fingerprint.append(type(child).__name__)
            
            if isinstance(child, (ast.For, ast.While)):
                fingerprint.append('LOOP')
            elif isinstance(child, ast.If):
                fingerprint.append('COND')
            elif isinstance(child, ast.BinOp):
                fingerprint.append(type(child.op).__name__)
        
        return ''.join(fingerprint)
    
    def get_clone_report(self) -> Dict[str, Any]:
        if not self.clones:
            return {
                'total_clones': 0,
                'total_duplicated_lines': 0,
                'duplication_percentage': 0.0,
                'clones_by_type': {},
                'clones_by_severity': {},
                'recommendations': ['No code clones detected. Great job!']
            }
        
        by_type = defaultdict(int)
        by_severity = defaultdict(int)
        total_lines = 0
        
        for clone in self.clones:
            by_type[clone.type] += 1
            by_severity[clone.severity] += 1
            total_lines += clone.size
        
        recommendations = []
        
        if by_severity['HIGH'] > 0:
            recommendations.append(
                f"URGENT: Found {by_severity['HIGH']} high-severity clones. "
                "Extract common code into reusable functions."
            )
        
        if by_type.get('Type 1', 0) > 5:
            recommendations.append(
                "Multiple exact clones detected. "
                "Consider using functions or classes to reduce duplication."
            )
        
        if total_lines > 50:
            recommendations.append(
                f"High duplication: {total_lines} lines duplicated. "
                "This increases maintenance cost significantly."
            )
        
        return {
            'total_clones': len(self.clones),
            'total_duplicated_lines': total_lines,
            'clones_by_type': dict(by_type),
            'clones_by_severity': dict(by_severity),
            'clones': [
                {
                    'type': c.type,
                    'file1': c.file1,
                    'file2': c.file2,
                    'lines1': c.lines1,
                    'lines2': c.lines2,
                    'similarity': round(c.similarity, 1),
                    'size': c.size,
                    'severity': c.severity
                }
                for c in self.clones
            ],
            'recommendations': recommendations
        }

class SemanticCloneDetector:
    pass
    
    def __init__(self):
        self.semantic_clones = []
    
    def detect_semantic_clones(self, tree: ast.AST) -> List[Dict]:
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                behavior = self._analyze_function_behavior(node)
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'behavior': behavior
                })
        
        for i in range(len(functions)):
            for j in range(i + 1, len(functions)):
                similarity = self._compare_behaviors(
                    functions[i]['behavior'],
                    functions[j]['behavior']
                )
                
                if similarity > 0.70:  # 70% behavioral similarity
                    self.semantic_clones.append({
                        'function1': functions[i]['name'],
                        'function2': functions[j]['name'],
                        'line1': functions[i]['line'],
                        'line2': functions[j]['line'],
                        'similarity': similarity * 100
                    })
        
        return self.semantic_clones
    
    def _analyze_function_behavior(self, func: ast.FunctionDef) -> Dict:
        behavior = {
            'operations': [],
            'returns_type': None,
            'modifies_args': False,
            'calls_functions': [],
            'uses_loops': False,
            'uses_conditions': False
        }
        
        for node in ast.walk(func):
            if isinstance(node, ast.BinOp):
                behavior['operations'].append(type(node.op).__name__)
            
            if isinstance(node, ast.Return):
                if node.value:
                    behavior['returns_type'] = type(node.value).__name__
            
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    behavior['calls_functions'].append(node.func.id)
            
            if isinstance(node, (ast.For, ast.While)):
                behavior['uses_loops'] = True
            
            if isinstance(node, ast.If):
                behavior['uses_conditions'] = True
        
        return behavior
    
    def _compare_behaviors(self, b1: Dict, b2: Dict) -> float:
        score = 0.0
        factors = 0
        
        if b1['operations'] == b2['operations']:
            score += 0.3
        factors += 0.3
        
        if b1['returns_type'] == b2['returns_type']:
            score += 0.2
        factors += 0.2
        
        common_calls = set(b1['calls_functions']) & set(b2['calls_functions'])
        if common_calls:
            score += 0.25
        factors += 0.25
        
        if b1['uses_loops'] == b2['uses_loops']:
            score += 0.125
        factors += 0.125
        
        if b1['uses_conditions'] == b2['uses_conditions']:
            score += 0.125
        factors += 0.125
        
        return score / factors if factors > 0 else 0.0

if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python clone_detection.py <file.py>")
        sys.exit(1)
    
    detector = CloneDetector(min_lines=6)
    clones = detector.detect_clones_in_file(sys.argv[1])
    
    report = detector.get_clone_report()
    
    print("="*60)
    print("CODE CLONE DETECTION REPORT")
    print("="*60)
    print(f"\nTotal Clones: {report['total_clones']}")
    print(f"Duplicated Lines: {report['total_duplicated_lines']}")
    print(f"\nBy Type: {report['clones_by_type']}")
    print(f"By Severity: {report['clones_by_severity']}")
    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    
    with open(sys.argv[1], 'r') as f:
        tree = ast.parse(f.read())
    
    semantic_detector = SemanticCloneDetector()
    semantic_clones = semantic_detector.detect_semantic_clones(tree)
    
    if semantic_clones:
        print(f"\n{'='*60}")
        print("SEMANTIC CLONES (Type 4)")
        print("="*60)
        for clone in semantic_clones:
            print(f"\n{clone['function1']} (line {clone['line1']}) ≈ "
                  f"{clone['function2']} (line {clone['line2']})")
            print(f"Similarity: {clone['similarity']:.1f}%")
