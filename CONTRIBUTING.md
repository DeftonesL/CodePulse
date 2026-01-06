# Contributing to CodePulse

Welcome! CodePulse is built on deep understanding of algorithms and software engineering principles.

## 🎯 Project Philosophy

**We Build from Scratch, Not Wrap Existing Tools**
- Custom algorithms from research papers
- Educational code that explains concepts
- Optimized and thoughtful performance

**Quality Over Speed**
- Every algorithm documented with time complexity
- Every function includes examples
- Comprehensive tests for every feature

---

## 🚀 Getting Started

```bash
# Fork and Clone
git clone https://github.com/YOUR_USERNAME/CodePulse.git
cd CodePulse

# Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Installation
pip install -e .
pip install -e .[dev]

# Verify Setup
pytest tests/
```

---

## 📝 Code Standards

### Type Hints Required

```python
# Correct ✅
def analyze_function(tree: ast.FunctionDef, context: AnalysisContext) -> List[Issue]:
    """Analyze function for issues."""
    pass

# Wrong ❌
def analyze_function(tree, context):
    pass
```

### Docstrings Required with Examples

```python
def calculate_complexity(tree: ast.AST) -> ComplexityMetrics:
    """
    Calculate code complexity metrics.
    
    Time Complexity: O(n)
    Space Complexity: O(d) where d = max depth
    
    Args:
        tree: Abstract syntax tree root
        
    Returns:
        ComplexityMetrics with cyclomatic, cognitive scores
        
    Example:
        >>> tree = ast.parse("def foo(): pass")
        >>> calculate_complexity(tree).cyclomatic
        1
        
    Reference:
        McCabe, T. (1976). IEEE Transactions on Software Engineering
    """
    pass
```

---

## 🧪 Testing

```python
import pytest

class TestDeepAnalysis:
    def test_control_flow_simple(self):
        """Test CFG for simple function."""
        code = "def foo():\n    return 1"
        tree = ast.parse(code)
        engine = DeepAnalysisEngine()
        engine.build_control_flow_graph(tree)
        
        assert engine.cfg.number_of_nodes() == 2
    
    @pytest.mark.parametrize("code,expected", [
        ("def foo(): pass", 1),
        ("def foo():\n if x: pass", 2),
    ])
    def test_complexity_levels(self, code, expected):
        tree = ast.parse(code)
        assert calculate_complexity(tree) >= expected
```

**Coverage Requirements:**
- All public functions: 100%
- Edge cases tested
- Performance measured

---

## ✨ Adding New Features

### New Analysis Algorithm

**1. Research First**
- Read research papers
- Understand time and space complexity
- Plan test cases

**2. Implementation with Documentation**
```python
def detect_feature_envy(tree: ast.AST) -> List[CodeSmell]:
    """
    Detect Feature Envy code smell.
    
    Method uses another class more than its own.
    
    Detection:
    - Count self.* accesses
    - Count other.* accesses  
    - If other > self + threshold, flag
    
    Time: O(n), Space: O(1)
    Reference: Fowler, M. "Refactoring" Ch. 3
    """
    # Implementation here
    pass
```

**3. Tests**
```python
def test_feature_envy_detection():
    code = """
class A:
    def method(self, b):
        b.x()
        b.y()
        b.z()  # Uses 'b' more than 'self'
"""
    smells = detect_feature_envy(ast.parse(code))
    assert len(smells) > 0
    assert smells[0].name == "Feature Envy"
```

---

## 🐛 Bug Reports

Use this template:

```markdown
**Description**
Clear and concise description of the issue

**Steps to Reproduce**
1. Create file: `example.py`
2. Run: `codepulse analyze example.py`
3. Error appears

**Expected vs Actual**
Expected: Should detect X
Actual: Crashes with error Y

**Code Sample**
```python
def problematic_code():
    pass
```

**Environment**
- OS: macOS 14.0
- Python: 3.11.5
- CodePulse: v0.5.0
```

---

## ✅ Pull Request Checklist

```
Code:
☐ PEP 8 compliant
☐ Type hints on all functions
☐ Docstrings with examples
☐ Time complexity documented
☐ No commented code
☐ Use logging instead of print()

Tests:
☐ All tests passing
☐ New tests for new code
☐ Coverage >= 75%
☐ Edge cases tested

Documentation:
☐ README updated
☐ CHANGELOG.md updated
☐ Algorithm references added
☐ Examples provided

Git:
☐ Descriptive branch name
☐ Logical commits
☐ Complete PR description
```
