# Configuration Guide

This document covers all configuration options available in CodePulse.

## Command-Line Options

### Basic Usage

```bash
python codepulse.py [OPTIONS]
```

### Available Options

**Scan Type:**
```bash
--scan TYPE          Scan type: quick, deep, security, full
                     Default: interactive menu
```

**Project Path:**
```bash
--path PATH          Path to project directory
                     Default: current directory
```

**Worker Threads:**
```bash
--workers N          Number of parallel workers (1-16)
                     Default: 4
```

**Output Format:**
```bash
--format FORMAT      Report format: html, json, both
                     Default: html
```

**Output File:**
```bash
--output FILE        Output file path
                     Default: reports/scan_TIMESTAMP.{format}
```

**Verbosity:**
```bash
--verbose           Enable verbose output
--quiet             Minimal output
```

### Examples

**Quick scan with 8 workers:**
```bash
python codepulse.py --scan quick --workers 8
```

**Security scan with JSON output:**
```bash
python codepulse.py --scan security --format json --output security_report.json
```

**Deep scan specific project:**
```bash
python codepulse.py --scan deep --path /path/to/project --format both
```

**Full enterprise scan:**
```bash
python codepulse.py --scan full --workers 16 --format both --verbose
```

## Interactive Mode

When run without options, CodePulse launches interactive mode:

```bash
python codepulse.py
```

Interactive mode provides:
- Menu-driven scan selection
- Real-time progress tracking
- Guided configuration
- Immediate result display

## Performance Tuning

### Worker Count Optimization

**Small Projects (< 1,000 files):**
```bash
--workers 2
```
CPU overhead outweighs benefits for small projects.

**Medium Projects (1,000-10,000 files):**
```bash
--workers 4
```
Balanced performance for most use cases.

**Large Projects (10,000+ files):**
```bash
--workers 8
```
Maximum throughput on multi-core systems.

**Very Large Projects (50,000+ files):**
```bash
--workers 16
```
Requires adequate RAM and CPU cores.

### Memory Considerations

Each worker requires approximately:
- 50-100MB for file processing
- 100-200MB for pattern matching
- Additional memory for large files

**Recommended RAM:**
- 4 workers: 2GB minimum, 4GB recommended
- 8 workers: 4GB minimum, 8GB recommended
- 16 workers: 8GB minimum, 16GB recommended

## Scan Type Details

### Quick Scan
**Purpose:** Fast daily checks  
**Coverage:** Basic security patterns  
**Analysis Depth:** Pattern matching only  
**Typical Duration:** Seconds to minutes  
**Best For:** CI/CD integration, pre-commit hooks

### Deep Scan
**Purpose:** Comprehensive analysis  
**Coverage:** All patterns plus advanced analysis  
**Analysis Depth:** AST analysis, cross-file detection  
**Typical Duration:** Minutes  
**Best For:** Weekly audits, code reviews

### Security Scan
**Purpose:** OWASP-focused security audit  
**Coverage:** All OWASP Top 10 patterns  
**Analysis Depth:** Deep security-specific analysis  
**Typical Duration:** Minutes  
**Best For:** Security audits, compliance checks

### Full Enterprise
**Purpose:** Complete professional audit  
**Coverage:** Everything  
**Analysis Depth:** Maximum  
**Typical Duration:** Minutes to hours  
**Best For:** Release audits, penetration testing prep

## File Filtering

### Include Patterns

Scan specific file types:
```bash
python codepulse.py --include "*.py,*.js"
```

### Exclude Patterns

Skip certain directories:
```bash
python codepulse.py --exclude "node_modules,venv,dist"
```

### Configuration File

Create `.codepulse.json` in project root:
```json
{
  "workers": 8,
  "format": "both",
  "exclude": [
    "node_modules",
    "venv",
    ".git",
    "dist",
    "build"
  ],
  "include": [
    "*.py",
    "*.js",
    "*.java"
  ]
}
```

## Custom Patterns

### Pattern File Format

Create `config/custom_patterns.json`:
```json
{
  "patterns": [
    {
      "language": "python",
      "pattern": "dangerous_function\\(",
      "type": "Custom Security Issue",
      "severity": "high",
      "description": "Usage of dangerous_function detected"
    }
  ]
}
```

### Loading Custom Patterns

```bash
python codepulse.py --patterns config/custom_patterns.json
```

## Output Configuration

### HTML Reports

**Features:**
- Visual severity indicators
- Interactive charts
- File-by-file breakdown
- Performance metrics

**Customization:**
```json
{
  "html": {
    "theme": "professional",
    "include_metrics": true,
    "show_code_snippets": true
  }
}
```

### JSON Reports

**Structure:**
```json
{
  "scan_type": "security_scan",
  "timestamp": "2025-01-18T10:30:00",
  "project_path": "/path/to/project",
  "stats": {
    "total_files": 1000,
    "analyzed_files": 998,
    "duration": 45.2,
    "files_per_second": 22.1
  },
  "issues": [
    {
      "file": "app.py",
      "type": "SQL Injection",
      "severity": "critical",
      "line": 42,
      "description": "Unsafe SQL query construction"
    }
  ]
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: CodePulse Security Scan

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install CodePulse
        run: |
          pip install -r requirements.txt
      
      - name: Run Security Scan
        run: |
          python codepulse.py --scan security --format json --output results.json
      
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: security-results
          path: results.json
```

### GitLab CI

```yaml
codepulse:
  stage: test
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - python codepulse.py --scan quick --format json --output results.json
  artifacts:
    reports:
      codequality: results.json
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Security Scan') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python codepulse.py --scan security --format json --output results.json'
                archiveArtifacts artifacts: 'results.json'
            }
        }
    }
}
```

## Environment Variables

### Configuration via Environment

```bash
export CODEPULSE_WORKERS=8
export CODEPULSE_FORMAT=both
export CODEPULSE_VERBOSE=1

python codepulse.py
```

### Available Variables

```
CODEPULSE_WORKERS         Number of worker threads
CODEPULSE_FORMAT          Output format (html/json/both)
CODEPULSE_OUTPUT_DIR      Report output directory
CODEPULSE_EXCLUDE         Comma-separated exclude patterns
CODEPULSE_VERBOSE         Enable verbose logging
```

## Ignore Files

### .codepulseignore

Create `.codepulseignore` in project root:
```
node_modules/
venv/
.git/
*.min.js
dist/
build/
test/fixtures/
```

Format follows `.gitignore` syntax.

## Logging Configuration

### Log Levels

```bash
--log-level DEBUG    Detailed debugging information
--log-level INFO     General information (default)
--log-level WARNING  Warnings only
--log-level ERROR    Errors only
```

### Log Output

```bash
--log-file scan.log  Write logs to file
```

## Advanced Configuration

### Timeout Settings

```json
{
  "timeouts": {
    "file_scan": 30,
    "total_scan": 3600
  }
}
```

### Memory Limits

```json
{
  "limits": {
    "max_file_size": 10485760,
    "max_line_length": 10000
  }
}
```

### Severity Thresholds

```json
{
  "thresholds": {
    "fail_on_critical": true,
    "fail_on_high": false,
    "max_issues": 100
  }
}
```

## Configuration Precedence

Configuration is loaded in this order (later overrides earlier):

1. Default values
2. Configuration file (`.codepulse.json`)
3. Environment variables
4. Command-line arguments

## Best Practices

**Development:**
```bash
python codepulse.py --scan quick --workers 4
```

**Pre-commit:**
```bash
python codepulse.py --scan quick --format json --quiet
```

**CI/CD:**
```bash
python codepulse.py --scan security --format json --workers 8
```

**Release Audit:**
```bash
python codepulse.py --scan full --workers 16 --format both --verbose
```

## Troubleshooting

**Slow Performance:**
- Reduce worker count
- Exclude unnecessary directories
- Use quick scan for large projects

**Out of Memory:**
- Reduce worker count
- Increase system RAM
- Exclude large binary files

**False Positives:**
- Review pattern definitions
- Use inline suppression comments
- Report patterns for refinement

## Support

For configuration assistance:
- Check documentation
- Review examples in `/examples` directory
- Open an issue on GitHub

See [README.md](../README.md) for general information.
