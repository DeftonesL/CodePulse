# Contributing to CodePulse

Welcome! CodePulse is built on deep understanding of algorithms and software engineering principles, not wrapping existing tools.

## Philosophy

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

## Getting Started

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/CodePulse.git
cd CodePulse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v
```

### Project Structure

```
CodePulse/
├── src/
│   ├── core/              # Core analysis engines
│   │   ├── scanner.py     # Main scanner
│   │   ├── deep_analysis_standalone.py
│   │   ├── clone_detection.py
│   │   ├── smell_detector.py
│   │   └── advanced_security.py
│   ├── performance/       # Performance modules
│   │   ├── parallel_scanner.py
│   │   ├── cache.py
│   │   └── incremental_analyzer.py
│   └── reporters/         # Report generators
│       ├── html_reporter.py
│       └── json_reporter.py
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Example usage
└── fast_scan.py          # CLI entry point
```

---

## Development Guidelines

### Code Style

**Python Standards**
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use Black for formatting: `black src/ tests/`

**Naming Conventions**
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

**Documentation**
- Every public function needs docstring
- Include complexity analysis
- Provide usage examples
- Document assumptions

### Example Function

```python
def calculate_cyclomatic_complexity(node: ast.AST) -> int:
    """
    Calculate McCabe cyclomatic complexity for an AST node.
    
    Complexity: O(n) where n is number of nodes
    Space: O(1)
    
    Args:
        node: AST node to analyze
        
    Returns:
        Cyclomatic complexity score
        
    Example:
        >>> tree = ast.parse("def foo(): pass")
        >>> calculate_cyclomatic_complexity(tree)
        1
        
    References:
        McCabe, T. (1976). A Complexity Measure. IEEE TSE.
    """
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For)):
            complexity += 1
    return complexity
```

---

## Testing

### Test Requirements

**Every Feature Must Have**
- Unit tests (80%+ coverage)
- Integration tests
- Performance benchmarks
- Documentation examples

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_scanner.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Performance benchmarks
pytest tests/test_performance.py --benchmark-only
```

### Writing Tests

```python
import pytest
from src.core.scanner import Scanner

def test_scanner_basic():
    """Test basic scanning functionality"""
    scanner = Scanner()
    result = scanner.scan_file("examples/sample.py")
    
    assert result['status'] == 'success'
    assert result['language'] == 'Python'
    assert result['code_lines'] > 0

def test_scanner_performance():
    """Test scanner performance on large files"""
    scanner = Scanner()
    
    import time
    start = time.time()
    result = scanner.scan_file("tests/fixtures/large_file.py")
    duration = time.time() - start
    
    assert duration < 1.0  # Should complete in < 1 second
```

---

## Contribution Process

### 1. Find or Create Issue

- Check existing issues
- Create new issue with:
  - Clear description
  - Expected behavior
  - Current behavior
  - Steps to reproduce (for bugs)
  - Proposed solution (for features)

### 2. Fork and Branch

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/CodePulse.git
cd CodePulse

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Implement Changes

- Write code following guidelines
- Add tests
- Update documentation
- Run tests locally
- Format code with Black

### 4. Commit

```bash
# Stage changes
git add .

# Commit with meaningful message
git commit -m "Add feature: descriptive name

- Detailed change 1
- Detailed change 2
- Fixes #issue_number"
```

**Commit Message Format**
```
Type: Short description (50 chars)

Detailed description of what and why.
Can be multiple paragraphs.

- Bullet points for changes
- Reference issues: Fixes #123

Technical details if needed.
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `perf:` Performance improvement

### 5. Push and Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

**On GitHub:**
1. Open Pull Request
2. Fill template:
   - Description
   - Related issues
   - Changes made
   - Testing done
   - Screenshots (if UI changes)
3. Wait for review

---

## Review Process

### What We Look For

**Code Quality**
- Follows style guidelines
- Has tests with good coverage
- Documentation is clear
- No unnecessary complexity

**Algorithm Quality**
- Correct implementation
- Optimal complexity
- Well-commented
- References provided (if applicable)

**Testing**
- All tests pass
- New tests for new features
- Edge cases covered
- Performance tests included

### Review Timeline

- Initial response: 1-3 days
- Full review: 3-7 days
- Follow-up: 1-2 days

### Feedback

We may request changes:
- Code improvements
- Additional tests
- Documentation updates
- Performance optimizations

---

## Algorithm Contributions

### Research-Based Implementations

When implementing algorithms from papers:

1. **Cite the Paper**
```python
"""
Implementation of Rabin-Karp rolling hash for clone detection.

Based on:
    Karp, R. M., & Rabin, M. O. (1987). 
    Efficient randomized pattern-matching algorithms.
    IBM Journal of Research and Development, 31(2), 249-260.
"""
```

2. **Document Complexity**
```python
def rabin_karp_hash(text: str, pattern_length: int) -> int:
    """
    Calculate rolling hash using Rabin-Karp algorithm.
    
    Time Complexity: O(1) per character
    Space Complexity: O(1)
    
    Args:
        text: Input string
        pattern_length: Length of pattern to hash
        
    Returns:
        Hash value
    """
```

3. **Provide Examples**
```python
# Example usage
hash1 = rabin_karp_hash("hello", 5)
hash2 = rabin_karp_hash("world", 5)
# Hashes can be compared in O(1) time
```

4. **Include Tests**
```python
def test_rabin_karp_correctness():
    """Verify hash produces correct matches"""
    # Test implementation
    pass

def test_rabin_karp_performance():
    """Verify O(1) rolling hash property"""
    # Benchmark implementation
    pass
```

---

## Documentation

### Required Documentation

**For New Features**
- README.md update
- API documentation
- Usage examples
- Performance characteristics

**For Bug Fixes**
- What was broken
- What was fixed
- How to verify fix

### Documentation Style

**Be Clear**
- Short sentences
- Active voice
- Concrete examples
- No jargon (or explain it)

**Be Complete**
- All parameters documented
- Return values explained
- Exceptions listed
- Edge cases noted

**Be Accurate**
- Test all examples
- Keep complexity claims correct
- Update when code changes
- Link to references

---

## Performance Guidelines

### Optimization Rules

1. **Measure First**
   - Profile before optimizing
   - Use pytest-benchmark
   - Document baseline

2. **Optimize Smartly**
   - Algorithm choice matters most
   - Caching helps repeated work
   - Parallel for independent tasks
   - Premature optimization is evil

3. **Document Results**
   - Before/after metrics
   - Complexity analysis
   - Trade-offs made

### Example Optimization PR

```
perf: Optimize clone detection with rolling hash

Changed from naive O(n²) comparison to Rabin-Karp O(n).

Performance on 1000-line file:
- Before: 45.2s
- After: 0.8s
- Improvement: 56.5x

Trade-off: Uses O(n) extra space for hash table.

Fixes #234
```

---

## Release Process

### Version Numbers

Follow Semantic Versioning (semver.org):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Git tag created
- [ ] Release notes written

---

## Getting Help

### Questions

- Check documentation first
- Search existing issues
- Ask in GitHub Discussions
- Be specific and provide examples

### Bug Reports

Include:
- CodePulse version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (full traceback)

### Feature Requests

Include:
- Use case description
- Expected behavior
- Why existing features don't work
- Proposed implementation (optional)

---

## Code of Conduct

### Our Standards

**Positive Behavior**
- Respectful communication
- Constructive feedback
- Collaborative problem-solving
- Inclusive language

**Unacceptable Behavior**
- Harassment or discrimination
- Personal attacks
- Unconstructive criticism
- Spam or trolling

### Enforcement

Violations will be reviewed and may result in:
- Warning
- Temporary ban
- Permanent ban

Report issues to: [maintainer email]

---

## Recognition

### Contributors

All contributors are recognized:
- CONTRIBUTORS.md listing
- Release notes mention
- GitHub contributors graph

### Significant Contributions

Major contributions may receive:
- Co-maintainer status
- Decision-making input
- Special recognition

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You

Every contribution makes CodePulse better. Whether it's:
- Bug reports
- Feature requests
- Documentation fixes
- Code contributions
- Performance improvements

Your effort is appreciated!

---

**Questions?** Open an issue or discussion on GitHub.

**Ready to contribute?** Fork the repo and start coding!
