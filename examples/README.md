# CodePulse Examples

Practical examples demonstrating CodePulse usage.

---

## Basic Scanning

### Example 1: Simple Python Project

```bash
# Scan Python project
python fast_scan.py examples/python_project --format html

# Result: HTML report with security and quality issues
```

### Example 2: Multi-Language Project

```bash
# Scan mixed project (Python, JavaScript, Java)
python fast_scan.py examples/multi_lang_project --format html

# All languages analyzed automatically
```

---

## Output Formats

### HTML Report

```bash
# Generate interactive HTML dashboard
python fast_scan.py ./project --format html
```

**Output:** `reports/fast_scan_project_timestamp.html`

**Contents:**
- Summary statistics
- Issue listings
- File analysis table
- Visual charts

### JSON Report

```bash
# Generate machine-readable JSON
python fast_scan.py ./project --format json
```

**Output:** `reports/fast_scan_project_timestamp.json`

**Use Cases:**
- CI/CD integration
- Custom processing
- API integration
- Automated quality gates

---

## Performance Options

### Parallel Scanning

```bash
# Use 8 workers
python fast_scan.py ./large_project --workers 8

# Use all CPU cores
python fast_scan.py ./large_project --workers $(nproc)
```

### Caching

```bash
# Use cache (default)
python fast_scan.py ./project

# Force fresh scan
python fast_scan.py ./project --no-cache

# Clear cache before scan
python fast_scan.py ./project --clear-cache
```

### Incremental Analysis

```bash
# Scan only changed files
python fast_scan.py ./project

# Scan all files
python fast_scan.py ./project --no-incremental
```

---

## File Filtering

### Specific Language

```bash
# Python only
python fast_scan.py ./project --pattern "*.py"

# JavaScript only
python fast_scan.py ./project --pattern "*.js"

# TypeScript only
python fast_scan.py ./project --pattern "*.ts"
```

### Multiple Patterns

```bash
# Python and JavaScript
python fast_scan.py ./project --pattern "*.py" --pattern "*.js"
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install CodePulse
        run: |
          pip install -r requirements.txt
      
      - name: Scan Code
        run: |
          python fast_scan.py ./src --format json --output scan.json
      
      - name: Check Quality Gate
        run: |
          ISSUES=$(jq '.stats.total_issues' scan.json)
          if [ $ISSUES -gt 10 ]; then
            echo "Quality gate failed: $ISSUES issues found"
            exit 1
          fi
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: scan-report
          path: scan.json
```

### GitLab CI

```yaml
# .gitlab-ci.yml
code_quality:
  stage: test
  script:
    - pip install -r requirements.txt
    - python fast_scan.py ./src --format json --output scan.json
    - |
      ISSUES=$(jq '.stats.total_issues' scan.json)
      if [ $ISSUES -gt 10 ]; then
        echo "Quality gate failed"
        exit 1
      fi
  artifacts:
    reports:
      codequality: scan.json
```

### Jenkins

```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Code Scan') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python fast_scan.py ./src --format json --output scan.json'
                script {
                    def scan = readJSON file: 'scan.json'
                    if (scan.stats.total_issues > 10) {
                        error("Quality gate failed: ${scan.stats.total_issues} issues")
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'scan.json'
        }
    }
}
```

---

## Custom Processing

### Parse JSON Results

```python
import json

# Load scan results
with open('reports/scan.json', 'r') as f:
    results = json.load(f)

# Extract statistics
stats = results['stats']
print(f"Files: {stats['total_files']}")
print(f"Issues: {stats['total_issues']}")

# Find critical files
for item in results['results']:
    if item['status'] == 'success':
        result = item['result']
        if len(result.get('security_issues', [])) > 0:
            print(f"Security issue in: {item['file']}")
```

### Generate Custom Report

```python
import json
from jinja2 import Template

# Load results
with open('reports/scan.json', 'r') as f:
    results = json.load(f)

# Custom template
template = Template('''
# Code Quality Report

## Summary
- Files: {{ stats.total_files }}
- Issues: {{ stats.total_issues }}
- Duration: {{ stats.duration }}

## Critical Files
{% for file in critical_files %}
- {{ file }}
{% endfor %}
''')

# Find critical files
critical = [
    item['file'] 
    for item in results['results']
    if item.get('result', {}).get('issue_count', 0) > 5
]

# Render
report = template.render(
    stats=results['stats'],
    critical_files=critical
)

print(report)
```

---

## Automated Quality Gates

### Python Script

```python
#!/usr/bin/env python3
import json
import sys
import subprocess

# Run scan
subprocess.run([
    'python', 'fast_scan.py',
    './src',
    '--format', 'json',
    '--output', 'scan.json'
])

# Load results
with open('scan.json', 'r') as f:
    results = json.load(f)

# Quality gates
stats = results['stats']
issues = stats['total_issues']
security = sum(
    len(item['result'].get('security_issues', []))
    for item in results['results']
    if item['status'] == 'success'
)

# Check gates
if security > 0:
    print(f"FAIL: {security} security issues found")
    sys.exit(1)

if issues > 20:
    print(f"FAIL: {issues} total issues (max: 20)")
    sys.exit(1)

print(f"PASS: {issues} issues (under threshold)")
```

### Shell Script

```bash
#!/bin/bash

# Run scan
python fast_scan.py ./src --format json --output scan.json

# Extract metrics
ISSUES=$(jq '.stats.total_issues' scan.json)
SECURITY=$(jq '[.results[].result.security_issues | length] | add' scan.json)

# Quality gates
if [ $SECURITY -gt 0 ]; then
    echo "FAIL: $SECURITY security issues"
    exit 1
fi

if [ $ISSUES -gt 20 ]; then
    echo "FAIL: $ISSUES total issues (max: 20)"
    exit 1
fi

echo "PASS: $ISSUES issues (under threshold)"
```

---

## Performance Benchmarking

### Compare Modes

```bash
# Sequential
time python fast_scan.py ./project --workers 1

# Parallel
time python fast_scan.py ./project --workers 8

# With cache
python fast_scan.py ./project  # First run
time python fast_scan.py ./project  # Second run (cached)
```

### Measure Improvement

```bash
# Baseline
python benchmark.py

# Output:
# Sequential: 60.5s
# Parallel:    6.2s (10x faster)
# Cached:      0.8s (75x faster)
```

---

## Real-World Scenarios

### Scenario 1: Daily Code Review

```bash
# Morning: Scan codebase
.\codepulse scan C:\work\myproject

# Review HTML report
# Fix high-priority issues
# Rescan to verify

.\codepulse scan C:\work\myproject
```

### Scenario 2: Pre-Deployment Check

```bash
# Before deployment
python fast_scan.py ./src --format json

# Check results
if [ $? -eq 0 ]; then
    echo "Quality check passed - deploying..."
    ./deploy.sh
else
    echo "Quality check failed - aborting"
    exit 1
fi
```

### Scenario 3: Legacy Code Analysis

```bash
# Full analysis of old codebase
.\codepulse comprehensive C:\legacy\project

# Generates detailed report with:
# - Clone detection
# - Code smells
# - Security issues
# - Complexity metrics
```

---

## Tips and Tricks

### Speed Up Large Scans

```bash
# Maximum workers
python fast_scan.py ./huge_project --workers 16

# Skip tests directory
python fast_scan.py ./project --pattern "!tests/*"

# Scan in chunks
for dir in src/*; do
    python fast_scan.py "$dir"
done
```

### Continuous Monitoring

```bash
# Watch for changes
while true; do
    python fast_scan.py ./src --format json
    sleep 300  # Scan every 5 minutes
done
```

### Compare Versions

```bash
# Scan before changes
python fast_scan.py ./src --output before.json

# Make changes...

# Scan after changes
python fast_scan.py ./src --output after.json

# Compare
diff <(jq '.stats' before.json) <(jq '.stats' after.json)
```

---

## Support

**More Examples:** https://github.com/DeftonesL/CodePulse/tree/main/examples  
**Documentation:** ../docs/  
**Issues:** https://github.com/DeftonesL/CodePulse/issues

---

**Ready to integrate CodePulse into your workflow!**
