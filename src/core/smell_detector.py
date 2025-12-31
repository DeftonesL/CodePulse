"""
Intelligent Code Smell Detector
================================

Advanced code smell detection using pattern matching and heuristics.
Goes beyond simple rule-based detection to understand context.

Custom algorithms for detecting subtle code quality issues.

Author: Saleh Almqati
"""

import ast
import re
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass
from collections import Counter, defaultdict
import math


@dataclass
class CodeSmell:
    """Represents a detected code smell"""
    name: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # Complexity, Coupling, Cohesion, Size, etc.
    description: str
    location: str
    line: int
    impact: str
    refactoring_suggestion: str
    code_example: str = ""


class IntelligentSmellDetector:
    """
    Detects code smells using intelligent analysis.
    
    Not just simple pattern matching - uses context-aware detection.
    """
    
    # Standard Python modules to ignore in Feature Envy detection
    STANDARD_MODULES = {
        'sys', 'os', 'ast', 're', 'json', 'time', 'datetime', 'pathlib',
        'logging', 'typing', 'collections', 'itertools', 'functools',
        'argparse', 'subprocess', 'shutil', 'tempfile', 'urllib', 'requests',
        'math', 'random', 'string', 'hashlib', 'base64', 'pickle', 'csv',
        'xml', 'html', 'email', 'http', 'socket', 'threading', 'multiprocessing',
        'unittest', 'pytest', 'click', 'console', 'table', 'structure', 'logger',
        'flask', 'django', 'numpy', 'pandas', 'matplotlib', 'seaborn', 'result',
    }
    
    # Relaxed thresholds for more realistic detection
    LONG_METHOD_THRESHOLD = 80  # More realistic (was 50)
    LARGE_CLASS_THRESHOLD = 500  # More realistic (was 200)
    LONG_PARAMETER_LIST = 6  # Reasonable (was 5)
    
    def __init__(self):
        self.smells = []
        self.metrics = {}
        
    def detect_smells(self, file_path: str) -> List[CodeSmell]:
        """
        Detect all code smells in a file.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        try:
            tree = ast.parse(code)
        except:
            return []
        
        # Calculate file-level metrics first
        self._calculate_file_metrics(tree, code)
        
        # Detect different types of smells
        self._detect_bloater_smells(tree, file_path)
        self._detect_oo_abuser_smells(tree, file_path)
        self._detect_change_preventer_smells(tree, file_path)
        self._detect_dispensable_smells(tree, file_path)
        self._detect_coupler_smells(tree, file_path)
        
        return self.smells
    
    def _calculate_file_metrics(self, tree: ast.AST, code: str):
        """
        Calculate comprehensive metrics for the file.
        """
        lines = code.split('\n')
        
        self.metrics = {
            'total_lines': len(lines),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'blank_lines': len([l for l in lines if not l.strip()]),
            'functions': 0,
            'classes': 0,
            'max_function_length': 0,
            'avg_function_length': 0,
            'max_class_size': 0,
            'total_complexity': 0
        }
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.metrics['functions'] += 1
                length = (node.end_lineno or node.lineno) - node.lineno
                functions.append(length)
                
            elif isinstance(node, ast.ClassDef):
                self.metrics['classes'] += 1
                size = (node.end_lineno or node.lineno) - node.lineno
                classes.append(size)
        
        if functions:
            self.metrics['max_function_length'] = max(functions)
            self.metrics['avg_function_length'] = sum(functions) / len(functions)
        
        if classes:
            self.metrics['max_class_size'] = max(classes)
    
    def _detect_bloater_smells(self, tree: ast.AST, file_path: str):
        """
        Detect "Bloater" smells (large structures).
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Long Method - using relaxed threshold
                length = (node.end_lineno or node.lineno) - node.lineno
                if length > self.LONG_METHOD_THRESHOLD:
                    self.smells.append(CodeSmell(
                        name="Long Method",
                        severity="HIGH" if length > 150 else "MEDIUM",
                        category="Bloater",
                        description=f"Function '{node.name}' is {length} lines long",
                        location=file_path,
                        line=node.lineno,
                        impact=f"Difficult to understand and maintain. Higher bug probability.",
                        refactoring_suggestion=f"Extract smaller methods. Aim for < {self.LONG_METHOD_THRESHOLD} lines per function.",
                        code_example=f"""# Current: {length} lines
def {node.name}(...):
    # Too much code here

# Refactor to:
def {node.name}(...):
    step1()
    step2()
    step3()

def step1(): ...
def step2(): ...
def step3(): ..."""
                    ))
                
                # Long Parameter List - using relaxed threshold
                param_count = len(node.args.args)
                if param_count > self.LONG_PARAMETER_LIST:
                    self.smells.append(CodeSmell(
                        name="Long Parameter List",
                        severity="MEDIUM",
                        category="Bloater",
                        description=f"Function '{node.name}' has {param_count} parameters",
                        location=file_path,
                        line=node.lineno,
                        impact="Hard to call, understand, and maintain.",
                        refactoring_suggestion="Use parameter objects or configuration classes.",
                        code_example=f"""# Bad:
def {node.name}(a, b, c, d, e, f): ...

# Good:
@dataclass
class Config:
    a: type
    b: type
    # ...

def {node.name}(config: Config): ..."""
                    ))
            
            elif isinstance(node, ast.ClassDef):
                # Large Class - using relaxed threshold
                size = (node.end_lineno or node.lineno) - node.lineno
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                
                if size > self.LARGE_CLASS_THRESHOLD or len(methods) > 25:
                    self.smells.append(CodeSmell(
                        name="Large Class",
                        severity="HIGH",
                        category="Bloater",
                        description=f"Class '{node.name}' has {size} lines and {len(methods)} methods",
                        location=file_path,
                        line=node.lineno,
                        impact="Violates Single Responsibility Principle. Hard to maintain.",
                        refactoring_suggestion="Split into smaller, focused classes.",
                        code_example=f"""# Current: {size} lines, {len(methods)} methods
class {node.name}:
    # Too many responsibilities

# Refactor to:
class {node.name}Handler:
    # Handles X
    
class {node.name}Processor:
    # Processes Y
    
class {node.name}Validator:
    # Validates Z"""
                    ))
    
    def _detect_oo_abuser_smells(self, tree: ast.AST, file_path: str):
        """
        Detect Object-Oriented abuse smells.
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self_assignments = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Attribute):
                        if isinstance(child.ctx, ast.Store):
                            if isinstance(child.value, ast.Name):
                                if child.value.id == 'self':
                                    self_assignments.append(child.attr)
                
                foreign_access = 0
                for child in ast.walk(node):
                    if isinstance(child, ast.Attribute):
                        if isinstance(child.value, ast.Name):
                            if child.value.id != 'self':
                                foreign_access += 1
                
                if foreign_access > 5:
                    self.smells.append(CodeSmell(
                        name="Inappropriate Intimacy",
                        severity="MEDIUM",
                        category="OO Abuser",
                        description=f"Function '{node.name}' accesses other objects' internals {foreign_access} times",
                        location=file_path,
                        line=node.lineno,
                        impact="Tight coupling. Changes in one class break another.",
                        refactoring_suggestion="Use proper encapsulation. Add methods instead of accessing fields.",
                        code_example="""# Bad:
def process(self, other):
    x = other.field1
    y = other.field2
    z = other._internal_field  # Accessing internals!

# Good:
def process(self, other):
    x = other.get_field1()
    y = other.get_field2()
    # Don't access internals"""
                    ))
    
    def _detect_change_preventer_smells(self, tree: ast.AST, file_path: str):
        """
        Detect smells that prevent easy changes.
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Count different types of operations
                operation_types = set()
                
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        # Categorize by name patterns
                        name = child.name.lower()
                        if 'get' in name or 'set' in name:
                            operation_types.add('accessors')
                        elif 'save' in name or 'load' in name or 'read' in name or 'write' in name:
                            operation_types.add('persistence')
                        elif 'validate' in name or 'check' in name:
                            operation_types.add('validation')
                        elif 'calculate' in name or 'compute' in name:
                            operation_types.add('computation')
                        elif 'format' in name or 'render' in name or 'display' in name:
                            operation_types.add('presentation')
                
                if len(operation_types) > 3:
                    self.smells.append(CodeSmell(
                        name="Divergent Change",
                        severity="HIGH",
                        category="Change Preventer",
                        description=f"Class '{node.name}' handles {len(operation_types)} different responsibilities",
                        location=file_path,
                        line=node.lineno,
                        impact="Changes for different reasons. Hard to maintain.",
                        refactoring_suggestion="Split into separate classes, each with one responsibility.",
                        code_example=f"""# Current - multiple responsibilities:
class {node.name}:
    def save_to_db(): ...      # Persistence
    def validate(): ...         # Validation
    def calculate(): ...        # Business logic
    def render_html(): ...      # Presentation

# Refactor to:
class {node.name}Repository:  # Persistence
    def save(): ...
    
class {node.name}Validator:   # Validation
    def validate(): ...
    
class {node.name}:             # Business logic
    def calculate(): ...
    
class {node.name}Presenter:   # Presentation
    def render_html(): ..."""
                    ))
    
    def _detect_dispensable_smells(self, tree: ast.AST, file_path: str):
        """
        Detect unnecessary code.
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Lazy Class (class that doesn't do enough)
                if isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    real_methods = [m for m in methods if m.name not in ['__init__', '__str__', '__repr__']]
                    
                    if len(real_methods) < 2:
                        self.smells.append(CodeSmell(
                            name="Lazy Class",
                            severity="LOW",
                            category="Dispensable",
                            description=f"Class '{node.name}' only has {len(real_methods)} method(s)",
                            location=file_path,
                            line=node.lineno,
                            impact="Unnecessary abstraction. Adds complexity without value.",
                            refactoring_suggestion="Remove class and inline functionality, or add more behavior.",
                            code_example=f"""# Current:
class {node.name}:
    def __init__(self, x):
        self.x = x
    
    def get_x(self):
        return self.x

# Refactor: Just use the value directly
# Or add more meaningful behavior to justify the class"""
                        ))
                
                # Speculative Generality (unused abstraction)
                # Dead Code
                docstring = ast.get_docstring(node)
                if docstring and 'deprecated' in docstring.lower():
                    self.smells.append(CodeSmell(
                        name="Dead Code",
                        severity="MEDIUM",
                        category="Dispensable",
                        description=f"Function '{node.name}' is marked as deprecated",
                        location=file_path,
                        line=node.lineno,
                        impact="Confuses developers. May be accidentally used.",
                        refactoring_suggestion="Remove deprecated code or migrate callers.",
                        code_example=f"""# Remove this:
def {node.name}(...):
    '''DEPRECATED: Use new_function instead'''
    ...

# Or properly deprecate with warnings:
import warnings

@deprecated
def {node.name}(...):
    warnings.warn("Use new_function", DeprecationWarning)
    ..."""
                    ))
    
    def _detect_coupler_smells(self, tree: ast.AST, file_path: str):
        """
        Detect coupling smells.
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count self vs other access
                self_access = 0
                other_access = defaultdict(int)
                
                for child in ast.walk(node):
                    if isinstance(child, ast.Attribute):
                        if isinstance(child.value, ast.Name):
                            if child.value.id == 'self':
                                self_access += 1
                            else:
                                other_access[child.value.id] += 1
                
                # Check for envy - but ignore standard modules
                for other_obj, count in other_access.items():
                    # Skip if it's a standard module
                    if other_obj.lower() in self.STANDARD_MODULES:
                        continue
                    
                    # Skip single-letter variables (likely loop variables)
                    if len(other_obj) == 1:
                        continue
                    
                    if count > self_access and count > 5:  # Increased threshold
                        self.smells.append(CodeSmell(
                            name="Feature Envy",
                            severity="MEDIUM",
                            category="Coupler",
                            description=f"Function '{node.name}' uses '{other_obj}' more than 'self'",
                            location=file_path,
                            line=node.lineno,
                            impact="Method is in the wrong class. Poor cohesion.",
                            refactoring_suggestion=f"Move this method to the '{other_obj}' class.",
                            code_example=f"""# Current (in wrong class):
class A:
    def {node.name}(self, other):
        x = other.field1
        y = other.field2
        return other.method1() + other.method2()

# Move to correct class:
class B:  # The 'other' class
    def {node.name}(self):
        x = self.field1
        y = self.field2
        return self.method1() + self.method2()"""
                        ))
    
    def get_smell_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive smell report.
        """
        if not self.smells:
            return {
                'total_smells': 0,
                'by_severity': {},
                'by_category': {},
                'code_health_score': 100.0,
                'recommendations': ['No code smells detected! Excellent code quality.']
            }
        
        # Categorize
        by_severity = Counter(s.severity for s in self.smells)
        by_category = Counter(s.category for s in self.smells)
        
        # Calculate health score
        score = 100.0
        for smell in self.smells:
            if smell.severity == 'CRITICAL':
                score -= 15
            elif smell.severity == 'HIGH':
                score -= 10
            elif smell.severity == 'MEDIUM':
                score -= 5
            elif smell.severity == 'LOW':
                score -= 2
        
        score = max(0, score)
        
        # Generate recommendations
        recommendations = []
        
        if by_severity['HIGH'] > 0 or by_severity.get('CRITICAL', 0) > 0:
            recommendations.append(
                "PRIORITY: Address high/critical severity smells first."
            )
        
        if by_category['Bloater'] > 3:
            recommendations.append(
                "Bloater smells detected. Refactor large methods and classes."
            )
        
        if by_category['Coupler'] > 2:
            recommendations.append(
                "Coupling issues found. Review class responsibilities and boundaries."
            )
        
        return {
            'total_smells': len(self.smells),
            'by_severity': dict(by_severity),
            'by_category': dict(by_category),
            'code_health_score': round(score, 1),
            'smells': [
                {
                    'name': s.name,
                    'severity': s.severity,
                    'category': s.category,
                    'description': s.description,
                    'line': s.line,
                    'impact': s.impact,
                    'refactoring': s.refactoring_suggestion
                }
                for s in self.smells
            ],
            'recommendations': recommendations,
            'metrics': self.metrics
        }


# Example usage
if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python smell_detector.py <file.py>")
        sys.exit(1)
    
    detector = IntelligentSmellDetector()
    smells = detector.detect_smells(sys.argv[1])
    
    report = detector.get_smell_report()
    
    print("="*70)
    print("INTELLIGENT CODE SMELL ANALYSIS")
    print("="*70)
    print(f"\nCode Health Score: {report['code_health_score']}/100")
    print(f"Total Smells: {report['total_smells']}")
    print(f"\nBy Severity: {report['by_severity']}")
    print(f"By Category: {report['by_category']}")
    
    if report['smells']:
        print(f"\nDetailed Smells:")
        for smell in report['smells']:
            print(f"\n[{smell['severity']}] {smell['name']} (Line {smell['line']})")
            print(f"  Category: {smell['category']}")
            print(f"  Impact: {smell['impact']}")
            print(f"  Fix: {smell['refactoring']}")
    
    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
