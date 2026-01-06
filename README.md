# CodePulse - Deep Code Intelligence Engine

> Advanced static analysis tool for Python and 13+ programming languages

**Version:** 0.7.1 | **License:** MIT | **Python:** 3.9+

[![Version](https://img.shields.io/badge/version-0.7.1-blue.svg)](https://github.com/DeftonesL/CodePulse)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

CodePulse is a comprehensive code analysis tool that combines security scanning, code quality assessment, clone detection, and performance analysis. Unlike traditional linters, CodePulse performs deep semantic analysis using graph-based algorithms and custom metrics.

### Key Capabilities

- **Security Analysis**: OWASP Top 10 vulnerability detection across 13+ languages
- **Code Quality**: Intelligent smell detection with minimal false positives
- **Clone Detection**: AST-based duplicate code identification (Type 1-4 clones)
- **Performance Analysis**: Algorithmic complexity detection and optimization suggestions
- **Multi-Language Support**: Python, JavaScript, TypeScript, PHP, Java, C#, Go, Ruby, Rust, Kotlin, HTML, JSON, SQL

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/DeftonesL/CodePulse.git
cd CodePulse

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import src.core.scanner; print('Ready')"
```

### Basic Usage

```bash
# Scan single file
python comprehensive_scan.py path/to/file.py

# Scan entire project
python comprehensive_scan.py ./project

# View reports
ls reports/
```

---

## Core Features

### 1. Security Scanner

Detects vulnerabilities including:
- SQL Injection (CWE-89)
- Cross-Site Scripting (CWE-79)
- Path Traversal (CWE-22)
- Command Injection (CWE-78)
- Hardcoded Credentials (CWE-798)
- Weak Cryptography (CWE-327)
- And 150+ additional patterns

**Supported Languages:** Python, JavaScript, TypeScript, PHP, Java, C#, Go, Ruby, Rust, Kotlin, HTML, JSON, SQL

### 2. Code Quality Analysis

Intelligent detection with reduced false positives:
- Code smells (Bloaters, Couplers, Change Preventers)
- Complexity metrics (Cyclomatic, Cognitive, Halstead)
- Maintainability Index calculation
- Technical debt estimation

**Thresholds (v0.7):**
- Long Method: 80 lines (realistic)
- Large Class: 500 lines
- Feature Envy: Ignores standard library modules

### 3. Clone Detection

Advanced duplicate code detection:
- Type 1: Exact clones (identical code)
- Type 2: Renamed clones (same structure, different names)
- Type 3: Modified clones (with minor changes)
- Type 4: Semantic clones (same functionality, different implementation)

**Minimum Thresholds:**
- Cross-file clones: 10 lines
- Same-file clones: 15 lines

### 4. Performance Analysis

Algorithmic complexity detection:
- O(n²) nested loop detection
- O(n³) triple-nested loops
- Memory leak patterns
- Inefficient operations
- N+1 query detection

---

## Output Reports

### Report Format

Reports are saved in `reports/` directory as JSON:

```json
{
  "project_score": 68.5,
  "grade": "C+",
  "total_issues": {
    "security": 35,
    "smells": 52,
    "clones": 8,
    "performance": 31
  },
  "files": {
    "path/to/file.py": {
      "security_issues": [...],
      "code_smells": [...],
      "clones": [...],
      "performance_issues": [...]
    }
  }
}
```

### Score Interpretation

- **90-100 (A)**: Excellent code quality
- **80-89 (B)**: Good code with minor issues
- **70-79 (C)**: Acceptable, needs improvement
- **60-69 (D)**: Below standard, requires attention
- **0-59 (F)**: Critical issues, immediate action needed

---

## Documentation

### Essential Guides

- [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
- [COMPREHENSIVE_GUIDE.md](COMPREHENSIVE_GUIDE.md) - Complete usage guide
- [PYTHON_VERSION_GUIDE.md](PYTHON_VERSION_GUIDE.md) - Python compatibility

### Technical Documentation

- [docs/TECHNICAL_ARCHITECTURE.md](docs/TECHNICAL_ARCHITECTURE.md) - System design
- [docs/ADVANCED_FEATURES.md](docs/ADVANCED_FEATURES.md) - Advanced capabilities
- [docs/REPORTS_MANAGEMENT.md](docs/REPORTS_MANAGEMENT.md) - Working with reports

### Release Notes

- [CHANGELOG.md](CHANGELOG.md) - Version history
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - v0.7 improvements
- [CRITICAL_FIXES.md](CRITICAL_FIXES.md) - v0.7.1 bug fixes

---

## Language Support

### Full Analysis
- Python (complete feature set)

### Security Scanning  
- JavaScript, TypeScript
- PHP, Java, C#
- Go, Ruby, Rust, Kotlin
- HTML, JSON, SQL

---

## Requirements

**System:**
- Python 3.9+
- 4 GB RAM minimum
- 100 MB disk space

**Dependencies:**
- networkx>=3.0
- click>=8.0.0
- rich>=13.0.0

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

## Contact

**Author:** Saleh Almqati  
**GitHub:** [@DeftonesL](https://github.com/DeftonesL)  
---

**CodePulse v0.7.1** - Professional code analysis for serious developers.
