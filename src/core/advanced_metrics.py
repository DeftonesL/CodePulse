"""
Advanced Code Metrics Calculator
================================

Calculates sophisticated code quality metrics including:
- Cyclomatic Complexity
- Cognitive Complexity
- Maintainability Index
- Technical Debt
- Code Churn
- Halstead Metrics

Author: Saleh Almqati
License: MIT
"""

import ast
import json
import math
import re
from typing import Dict, List, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class HalsteadMetrics:
    """Halstead complexity metrics"""
    n1: int  # Number of distinct operators
    n2: int  # Number of distinct operands
    N1: int  # Total operators
    N2: int  # Total operands
    
    @property
    def vocabulary(self) -> int:
        """Program vocabulary"""
        return self.n1 + self.n2
    
    @property
    def length(self) -> int:
        """Program length"""
        return self.N1 + self.N2
    
    @property
    def calculated_length(self) -> float:
        """Calculated program length"""
        if self.n1 == 0 or self.n2 == 0:
            return 0
        return self.n1 * math.log2(self.n1) + self.n2 * math.log2(self.n2)
    
    @property
    def volume(self) -> float:
        """Program volume"""
        if self.vocabulary == 0:
            return 0
        return self.length * math.log2(self.vocabulary)
    
    @property
    def difficulty(self) -> float:
        """Program difficulty"""
        if self.n2 == 0 or self.N2 == 0:
            return 0
        return (self.n1 / 2) * (self.N2 / self.n2)
    
    @property
    def effort(self) -> float:
        """Programming effort"""
        return self.difficulty * self.volume
    
    @property
    def time_to_program(self) -> float:
        """Time required to program (seconds)"""
        return self.effort / 18  # Stroud number
    
    @property
    def bugs_delivered(self) -> float:
        """Estimated number of bugs"""
        return self.volume / 3000


@dataclass
class ComplexityMetrics:
    """Comprehensive complexity metrics"""
    cyclomatic_complexity: int
    cognitive_complexity: int
    essential_complexity: int
    max_nesting_depth: int
    average_complexity: float
    
    def get_score(self) -> float:
        """Calculate complexity score (0-100)"""
        score = 100
        
        # Penalize high cyclomatic complexity
        if self.cyclomatic_complexity > 50:
            score -= 30
        elif self.cyclomatic_complexity > 30:
            score -= 20
        elif self.cyclomatic_complexity > 15:
            score -= 10
        
        # Penalize high cognitive complexity
        if self.cognitive_complexity > 40:
            score -= 25
        elif self.cognitive_complexity > 25:
            score -= 15
        
        # Penalize deep nesting
        if self.max_nesting_depth > 5:
            score -= 15
        elif self.max_nesting_depth > 3:
            score -= 10
        
        return max(0, score)


@dataclass
class MaintainabilityMetrics:
    """Maintainability metrics"""
    maintainability_index: float
    comment_ratio: float
    documentation_ratio: float
    test_coverage_estimate: float
    
    def get_grade(self) -> str:
        """Get maintainability grade"""
        if self.maintainability_index >= 85:
            return "A - Highly Maintainable"
        elif self.maintainability_index >= 70:
            return "B - Moderately Maintainable"
        elif self.maintainability_index >= 50:
            return "C - Difficult to Maintain"
        else:
            return "D - Very Difficult to Maintain"


class AdvancedMetricsCalculator:
    """
    Calculate advanced code quality metrics.
    
    This goes beyond basic analysis to provide deep insights
    into code quality, maintainability, and technical debt.
    """
    
    def __init__(self):
        self.operators = set()
        self.operands = set()
        self.operator_count = 0
        self.operand_count = 0
    
    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dictionary with all metrics
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            # Calculate all metrics
            halstead = self.calculate_halstead_metrics(tree, code)
            complexity = self.calculate_complexity_metrics(tree)
            maintainability = self.calculate_maintainability_metrics(tree, code)
            
            # Calculate technical debt
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
        """Calculate Halstead complexity metrics"""
        operators = set()
        operands = set()
        operator_count = 0
        operand_count = 0
        
        # Python operators
        operator_nodes = (
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
            ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
            ast.FloorDiv, ast.And, ast.Or, ast.Eq, ast.NotEq,
            ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot,
            ast.In, ast.NotIn, ast.Not, ast.Invert, ast.UAdd, ast.USub
        )
        
        for node in ast.walk(tree):
            # Count operators
            if isinstance(node, operator_nodes):
                operators.add(type(node).__name__)
                operator_count += 1
            
            # Function/method calls are operators
            if isinstance(node, ast.Call):
                operators.add('Call')
                operator_count += 1
            
            # Assignments are operators
            if isinstance(node, (ast.Assign, ast.AugAssign)):
                operators.add('Assign')
                operator_count += 1
            
            # Count operands (variables, constants)
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
        """Calculate complexity metrics"""
        cyclomatic = self._calculate_cyclomatic_complexity(tree)
        cognitive = self._calculate_cognitive_complexity(tree)
        essential = self._calculate_essential_complexity(tree)
        max_depth = self._calculate_max_nesting_depth(tree)
        
        # Calculate average per function
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
        """Calculate McCabe's cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        decision_points = (
            ast.If, ast.While, ast.For, ast.ExceptHandler,
            ast.With, ast.Assert, ast.BoolOp
        )
        
        for node in ast.walk(tree):
            if isinstance(node, decision_points):
                complexity += 1
            
            # Each elif adds complexity
            if isinstance(node, ast.If) and node.orelse:
                if isinstance(node.orelse[0], ast.If):
                    complexity += 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, tree: ast.AST) -> int:
        """
        Calculate cognitive complexity (more human-centric than cyclomatic)
        """
        complexity = 0
        nesting_level = 0
        
        def visit_node(node, depth=0):
            nonlocal complexity, nesting_level
            
            # Nesting increments
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += (1 + depth)
                depth += 1
            
            # Logical operators add complexity
            if isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            
            # Recursion adds complexity
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    # Check if recursive (simplified check)
                    complexity += 1
            
            for child in ast.iter_child_nodes(node):
                visit_node(child, depth)
        
        visit_node(tree)
        return complexity
    
    def _calculate_essential_complexity(self, tree: ast.AST) -> int:
        """Calculate essential complexity (unstructured flow)"""
        # Simplified: count goto-like patterns
        complexity = 1
        
        for node in ast.walk(tree):
            # Break/continue in loops
            if isinstance(node, (ast.Break, ast.Continue)):
                complexity += 1
            
            # Multiple returns
            if isinstance(node, ast.Return):
                complexity += 1
        
        return complexity
    
    def _calculate_max_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nesting depth"""
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
        """Calculate maintainability metrics"""
        lines = code.split('\n')
        
        # Count comments
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        # Count docstrings
        docstring_count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if (ast.get_docstring(node)):
                    docstring_count += 1
        
        # Calculate ratios
        total_lines = len(lines)
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        
        comment_ratio = comment_lines / max(total_lines, 1)
        documentation_ratio = docstring_count / max(
            sum(1 for _ in ast.walk(tree) if isinstance(_, (ast.FunctionDef, ast.ClassDef))),
            1
        )
        
        # Calculate maintainability index
        # MI = 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(LOC)
        # Where V = Halstead Volume, G = Cyclomatic Complexity, LOC = Lines of Code
        
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
        
        # Estimate test coverage (simplified)
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
        """
        Estimate technical debt in minutes.
        
        Based on SQALE methodology:
        - High complexity = more time to understand and modify
        - Low maintainability = more refactoring needed
        """
        debt = 0
        
        # Complexity debt (minutes per complexity point over threshold)
        if complexity.cyclomatic_complexity > 10:
            debt += (complexity.cyclomatic_complexity - 10) * 5
        
        if complexity.cognitive_complexity > 15:
            debt += (complexity.cognitive_complexity - 15) * 3
        
        # Maintainability debt
        if maintainability.maintainability_index < 65:
            debt += (65 - maintainability.maintainability_index) * 2
        
        # Documentation debt
        if maintainability.documentation_ratio < 0.5:
            debt += (0.5 - maintainability.documentation_ratio) * 100
        
        # Size penalty (large files are harder to maintain)
        if lines_of_code > 500:
            debt += (lines_of_code - 500) * 0.1
        
        return debt
    
    def calculate_overall_score(
        self,
        complexity: ComplexityMetrics,
        maintainability: MaintainabilityMetrics
    ) -> float:
        """Calculate overall quality score (0-100)"""
        # Weighted average
        complexity_score = complexity.get_score()
        maintainability_score = maintainability.maintainability_index
        
        # 40% complexity, 60% maintainability
        overall = (complexity_score * 0.4) + (maintainability_score * 0.6)
        
        return round(overall, 2)


# Example usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python advanced_metrics.py <file.py>")
        sys.exit(1)
    
    calculator = AdvancedMetricsCalculator()
    results = calculator.analyze_python_file(sys.argv[1])
    
    print(json.dumps(results, indent=2))
