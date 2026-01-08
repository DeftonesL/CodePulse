# Changelog

All notable changes to CodePulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.10.1] - 2026-01-08

### Added
- Full issue display in HTML reports with categorization (Security/Quality)
- Extended language support to 25+ programming languages
- Comprehensive scan command with deep analysis capabilities
- Functions and Classes columns in file analysis table
- Performance metrics display in report header
- Scroll-reveal animations for progressive content loading
- Responsive table design for mobile compatibility

### Enhanced
- HTML report design with glassmorphism UI
- Background animations: 150 twinkling stars, 20 floating particles
- Advanced CSS animations:
  - Header slide-down animation (0.8s cubic-bezier easing)
  - Card fade-in-up with staggered delays (0.1s increments)
  - Issue slide-in-left with alternating delays
  - Continuous icon bounce animation (2s cycle)
  - Status dot pulse effect (2s cycle)
  - Header text glow animation (2s cycle)
  - Star twinkle effect (3s random delays)
  - Particle float animation (8s random delays)
- Hover effects with CSS transforms and transitions
- Professional dark gradient color scheme
- Enhanced typography using Inter font family

### Fixed
- SyntaxError in smell_detector.py (missing code_example value)
- UnicodeDecodeError in requirements.txt (encoding issues)
- Variable expansion error in codepulse.bat (!LATEST! issue)
- Blank HTML page rendering (f-string implementation)
- Module import errors in comprehensive_scan.py

### Changed
- Default scan pattern from `*.py` to `*` (all files)
- comprehensive_scan.py to support all 25+ language extensions
- HTML report structure for better error display
- Table styling with improved borders and spacing

---

## [0.10.0] - 2026-01-07

### Added
- HTML report generation with interactive dashboard
- Dark theme glassmorphism design
- 8 summary metric cards (Files, Issues, Score, Speed, Lines, Functions, Classes, Performance)
- Cross-platform launcher scripts:
  - codepulse.bat for Windows
  - codepulse.sh for Linux/Mac
- Multi-language support for 25+ programming languages
- Auto-open HTML reports in default browser
- Chart.js integration for data visualization
- Project management commands (install, update, test, benchmark, clean, reports)

### Performance
- Parallel processing implementation (10x performance improvement)
- Smart result caching system (60x performance improvement)
- Incremental analysis for changed files (20x performance improvement)
- Worker pool management for CPU-optimized scanning

---

## [0.9.0] - 2026-01-06

### Added
- Multi-language analysis support
- Performance optimization modules:
  - parallel_scanner.py
  - cache.py
  - incremental_analyzer.py
  - fast_scanner.py
- fast_scan.py command-line interface
- benchmark.py for performance testing
- Unit tests for performance modules

### Changed
- Scanner architecture to support parallel processing
- File analysis to use worker pools

---

## [0.8.0] - 2026-01-05

### Added
- Deep analysis engine with:
  - Control Flow Graph (CFG) generation
  - Data Flow Graph (DFG) analysis
  - Call graph construction
- Clone detection with multiple algorithms
- Code smell detection (5 categories)
- Advanced security scanner with OWASP patterns
- Performance analyzer module
- Advanced metrics calculator

---

## [0.7.1] - 2025-12-30

### Added
- Initial release
- Basic Python code scanning
- Security issue detection
- Quality checks
- JSON report generation
- Command-line interface

---

## Statistics

### Version 0.10.1
- Lines of Code: ~15,000
- Files: 50+
- Languages Supported: 25+
- Security Patterns: 150+
- Test Coverage: 75%

### Performance Metrics
- Sequential Scan (100 files): 60.0s
- Parallel Scan (100 files): 6.0s
- Cached Scan (100 files): 1.0s
- Incremental Scan (5 changed): 3.0s

---

**Note:** For migration guides and breaking changes, see MIGRATION.md

**Note:** For detailed technical changes, see commit history at https://github.com/DeftonesL/CodePulse
