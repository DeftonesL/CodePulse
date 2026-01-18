import ast
import re
from typing import List, Dict, Any, Set
from dataclasses import dataclass
from enum import Enum

class PatternType(Enum):
    pass
    DESIGN_PATTERN = "design_pattern"
    ANTI_PATTERN = "anti_pattern"
    CODE_SMELL = "code_smell"
    BEST_PRACTICE = "best_practice"

class Severity(Enum):
    pass
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class DetectedPattern:
    pass
    name: str
    type: PatternType
    severity: Severity
    description: str
    location: str
    line: int
    recommendation: str
    example: str = ""

class CodePatternsDetector:
    pass
    
    def __init__(self):
        self.patterns: List[DetectedPattern] = []
    
    def analyze_file(self, file_path: str) -> List[DetectedPattern]:
        self.patterns = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            self._detect_design_patterns(tree, file_path)
            self._detect_anti_patterns(tree, file_path, code)
            self._detect_code_smells(tree, file_path, code)
            self._detect_best_practices(tree, file_path, code)
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return self.patterns
    
    def _detect_design_patterns(self, tree: ast.AST, file_path: str):
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                
                if '__new__' in methods or '_instance' in [
                    attr.target.id for attr in node.body 
                    if isinstance(attr, ast.Assign) 
                    and isinstance(attr.target, ast.Name)
                ]:
                    self.patterns.append(DetectedPattern(
                        name="Singleton Pattern",
                        type=PatternType.DESIGN_PATTERN,
                        severity=Severity.INFO,
                        description=f"Class '{class_name}' implements Singleton pattern",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Good! Singleton ensures single instance.",
                        example="class Singleton:\n    _instance = None\n    def __new__(cls):\n        if not cls._instance:\n            cls._instance = super().__new__(cls)\n        return cls._instance"
                    ))
                
                if 'create' in methods or 'factory' in class_name.lower():
                    self.patterns.append(DetectedPattern(
                        name="Factory Pattern",
                        type=PatternType.DESIGN_PATTERN,
                        severity=Severity.INFO,
                        description=f"Class '{class_name}' appears to be a Factory",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Good! Factory pattern promotes loose coupling.",
                        example="class Factory:\n    def create(self, type):\n        if type == 'A':\n            return ClassA()\n        return ClassB()"
                    ))
                
                if any(m.startswith('with_') or m.startswith('set_') for m in methods) and 'build' in methods:
                    self.patterns.append(DetectedPattern(
                        name="Builder Pattern",
                        type=PatternType.DESIGN_PATTERN,
                        severity=Severity.INFO,
                        description=f"Class '{class_name}' implements Builder pattern",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Excellent! Builder pattern creates complex objects step by step.",
                        example="class Builder:\n    def with_x(self, x):\n        self.x = x\n        return self\n    def build(self):\n        return Product()"
                    ))
    
    def _detect_anti_patterns(self, tree: ast.AST, file_path: str, code: str):
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
                attribute_count = sum(1 for n in node.body if isinstance(n, ast.Assign))
                
                if method_count > 20 or attribute_count > 15:
                    self.patterns.append(DetectedPattern(
                        name="God Class",
                        type=PatternType.ANTI_PATTERN,
                        severity=Severity.ERROR,
                        description=f"Class '{node.name}' has too many responsibilities ({method_count} methods, {attribute_count} attributes)",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Split this class into smaller, focused classes following Single Responsibility Principle.",
                        example="# Bad:\nclass GodClass:\n    # 20+ methods\n\n# Good:\nclass UserManager:\n    # User-related methods\nclass DataProcessor:\n    # Data-related methods"
                    ))
            
            if isinstance(node, ast.FunctionDef):
                function_lines = []
                for stmt in ast.walk(node):
                    if hasattr(stmt, 'lineno'):
                        function_lines.append(stmt.lineno)
                
                if len(function_lines) > 50:
                    self.patterns.append(DetectedPattern(
                        name="Long Method",
                        type=PatternType.ANTI_PATTERN,
                        severity=Severity.WARNING,
                        description=f"Function '{node.name}' is too long ({len(function_lines)} lines)",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Break down into smaller functions. Each function should do one thing.",
                        example="# Bad:\ndef do_everything():\n    # 50+ lines\n\n# Good:\ndef process():\n    validate()\n    transform()\n    save()"
                    ))
                
                param_count = len(node.args.args)
                if param_count > 5:
                    self.patterns.append(DetectedPattern(
                        name="Too Many Parameters",
                        type=PatternType.CODE_SMELL,
                        severity=Severity.WARNING,
                        description=f"Function '{node.name}' has {param_count} parameters",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Consider using a config object or dataclass to group parameters.",
                        example="# Bad:\ndef func(a, b, c, d, e, f):\n    pass\n\n# Good:\n@dataclass\nclass Config:\n    a: int\n    b: str\ndef func(config: Config):\n    pass"
                    ))
        
        lines = code.split('\n')
        line_counts = {}
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and len(stripped) > 20:
                if stripped in line_counts:
                    line_counts[stripped].append(i + 1)
                else:
                    line_counts[stripped] = [i + 1]
        
        for line_text, occurrences in line_counts.items():
            if len(occurrences) > 2:
                self.patterns.append(DetectedPattern(
                    name="Duplicated Code",
                    type=PatternType.CODE_SMELL,
                    severity=Severity.WARNING,
                    description=f"Code duplication detected ({len(occurrences)} times)",
                    location=file_path,
                    line=occurrences[0],
                    recommendation="Extract duplicated code into a reusable function or method.",
                    example="# Bad:\nif x:\n    process(data)\nif y:\n    process(data)\n\n# Good:\ndef handle(condition):\n    if condition:\n        process(data)\nhandle(x)\nhandle(y)"
                ))
    
    def _detect_code_smells(self, tree: ast.AST, file_path: str, code: str):
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    if node.value not in [0, 1, -1, 2, 10, 100, 1000]:
                        self.patterns.append(DetectedPattern(
                            name="Magic Number",
                            type=PatternType.CODE_SMELL,
                            severity=Severity.INFO,
                            description=f"Magic number '{node.value}' found without explanation",
                            location=file_path,
                            line=node.lineno,
                            recommendation="Define constants with meaningful names.",
                            example=f"# Bad:\nif x > {node.value}:\n\n# Good:\nMAX_LIMIT = {node.value}\nif x > MAX_LIMIT:"
                        ))
            
            if isinstance(node, ast.If):
                depth = self._calculate_nesting_depth(node)
                if depth > 3:
                    self.patterns.append(DetectedPattern(
                        name="Deeply Nested If",
                        type=PatternType.CODE_SMELL,
                        severity=Severity.WARNING,
                        description=f"If statement nested {depth} levels deep",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Flatten nested conditions using early returns or guard clauses.",
                        example="# Bad:\nif a:\n    if b:\n        if c:\n            do()\n\n# Good:\nif not a:\n    return\nif not b:\n    return\nif c:\n    do()"
                    ))
            
            if isinstance(node, ast.ExceptHandler):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    self.patterns.append(DetectedPattern(
                        name="Empty Except Block",
                        type=PatternType.CODE_SMELL,
                        severity=Severity.ERROR,
                        description="Catch-all exception handler with no action",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Log the exception or handle it properly. Never silently catch all exceptions.",
                        example="# Bad:\ntry:\n    risky()\nexcept:\n    pass\n\n# Good:\ntry:\n    risky()\nexcept SpecificError as e:\n    logger.error(f'Error: {e}')"
                    ))
    
    def _detect_best_practices(self, tree: ast.AST, file_path: str, code: str):
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if not docstring and not node.name.startswith('_'):
                    self.patterns.append(DetectedPattern(
                        name="Missing Docstring",
                        type=PatternType.BEST_PRACTICE,
                        severity=Severity.INFO,
                        description=f"Function '{node.name}' lacks docstring",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Add a docstring explaining what the function does, its parameters, and return value.",
                        example='def func(x: int) -> str:\n    """Convert int to string.\n    \n    Args:\n        x: Number to convert\n        \n    Returns:\n        String representation\n    """\n    return str(x)'
                    ))
                
                has_type_hints = (
                    node.returns is not None or 
                    any(arg.annotation for arg in node.args.args)
                )
                
                if not has_type_hints and not node.name.startswith('_'):
                    self.patterns.append(DetectedPattern(
                        name="Missing Type Hints",
                        type=PatternType.BEST_PRACTICE,
                        severity=Severity.INFO,
                        description=f"Function '{node.name}' lacks type hints",
                        location=file_path,
                        line=node.lineno,
                        recommendation="Add type hints for better code clarity and IDE support.",
                        example="# Bad:\ndef add(a, b):\n    return a + b\n\n# Good:\ndef add(a: int, b: int) -> int:\n    return a + b"
                    ))
    
    def _calculate_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        max_depth = depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                child_depth = self._calculate_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def get_summary(self) -> Dict[str, Any]:
        summary = {
            'total_patterns': len(self.patterns),
            'by_type': {},
            'by_severity': {},
            'critical_issues': []
        }
        
        for pattern in self.patterns:
            type_key = pattern.type.value
            summary['by_type'][type_key] = summary['by_type'].get(type_key, 0) + 1
            
            sev_key = pattern.severity.value
            summary['by_severity'][sev_key] = summary['by_severity'].get(sev_key, 0) + 1
            
            if pattern.severity in [Severity.ERROR, Severity.CRITICAL]:
                summary['critical_issues'].append({
                    'name': pattern.name,
                    'line': pattern.line,
                    'description': pattern.description
                })
        
        return summary

if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python code_patterns.py <file.py>")
        sys.exit(1)
    
    detector = CodePatternsDetector()
    patterns = detector.analyze_file(sys.argv[1])
    
    print(f"\nFound {len(patterns)} patterns:\n")
    for p in patterns:
        print(f"[{p.severity.value.upper()}] {p.name} at line {p.line}")
        print(f"  {p.description}")
        print(f"  💡 {p.recommendation}\n")
    
    print("\nSummary:")
    print(json.dumps(detector.get_summary(), indent=2))
