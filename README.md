# CodePulse

A professional static code analysis tool supporting 50+ programming languages with advanced security pattern detection and comprehensive reporting capabilities.

[النسخة العربية](README_AR.md) | English

## Features

- Multi-language support (Python, JavaScript, Java, C/C++, PHP, Ruby, Go, Rust, and 40+ more)
- Advanced security vulnerability detection (OWASP Top 10)
- Multi-threaded scanning for enterprise-scale projects
- Professional HTML and JSON reporting
- Customizable scan depth and performance settings
- Zero external dependencies for core scanning

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/DeftonesL/codepulse.git
cd codepulse

# Install dependencies
pip install -r requirements.txt

# Or use setup scripts
./setup.sh        # Linux/Mac
setup.bat         # Windows
```

### Basic Usage

```bash
# Interactive mode
python codepulse.py

# Quick scan
python codepulse.py --scan quick --path /your/project

# Security-focused scan
python codepulse.py --scan security --path /your/project --format both
```

## Documentation

- [Overview](docs/OVERVIEW.md) - Architecture and design decisions
- [Supported Languages](docs/LANGUAGES.md) - Complete list of supported file types
- [Security Patterns](docs/SECURITY.md) - Detection patterns and rules
- [Configuration](docs/CONFIG.md) - Advanced configuration options
- [Contributing](CONTRIBUTING.md) - Contribution guidelines
- [Changelog](CHANGELOG.md) - Version history

## Scan Types

### Quick Scan
Fast security checks across all supported languages. Ideal for CI/CD integration.

### Deep Scan
Comprehensive analysis including cross-file dependencies and advanced pattern matching.

### Security Scan
OWASP-focused security vulnerability detection with detailed remediation guidance.

### Full Enterprise
Complete professional analysis with all features enabled for production releases.

## Supported Languages

**Systems**: C, C++, Rust, Go  
**JVM**: Java, Kotlin, Scala, Groovy  
**Web**: JavaScript, TypeScript, PHP, Ruby, Python  
**Mobile**: Swift, Objective-C, Dart  
**Data**: SQL, JSON, YAML, XML  
**Scripts**: Shell, PowerShell, Batch  

[View complete list](docs/LANGUAGES.md)

## Configuration

### Worker Threads
```bash
# Use 8 parallel workers for faster scanning
python codepulse.py --workers 8
```

### Output Format
```bash
# Generate both HTML and JSON reports
python codepulse.py --format both
```

### Custom Patterns
Add custom security patterns in `config/patterns.json`

## Performance

- Small projects (< 1,000 files): < 5 seconds
- Medium projects (1,000-10,000 files): 30-60 seconds
- Large projects (10,000+ files): 2-5 minutes

Performance scales linearly with worker count on multi-core systems.

## CI/CD Integration

### GitHub Actions
```yaml
- name: Run CodePulse
  run: |
    pip install -r requirements.txt
    python codepulse.py --scan security --format json --output results.json
```

### GitLab CI
```yaml
codepulse:
  script:
    - pip install -r requirements.txt
    - python codepulse.py --scan quick --format json
```

## Requirements

- Python 3.9 or higher
- 2GB RAM minimum (4GB recommended)
- Multi-core CPU recommended for parallel scanning

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- Issues: [GitHub Issues](https://github.com/DeftonesL/codepulse/issues)
- Documentation: [Wiki](https://github.com/DeftonesL/codepulse/wiki)
- Security: [SECURITY.md](SECURITY.md)

## Credits

Developed with focus on security, performance, and usability for professional development teams.
