# Contributing to CodePulse

Welcome! CodePulse is built on deep understanding of algorithms and software engineering principles, not wrapping existing tools.

## 🎯 Philosophy

### What Makes CodePulse Different

**We Build, Not Wrap**
- Custom algorithms from research papers
- Deep understanding of complexity
- Educational code that teaches
- Performance-conscious implementations

**Quality Over Speed**
- Every algorithm documented with complexity
- Every function has examples
- Every metric has mathematical foundation
- Every feature thoroughly tested

---

## 🚀 Getting Started

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/CodePulse.git
cd CodePulse

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e .
pip install -e .[dev]

# Verify
pytest tests/
```

### Project Structure

```
CodePulse/
├── src/core/          # Analysis engines
│   ├── deep_analysis.py        # CFG, DFG (543 lines)
│   ├── clone_detection.py      # 4-type clones (466 lines)
│   ├── smell_detector.py       # Context-aware (505 lines)
│   └── ...
├── src/modules/       # Security, etc.
├── docs/             # Documentation
└── tests/            # Test suite
```

---

## 📝 Code Standards

### Python Style

**Type Hints Required**
```python
# Good ✅
def analyze_function(
    tree: ast.FunctionDef,
    context: AnalysisContext
) -> List[Issue]:
    """Analyze function for issues."""
    pass

# Bad ❌
def analyze_function(tree, context):
    pass
```

**Docstrings Required**
```python
def calculate_complexity(tree: ast.AST) -> ComplexityMetrics:
    """
    Calculate code complexity metrics.
    
    Implements McCabe's cyclomatic complexity plus
    cognitive complexity based on nesting depth.
    
    Time Complexity: O(n)
    Space Complexity: O(d) where d = max depth
    
    Args:
        tree: Abstract syntax tree root
        
    Returns:
        ComplexityMetrics with cyclomatic, cognitive scores
        
    Raises:
        ValueError: If tree is invalid
        
    Example:
        >>> tree = ast.parse("def foo(): pass")
        >>> m = calculate_complexity(tree)
        >>> m.cyclomatic
        1
        
    Reference:
        McCabe, T. (1976). "A Complexity Measure"
        IEEE Transactions on Software Engineering
    """
    pass
```

**Complexity Analysis Required**
```python
def detect_clones(lines: List[str]) -> List[Clone]:
    """
    Detect code clones using rolling hash.
    
    Time Complexity: O(n) where n = number of lines
    Space Complexity: O(n) for hash table
    
    Algorithm:
        1. Create sliding window size W
        2. Hash each window using rolling hash
        3. Store hash -> line mapping
        4. Check collisions for exact match
        
    Based on: Rabin-Karp string matching
    Reference: Cormen et al., Ch. 32
    """
    pass
```

---

## 🧪 Testing Standards

**Comprehensive Tests**
```python
import pytest

class TestDeepAnalysis:
    def setup_method(self):
        self.engine = DeepAnalysisEngine()
    
    def test_control_flow_simple(self):
        """Test CFG for simple function."""
        code = "def foo():\n    return 1"
        tree = ast.parse(code)
        self.engine.build_control_flow_graph(tree)
        
        assert self.engine.cfg.number_of_nodes() == 2
    
    @pytest.mark.parametrize("code,expected", [
        ("def foo(): pass", 1),
        ("def foo():\n if x: pass", 2),
    ])
    def test_complexity_levels(self, code, expected):
        """Test various complexity levels."""
        tree = ast.parse(code)
        result = calculate_complexity(tree)
        assert result >= expected
```

**Coverage Requirements**
- All public functions: 100%
- All algorithms: Edge cases
- Performance: Benchmarked

---

## 🎨 Adding Features

### New Analysis Algorithm

**1. Research First**
```
Read academic papers
Understand time/space complexity
Find reference implementations
Plan test cases
```

**2. Implement with Documentation**
```python
def calculate_cognitive_complexity(tree: ast.AST) -> int:
    """
    Calculate cognitive complexity.
    
    Cognitive complexity measures how difficult code
    is to understand (vs cyclomatic = path count).
    
    Increments:
    - if/elif/else: +1
    - Loops: +1
    - Nesting: +nesting_level
    - Recursion: +1
    - Boolean operators: +1 each
    
    Time: O(n), Space: O(d)
    
    Reference:
        Campbell, G. A. (2018)
        "Cognitive Complexity"
        SonarSource White Paper
    """
    complexity = 0
    nesting = 0
    
    class Visitor(ast.NodeVisitor):
        def visit_If(self, node):
            nonlocal complexity, nesting
            complexity += 1 + nesting
            nesting += 1
            self.generic_visit(node)
            nesting -= 1
    
    Visitor().visit(tree)
    return complexity
```

**3. Add Tests**
```python
def test_cognitive_simple():
    code = "def foo(): return 1"
    assert calculate_cognitive_complexity(ast.parse(code)) == 0

def test_cognitive_nested():
    code = """
def foo():
    if x:      # +1
        if y:  # +1 + 1 (nesting) = 2
            pass
"""
    assert calculate_cognitive_complexity(ast.parse(code)) == 3
```

**4. Integrate**
```python
# In analyzer.py
metrics['cognitive_complexity'] = calculate_cognitive_complexity(tree)
```

**5. Document**
```markdown
# In docs/ADVANCED_FEATURES.md
### Cognitive Complexity
Measures understandability...
```

---

### New Code Smell

```python
def detect_feature_envy(tree: ast.AST) -> List[CodeSmell]:
    """
    Detect Feature Envy smell.
    
    Method uses another class more than its own.
    Indicates poor responsibility distribution.
    
    Detection:
    - Count self.* accesses
    - Count other.* accesses
    - If other > self + threshold, flag
    
    Reference: Fowler, M. "Refactoring" Ch. 3
    """
    smells = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            self_access = 0
            other_access = defaultdict(int)
            
            for child in ast.walk(node):
                if isinstance(child, ast.Attribute):
                    if isinstance(child.value, ast.Name):
                        if child.value.id == 'self':
                            self_access += 1
                        else:
                            other_access[child.value.id] += 1
            
            for obj, count in other_access.items():
                if count > self_access and count > 3:
                    smells.append(CodeSmell(
                        name="Feature Envy",
                        severity="MEDIUM",
                        description=f"Method '{node.name}' uses '{obj}' more than 'self'",
                        refactoring_suggestion=f"Move method to '{obj}' class",
                        code_example=_generate_example(node, obj)
                    ))
    
    return smells
```

---

### New Language Support

```python
# src/core/go_scanner.py
class GoScanner:
    """Go language scanner."""
    
    def __init__(self):
        self.extensions = ['.go']
    
    def scan_file(self, path: str) -> Dict:
        """
        Scan Go file.
        
        Uses regex for basic analysis.
        For full AST, would call Go's parser.
        """
        with open(path) as f:
            content = f.read()
        
        return {
            'language': 'Go',
            'functions': self._extract_functions(content),
            'structs': self._extract_structs(content),
            'lines': len(content.split('\n'))
        }
    
    def _extract_functions(self, content: str) -> List[Dict]:
        pattern = r'func\s+(\w+)\s*\('
        return [
            {'name': m.group(1), 'line': content[:m.start()].count('\n') + 1}
            for m in re.finditer(pattern, content)
        ]

# Register in scanner.py
SCANNERS['.go'] = GoScanner
```

---

## 🐛 Bug Reports

### Template

```markdown
**Bug Description**
Clear, concise description.

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

**Stack Trace**
```
Full error message
```
```

---

## 💡 Feature Requests

### Template

```markdown
**Problem**
What pain point does this solve?

**Solution**
Proposed implementation approach.

**Algorithm**
If technical:
- Algorithm name/type
- Time/space complexity
- Reference papers

**Example**
```python
# Desired behavior
result = new_feature()
```

**Complexity**
Easy / Medium / Hard
```

---

## ✅ Pull Request Checklist

```
Code:
☐ PEP 8 compliant
☐ Type hints on all functions
☐ Docstrings with examples
☐ Complexity analysis documented
☐ No commented code
☐ No print() (use logging)

Testing:
☐ All tests pass
☐ New tests for new code
☐ Coverage >= 75%
☐ Edge cases tested

Documentation:
☐ README updated
☐ CHANGELOG.md updated
☐ Algorithm references included
☐ Examples provided

Git:
☐ Descriptive branch name
☐ Logical commits
☐ PR description complete
☐ No merge commits
```

---

## 📚 Learning Resources

### Understanding the Code

**Start:**
1. README.md - Overview
2. TECHNICAL_ARCHITECTURE.md - Algorithms
3. scanner.py - Simple module
4. deep_analysis.py - Complex module

**Key Concepts:**
- Abstract Syntax Trees
- Graph Theory (CFG, DFG)
- Complexity Metrics
- Static Analysis

**Reading:**
```
Books:
- "Introduction to Algorithms" - Cormen
- "Refactoring" - Fowler
- "Code Complete" - McConnell

Papers:
- McCabe (1976) - Cyclomatic Complexity
- Halstead (1977) - Software Science
- Roy (2007) - Clone Detection
```

---

## 🏆 Recognition

### Contributors

Significant contributions earn:
- Name in CONTRIBUTORS.md
- Mention in release notes
- Credit in documentation

**Significant = **
- New algorithm
- Performance improvement
- Language support
- Major bug fix

---

## 📞 Contact

**Questions:** GitHub Discussions
**Bugs:** GitHub Issues
**Email:** xsll7c@gmail.com

**Maintainer:**
- Saleh Almqati
- GitHub: @DeftonesL
- LinkedIn: Saleh-almqati

---

## 🤝 Code of Conduct

**Be Respectful**
- Professional communication
- Constructive feedback
- Help beginners

**Be Educational**
- Explain reasoning
- Share knowledge
- Reference sources

**Be Collaborative**
- Accept criticism
- Give credit
- Work together

---

## 📄 License

Contributions licensed under MIT License.

---

**Thank you for contributing!**

*We're not just building a tool - we're building understanding.*
