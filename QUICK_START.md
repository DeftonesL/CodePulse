# Quick Start Guide

Get CodePulse running in 5 minutes.

---

## Installation

### Step 1: Extract Files
```bash
unzip CodePulse_v0.10.1_PROFESSIONAL.zip
cd CodePulse
```

### Step 2: Install Dependencies
```bash
# Windows
.\codepulse install

# Linux/Mac
./codepulse.sh install

# Manual
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python fast_scan.py --help
```

---

## Basic Usage

### Scan a Project

**Windows:**
```powershell
.\codepulse scan C:\path\to\project
```

**Linux/Mac:**
```bash
./codepulse.sh scan /path/to/project
```

**Direct Python:**
```bash
python fast_scan.py ./project --format html
```

### View Results

HTML report opens automatically in browser. Or find it in:
```
CodePulse/reports/fast_scan_projectname_timestamp.html
```

---

## Common Tasks

### Scan Different Languages

All languages are scanned by default:
```bash
.\codepulse scan C:\mixed-project
# Scans: Python, JavaScript, Java, C++, etc.
```

### Fast Scan (8 Workers)
```bash
.\codepulse fast C:\project
```

### Full Scan (No Cache)
```bash
.\codepulse full C:\project
```

### JSON Output
```bash
.\codepulse json C:\project
```

### Comprehensive Analysis
```bash
.\codepulse comprehensive C:\project
```

---

## Understanding Reports

### HTML Dashboard

**Summary Cards:**
- Total Files: Number of files analyzed
- Total Issues: Security + Quality problems found
- Security Issues: Vulnerabilities detected
- Quality Score: Percentage of clean files

**Issues Section:**
- Lists all detected problems
- Categorized by type (Security/Quality)
- Shows affected files
- Includes descriptions

**Files Table:**
- Complete file listing
- Metrics per file (Lines, Functions, Classes)
- Issue count per file
- Status badges (Clean/Warning/Danger)

### JSON Report

```json
{
  "stats": {
    "total_files": 10,
    "analyzed_files": 10,
    "total_issues": 5,
    "duration": "2.3s"
  },
  "results": [
    {
      "file": "app.py",
      "status": "success",
      "result": {
        "language": "Python",
        "code_lines": 150,
        "security_issues": ["SQL injection risk"],
        "quality_issues": ["Function too complex"]
      }
    }
  ]
}
```

---

## Command Reference

### Scanning
```bash
scan <path>           # HTML report + auto-open
fast <path>           # Fast scan (8 workers)
full <path>           # Full scan (no cache)
json <path>           # JSON output
comprehensive <path>  # Deep analysis
```

### Management
```bash
install      # Install dependencies
update       # Update CodePulse
test         # Run test suite
benchmark    # Performance test
clean        # Clean cache/reports
reports      # Open reports folder
help         # Show commands
```

---

## Troubleshooting

### Python Not Found
```bash
# Check Python installation
python --version

# Should be 3.9 or higher
# If not installed, download from python.org
```

### Permission Denied
```bash
# Windows: Run as Administrator
# Linux/Mac: Add execute permission
chmod +x codepulse.sh
```

### Module Not Found
```bash
# Reinstall dependencies
.\codepulse install

# Or manually
pip install -r requirements.txt
```

### Slow Scanning
```bash
# Use fast mode
.\codepulse fast C:\project

# Or increase workers
python fast_scan.py ./project --workers 16
```

### Out of Memory
```bash
# Scan specific file types only
python fast_scan.py ./project --pattern "*.py"

# Or scan subdirectories separately
.\codepulse scan C:\project\module1
.\codepulse scan C:\project\module2
```

---

## Advanced Usage

### Custom Workers
```bash
python fast_scan.py ./project --workers 16
```

### Specific File Pattern
```bash
python fast_scan.py ./project --pattern "*.js"
```

### Disable Cache
```bash
python fast_scan.py ./project --no-cache
```

### Custom Output Location
```bash
python fast_scan.py ./project --output my_report.html
```

### Clear Cache
```bash
python fast_scan.py ./project --clear-cache
```

---

## Integration

### CI/CD Pipeline
```yaml
# .github/workflows/code-scan.yml
- name: Scan Code
  run: |
    pip install -r requirements.txt
    python fast_scan.py ./src --format json
```

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
python fast_scan.py ./src --format json
if [ $? -ne 0 ]; then
    echo "Code scan failed"
    exit 1
fi
```

### Build Script
```bash
# build.sh
echo "Running code analysis..."
python fast_scan.py ./src --format json --output scan.json

# Check for critical issues
ISSUES=$(jq '.stats.total_issues' scan.json)
if [ $ISSUES -gt 10 ]; then
    echo "Too many issues: $ISSUES"
    exit 1
fi
```

---

## Next Steps

### Learn More
- Read README.md for full feature list
- Check CHANGELOG.md for recent updates
- Browse docs/ for technical details

### Customize
- Edit scan patterns
- Adjust worker count
- Configure output format

### Contribute
- Report bugs on GitHub
- Request features
- Submit pull requests
- See CONTRIBUTING.md

---

## Support

**Issues:** https://github.com/DeftonesL/CodePulse/issues  
**Documentation:** docs/  
**Examples:** examples/

---

**You're ready to start analyzing code!**

Run your first scan:
```bash
.\codepulse scan C:\your\project
```
