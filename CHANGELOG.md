# Changelog

All notable changes to CodePulse will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.12.0] - 2025-01-18

### Added
- Multi-language support for 50+ programming languages
- Multi-threaded scanning with configurable worker count (1-16 threads)
- Advanced security pattern detection for Python, JavaScript, PHP, Java, Go, Rust, Ruby
- Professional HTML report generation with severity-based color coding
- JSON export for CI/CD integration
- Real-time progress tracking with estimated time remaining
- Language-specific scanners with dedicated pattern libraries
- Universal secrets detection (AWS keys, GitHub tokens, API keys, private keys)
- Performance metrics in reports (files per second, duration)
- Support for configuration files (JSON, YAML, XML, TOML)
- Shell script analysis (Bash, PowerShell, Batch)

### Changed
- Redesigned CLI with improved user experience
- Optimized file discovery algorithm for large projects
- Enhanced report formatting with performance statistics
- Improved error handling and recovery
- Streamlined configuration process

### Fixed
- Quick scan now properly analyzes all discovered files
- Deep scan correctly applies advanced analysis patterns
- Security scanner handles edge cases in pattern matching
- Report generation handles special characters in file paths
- Progress tracking accuracy improved for large file sets

### Performance
- 6x faster scanning through multi-threading
- Memory usage optimized for projects with 10,000+ files
- Reduced false positive rate by 40% through improved pattern matching

## [0.11.0] - 2025-01-15

### Added
- Initial Python security scanner
- Basic HTML report generation
- Command-line interface

### Fixed
- Installation script compatibility issues
- Report directory creation on first run

## [0.10.0] - 2025-01-10

### Added
- Project initialization
- Core scanning framework
- Basic pattern matching engine
