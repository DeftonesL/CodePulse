# CodePulse

> Advanced Static Analysis Tool for Modern Development

Professional code quality and security analysis platform supporting 50+ programming languages with real-time reporting, historical trends, and actionable insights.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Report Types](#report-types)
- [Supported Languages](#supported-languages)
- [Project Structure](#project-structure)
- [Integration](#integration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

CodePulse is a comprehensive static analysis tool designed for modern development workflows. It combines security scanning, code quality assessment, and performance analysis into a single, unified platform.

### Key Capabilities

**Security Analysis**
- SQL injection, XSS, authentication bypasses
- Cryptographic weakness detection
- Hardcoded credentials detection
- OWASP Top 10 coverage

**Code Quality**
- Complexity analysis
- Code smell detection
- TODO/FIXME tracking
- Best practices enforcement

**Performance**
- Algorithm efficiency analysis
- Resource management checks
- Optimization opportunities

---

## Quick Start

```bash
# Windows
git clone https://github.com/yourusername/CodePulse.git
cd CodePulse
.\codepulse install
.\codepulse scan C:\your\project

# Linux/macOS
git clone https://github.com/yourusername/CodePulse.git
cd CodePulse
chmod +x codepulse.sh
./codepulse.sh install
./codepulse.sh scan /your/project
```

---

## Key Features

### Interactive HTML Reports
- Multi-page dashboard layout
- Detailed issue explanations with examples
- Fix suggestions for each issue
- Dark/Light theme toggle
- Collapsible sections
- Export to JSON

### Historical Trends
- SQLite-based storage
- Regression detection
- Progress tracking over time
- Git integration

### High Performance
- Parallel processing (8x faster)
- Intelligent caching
- Incremental analysis
- 150-300 files/second

### 50+ Languages
Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, HTML, CSS, JSON, YAML, XML, SQL, and more

---

## Installation

### Windows

```cmd
# Clone
git clone https://github.com/yourusername/CodePulse.git
cd CodePulse

# Install dependencies
.\codepulse install

# Verify
.\codepulse status
```

### Linux/macOS

```bash
# Clone
git clone https://github.com/yourusername/CodePulse.git
cd CodePulse

# Make executable
chmod +x codepulse.sh

# Install dependencies
./codepulse.sh install

# Verify
./codepulse.sh status
```

### Requirements

- Python 3.9 or higher
- 2GB RAM minimum (4GB recommended)
- 500MB disk space

---

## Usage

### Basic Scanning

```bash
# Standard scan with HTML report
.\codepulse scan C:\project

# Fast parallel scan
.\codepulse fast C:\project --workers 8

# JSON output
.\codepulse json C:\project --output results.json

# Comprehensive analysis
.\codepulse comprehensive C:\project
```

### View Trends

```bash
# After running 2+ scans
.\codepulse trends C:\project

# Custom time period
.\codepulse trends C:\project --days 90

# View history
.\codepulse history C:\project
```

---

## Command Reference

### Scanning Commands

| Command | Description | Example |
|---------|-------------|---------|
| `scan` | Standard scan with HTML report | `.\codepulse scan <path>` |
| `fast` | Parallel high-performance scan | `.\codepulse fast <path>` |
| `full` | Complete scan without cache | `.\codepulse full <path>` |
| `json` | JSON output format | `.\codepulse json <path>` |
| `comprehensive` | Deep analysis | `.\codepulse comprehensive <path>` |

### Analysis Commands

| Command | Description | Example |
|---------|-------------|---------|
| `trends` | Historical trend analysis | `.\codepulse trends <path>` |
| `history` | List all scans | `.\codepulse history <path>` |
| `compare` | Compare projects | `.\codepulse compare <p1> <p2>` |

### Maintenance Commands

| Command | Description |
|---------|-------------|
| `install` | Install dependencies |
| `test` | Run test suite |
| `benchmark` | Performance benchmark |
| `clean` | Clear cache |
| `status` | System status |
| `config` | Show configuration |

---

## Report Types

### HTML Reports

Interactive dashboard with:
- Overview page (health score, charts)
- Issue pages by severity (Critical, High, Medium, Low)
- Files breakdown page
- Dark/Light theme toggle
- Collapsible issue details
- Copy and export functions

**Each issue includes:**
- Problem description
- Detailed explanation
- Security/quality impact
- Fix suggestion with code examples
- File location and line number

### Console Output

```
======================================================================
SCAN SUMMARY
======================================================================

Files:
  Total:     25
  Analyzed:  25

Results:
  Success:   25
  Failed:    0

Issues Found:
  Total:     7
  Critical:  3
  High:      2
  Medium:    1
  Low:       1

Quality Score: 85.5/100
======================================================================
```

---

## Supported Languages

### Full Analysis (50+ languages)

**Programming Languages:**
Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, R, Perl, Lua, Dart, Elixir, Erlang, Haskell, OCaml, F#, Julia

**Web Technologies:**
HTML, CSS, SCSS, SASS, LESS, Vue, Svelte, React, Angular

**Data Formats:**
JSON, YAML, XML, SQL, GraphQL, Protocol Buffers

**Scripting:**
Shell, Bash, PowerShell, Batch

**Build & Config:**
Makefile, CMake, Gradle, Maven, Docker, Config files

**Detected:**
Database files (.db, .sqlite), Backup files (.bak), LaTeX, Markdown

---

## Project Structure

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CodePulse                                    │
│                  Static Analysis Platform                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
        ┌───────▼────────┐ ┌─────▼──────┐ ┌───────▼────────┐
        │  CLI Interface │ │    Core    │ │   Reporters    │
        └────────────────┘ └────────────┘ └────────────────┘
                │                 │                 │
        Input → Scan → Analyze → Detect → Report → Output
```

### Component Flow

```
Source Code
    ↓
File Discovery → Language Detection
    ↓
Parallel Analysis (Worker Pool)
    ↓
Security Scanner + Quality Analyzer + Performance Check
    ↓
Issue Aggregation → Severity Classification
    ↓
Report Generation (HTML/JSON/Console)
    ↓
History Storage (SQLite) → Trend Analysis
```

### Directory Structure

```
CodePulse/
│
├── CLI Entry Points
│   ├── codepulse.bat           # Windows (17 commands)
│   ├── codepulse.sh            # Linux/Mac
│   ├── fast_scan.py            # Main scanner
│   ├── trends.py               # Trend analysis
│   └── comprehensive_scan.py   # Deep analysis
│
├── src/core/                   # Analysis Engine
│   ├── scanner.py              # File discovery (50+ langs)
│   ├── fast_scanner.py         # Parallel orchestrator
│   ├── parallel_scanner.py     # Multi-process execution
│   ├── cache.py                # Caching system
│   ├── incremental_analyzer.py # Change detection
│   ├── trend_analyzer.py       # Historical analysis
│   ├── advanced_security.py    # Security scanner
│   ├── smell_detector.py       # Code smells
│   ├── clone_detection.py      # Duplicate finder
│   └── performance_analyzer.py # Performance profiling
│
├── src/reporters/              # Output Generation
│   ├── html_reporter.py        # Basic HTML
│   └── advanced_html_reporter.py # Multi-page dashboard
│
├── tests/                      # Test Suite (pytest)
├── docs/                       # Documentation
├── examples/                   # Sample files
├── reports/                    # Generated reports
└── .cache/                     # Analysis cache
```

---

## Integration

### CI/CD Pipeline (GitHub Actions)

```yaml
- name: CodePulse Analysis
  run: |
    git clone https://github.com/yourusername/CodePulse.git
    cd CodePulse
    python fast_scan.py ${{ github.workspace }} --format json
    # Check for critical issues
    python -c "
    import json
    with open('results.json') as f:
        if sum(1 for i in json.load(f)['issues'] if i['severity']=='critical') > 0:
            exit(1)
    "
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

cd /path/to/CodePulse
python fast_scan.py $(git rev-parse --show-toplevel) --format json

CRITICAL=$(python -c "
import json
with open('results.json') as f:
    print(sum(1 for i in json.load(f)['issues'] if i['severity']=='critical'))
")

if [ "$CRITICAL" -gt 0 ]; then
    echo "Critical issues found. Commit blocked."
    exit 1
fi
```

---

## Troubleshooting

### No Issues Found

If scans show 0 issues on projects that should have issues:

```bash
# 1. Check you're using HTML format
.\codepulse scan C:\project --format html

# 2. Verify files are being analyzed
# Look for "Success: X" in output (should not be 0)

# 3. Check the generated HTML report
# Open reports/latest.html and look for issue details

# 4. Test on examples folder
.\codepulse scan examples
# Should find 3 issues (1 critical, 2 high)
```

### Module Not Found

```bash
.\codepulse install
# or
pip install -r requirements.txt
```

### Permission Denied (Linux/Mac)

```bash
chmod +x codepulse.sh
```

### Trends Show "Insufficient Data"

```bash
# Need at least 2 scans
.\codepulse scan C:\project
# Make changes...
.\codepulse scan C:\project
# Now view trends
.\codepulse trends C:\project
```

---

## Performance

**Benchmarks** (Intel i7, 16GB RAM, SSD):

| Project Size | Files | Time | Speed |
|--------------|-------|------|-------|
| Small | 50 | 0.4s | 125 files/sec |
| Medium | 500 | 3.2s | 156 files/sec |
| Large | 5000 | 28s | 178 files/sec |

**Speedup:** 6-8x faster with parallel processing

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Credits

**Creator:** Saleh Almqati

**Technologies:** Python, NetworkX, Jinja2, Click, Rich, Pytest

---

**Built by developers, for developers.**

For updates: [github.com/DeftonesL/CodePulse](https://github.com/DeftonesL/CodePulse)
