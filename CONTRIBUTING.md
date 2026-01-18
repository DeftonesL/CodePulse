# Contributing to CodePulse

Thank you for considering contributing to CodePulse. This document outlines the process and guidelines for contributions.

## Code of Conduct

All contributors are expected to adhere to professional standards of conduct. Respectful communication and collaboration are essential.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Sample code or project that triggers the bug
- Relevant logs or error messages

### Suggesting Features

Feature suggestions are welcome. Please provide:

- Clear use case description
- Expected behavior
- Examples of similar features in other tools
- Implementation considerations

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your fork
8. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/codepulse.git
cd codepulse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## Code Standards

### Python Style
- Follow PEP 8 guidelines
- Maximum line length: 100 characters
- Use type hints for function signatures
- Document all public functions and classes

### Testing
- Write unit tests for new features
- Maintain test coverage above 80%
- Include integration tests for scanners
- Test with multiple Python versions (3.9, 3.10, 3.11)

### Documentation
- Update README.md for user-facing changes
- Add docstrings to new functions
- Update CHANGELOG.md with your changes
- Include examples for new features

## Project Structure

```
codepulse/
├── src/
│   ├── core/              # Core scanning engines
│   ├── reporters/         # Report generators
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── docs/                  # Documentation
├── config/                # Configuration files
└── reports/               # Generated reports
```

## Adding New Language Support

To add support for a new language:

1. Add file extensions to `LANGUAGE_SUPPORT` in `codepulse.py`
2. Create scanner method in `EnterpriseScanner` class
3. Define security patterns for the language
4. Add test cases in `tests/test_languages.py`
5. Update documentation in `docs/LANGUAGES.md`

Example:
```python
def _scan_newlang(self, file_path):
    issues = []
    patterns = [
        (r'dangerous_function\(', 'Security issue', 'high'),
    ]
    # Implementation
    return issues
```

## Adding Security Patterns

Security patterns are defined in scanner methods. To add new patterns:

1. Research the vulnerability (OWASP, CWE references)
2. Create regex pattern or AST check
3. Assign appropriate severity (critical, high, medium, low)
4. Add test cases with both vulnerable and safe code
5. Document pattern in code comments

## Performance Considerations

- Optimize for large codebases (10,000+ files)
- Use multi-threading where applicable
- Avoid loading entire files into memory when possible
- Cache results when appropriate
- Profile code for bottlenecks

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

Release checklist:
1. Update version in `setup.py` and `codepulse.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Create release branch
5. Tag release
6. Update documentation

## Questions

For questions about contributing, open a discussion in GitHub Discussions or contact the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
