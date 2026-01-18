import ast
import math
import re
import json
from typing import Dict, List, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class HalsteadMetrics:
    pass
    n1: int  # Number of distinct operators
    n2: int  # Number of distinct operands
    N1: int  # Total operators
    N2: int  # Total operands
    
    @property
    def vocabulary(self) -> int:
        return self.n1 + self.n2
    
    @property
    def length(self) -> int:
        return self.N1 + self.N2
    
    @property
    def calculated_length(self) -> float:
        if self.n1 == 0 or self.n2 == 0:
            return 0
        return self.n1 * math.log2(self.n1) + self.n2 * math.log2(self.n2)
    
    @property
    def volume(self) -> float:
        if self.vocabulary == 0:
            return 0
        return self.length * math.log2(self.vocabulary)
    
    @property
    def difficulty(self) -> float:
        if self.n2 == 0 or self.N2 == 0:
            return 0
        return (self.n1 / 2) * (self.N2 / self.n2)
    
    @property
    def effort(self) -> float:
        return self.difficulty * self.volume
    
    @property
    def time_to_program(self) -> float:
        return self.effort / 18  # Stroud number
    
    @property
    def bugs_delivered(self) -> float:
        return self.volume / 3000

@dataclass
class ComplexityMetrics:
    pass
    cyclomatic_complexity: int
    cognitive_complexity: int
    essential_complexity: int
    max_nesting_depth: int
    average_complexity: float
    
    def get_score(self) -> float:
        score = 100
        
        if self.cyclomatic_complexity > 50:
            score -= 30
        elif self.cyclomatic_complexity > 30:
            score -= 20
        elif self.cyclomatic_complexity > 15:
            score -= 10
        
        if self.cognitive_complexity > 40:
            score -= 25
        elif self.cognitive_complexity > 25:
            score -= 15
        
        if self.max_nesting_depth > 5:
            score -= 15
        elif self.max_nesting_depth > 3:
            score -= 10
        
        return max(0, score)

@dataclass
class MaintainabilityMetrics:
    pass
    maintainability_index: float
    comment_ratio: float
    documentation_ratio: float
    test_coverage_estimate: float
    
    def get_grade(self) -> str:
        if self.maintainability_index >= 85:
            return "A - Highly Maintainable"
        elif self.maintainability_index >= 70:
            return "B - Moderately Maintainable"
        elif self.maintainability_index >= 50:
            return "C - Difficult to Maintain"
        else:
            return "D - Very Difficult to Maintain"

class AdvancedMetricsCalculator:
    pass
    
    def __init__(self):
        self.operators = set()
        self.operands = set()
        self.operator_count = 0
        self.operand_count = 0
    
    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            halstead = self.calculate_halstead_metrics(tree, code)
            complexity = self.calculate_complexity_metrics(tree)
            maintainability = self.calculate_maintainability_metrics(tree, code)
            
            tech_debt = self.estimate_technical_debt(
                complexity, maintainability, len(code.split('\n'))
            )
            
            return {
                'halstead': asdict(halstead) if hasattr(halstead, '__dataclass_fields__') else halstead,
                'complexity': asdict(complexity) if hasattr(complexity, '__dataclass_fields__') else complexity,
                'maintainability': asdict(maintainability) if hasattr(maintainability, '__dataclass_fields__') else maintainability,
                'technical_debt_minutes': tech_debt,
                'technical_debt_hours': tech_debt / 60,
                'overall_quality_score': self.calculate_overall_score(
                    complexity, maintainability
                )
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_halstead_metrics(self, tree: ast.AST, code: str) -> HalsteadMetrics:
        operators = set()
        operands = set()
        operator_count = 0
        operand_count = 0
        
        operator_nodes = (
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
            ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
            ast.FloorDiv, ast.And, ast.Or, ast.Eq, ast.NotEq,
            ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot,
            ast.In, ast.NotIn, ast.Not, ast.Invert, ast.UAdd, ast.USub
        )
        
        for node in ast.walk(tree):
            if isinstance(node, operator_nodes):
                operators.add(type(node).__name__)
                operator_count += 1
            
            if isinstance(node, ast.Call):
                operators.add('Call')
                operator_count += 1
            
            if isinstance(node, (ast.Assign, ast.AugAssign)):
                operators.add('Assign')
                operator_count += 1
            
            if isinstance(node, ast.Name):
                operands.add(node.id)
                operand_count += 1
            
            if isinstance(node, (ast.Constant, ast.Num, ast.Str)):
                operands.add(str(node))
                operand_count += 1
        
        return HalsteadMetrics(
            n1=len(operators),
            n2=len(operands),
            N1=operator_count,
            N2=operand_count
        )
    
    def calculate_complexity_metrics(self, tree: ast.AST) -> ComplexityMetrics:
        cyclomatic = self._calculate_cyclomatic_complexity(tree)
        cognitive = self._calculate_cognitive_complexity(tree)
        essential = self._calculate_essential_complexity(tree)
        max_depth = self._calculate_max_nesting_depth(tree)
        
        function_count = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.FunctionDef))
        avg_complexity = cyclomatic / max(function_count, 1)
        
        return ComplexityMetrics(
            cyclomatic_complexity=cyclomatic,
            cognitive_complexity=cognitive,
            essential_complexity=essential,
            max_nesting_depth=max_depth,
            average_complexity=avg_complexity
        )
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        complexity = 1  # Base complexity
        
        decision_points = (
            ast.If, ast.While, ast.For, ast.ExceptHandler,
            ast.With, ast.Assert, ast.BoolOp
        )
        
        for node in ast.walk(tree):
            if isinstance(node, decision_points):
                complexity += 1
            
            if isinstance(node, ast.If) and node.orelse:
                if isinstance(node.orelse[0], ast.If):
                    complexity += 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, tree: ast.AST) -> int:
        complexity = 0
        nesting_level = 0
        
        def visit_node(node, depth=0):
            nonlocal complexity, nesting_level
            
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += (1 + depth)
                depth += 1
            
            if isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    complexity += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
        
        visit_node(tree)
        return complexity
    
    def _calculate_essential_complexity(self, tree: ast.AST) -> int:
        complexity = 1
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Break, ast.Continue)):
                complexity += 1
            
            if isinstance(node, ast.Return):
                complexity += 1
        
        return complexity
    
    def _calculate_max_nesting_depth(self, tree: ast.AST) -> int:
        max_depth = 0
        
        def visit_node(node, depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                depth += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
        
        visit_node(tree)
        return max_depth
    
    def calculate_maintainability_metrics(
        self, tree: ast.AST, code: str
    ) -> MaintainabilityMetrics:
        lines = code.split('\n')
        
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        docstring_count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if (ast.get_docstring(node)):
                    docstring_count += 1
        
        total_lines = len(lines)
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        
        comment_ratio = comment_lines / max(total_lines, 1)
        documentation_ratio = docstring_count / max(
            sum(1 for _ in ast.walk(tree) if isinstance(_, (ast.FunctionDef, ast.ClassDef))),
            1
        )
        
        
        halstead = self.calculate_halstead_metrics(tree, code)
        complexity = self._calculate_cyclomatic_complexity(tree)
        
        if halstead.volume > 0 and code_lines > 0:
            mi = (
                171 
                - 5.2 * math.log(halstead.volume)
                - 0.23 * complexity
                - 16.2 * math.log(code_lines)
            )
            mi = max(0, min(100, mi))  # Normalize to 0-100
        else:
            mi = 50  # Default
        
        test_count = sum(1 for node in ast.walk(tree) 
                        if isinstance(node, ast.FunctionDef) 
                        and node.name.startswith('test_'))
        function_count = sum(1 for node in ast.walk(tree) 
                           if isinstance(node, ast.FunctionDef))
        test_coverage = (test_count / max(function_count, 1)) * 100
        
        return MaintainabilityMetrics(
            maintainability_index=mi,
            comment_ratio=comment_ratio,
            documentation_ratio=documentation_ratio,
            test_coverage_estimate=min(test_coverage, 100)
        )
    
    def estimate_technical_debt(
        self,
        complexity: ComplexityMetrics,
        maintainability: MaintainabilityMetrics,
        lines_of_code: int
    ) -> float:
        debt = 0
        
        if complexity.cyclomatic_complexity > 10:
            debt += (complexity.cyclomatic_complexity - 10) * 5
        
        if complexity.cognitive_complexity > 15:
            debt += (complexity.cognitive_complexity - 15) * 3
        
        if maintainability.maintainability_index < 65:
            debt += (65 - maintainability.maintainability_index) * 2
        
        if maintainability.documentation_ratio < 0.5:
            debt += (0.5 - maintainability.documentation_ratio) * 100
        
        if lines_of_code > 500:
            debt += (lines_of_code - 500) * 0.1
        
        return debt
    
    def calculate_overall_score(
        self,
        complexity: ComplexityMetrics,
        maintainability: MaintainabilityMetrics
    ) -> float:
        complexity_score = complexity.get_score()
        maintainability_score = maintainability.maintainability_index
        
        overall = (complexity_score * 0.4) + (maintainability_score * 0.6)
        
        return round(overall, 2)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python advanced_metrics.py <file.py>")
        sys.exit(1)
    
    calculator = AdvancedMetricsCalculator()
    results = calculator.analyze_python_file(sys.argv[1])
    
    print(json.dumps(results, indent=2))
