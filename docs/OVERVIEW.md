# CodePulse Architecture Overview

This document provides a technical overview of CodePulse's architecture, design decisions, and implementation details.

## System Architecture

CodePulse follows a modular architecture with clear separation between scanning engines, analysis logic, and reporting.

### Core Components

**EnterpriseScanner**
- Orchestrates multi-threaded file scanning
- Manages scanner lifecycle and resource allocation
- Aggregates results from individual scanners
- Tracks performance metrics

**Language-Specific Scanners**
- AdvancedSecurityScanner: Deep Python analysis using AST
- AdvancedLanguageScanner: Multi-language pattern detection
- HTMLScanner: Web security analysis
- Specialized scanners for SQL, JSON, and configuration files

**Report Generators**
- HTML: Professional visual reports
- JSON: Machine-readable output for automation

## Scanning Pipeline

1. **File Discovery**: Recursively find all scannable files
2. **Classification**: Group files by language/type
3. **Parallel Scanning**: Distribute work across worker threads
4. **Pattern Matching**: Apply language-specific security patterns
5. **Aggregation**: Collect and categorize findings
6. **Report Generation**: Create formatted output

## Pattern Detection

### Static Analysis
Pattern detection uses regular expressions and abstract syntax tree (AST) analysis:

- **Regex patterns**: Fast detection of common vulnerabilities
- **AST analysis**: Deep semantic understanding for Python
- **Context awareness**: Reduce false positives through code context

### Pattern Categories

**Injection Vulnerabilities**
- SQL injection (string concatenation, unsafe queries)
- Command injection (system calls, shell execution)
- Code injection (eval, exec, dynamic execution)

**Authentication & Session**
- Hardcoded credentials
- Weak session management
- Insecure authentication patterns

**Data Exposure**
- Hardcoded secrets (API keys, tokens, passwords)
- Sensitive data in logs
- Unencrypted sensitive data

**Input Validation**
- Missing sanitization
- Path traversal vulnerabilities
- File upload security issues

## Performance Optimization

### Multi-Threading
Worker threads process files independently with minimal contention:
- ThreadPoolExecutor for work distribution
- Lock-free result collection
- Memory-efficient file processing

### Memory Management
- Stream processing for large files
- Lazy loading of analysis results
- Bounded result queues

### Caching Strategy
Results are not cached between runs to ensure fresh analysis. However, file metadata is cached during a single scan to avoid redundant I/O.

## Extensibility

### Adding Language Support

Create a new scanner method following this pattern:

```python
def _scan_language(self, file_path):
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        patterns = [
            (r'pattern', 'Issue description', 'severity'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, desc, severity in patterns:
                if re.search(pattern, line):
                    issues.append({
                        'file': str(file_path),
                        'type': 'Issue Type',
                        'severity': severity,
                        'description': desc,
                        'line': i
                    })
    except:
        pass
    
    return issues
```

### Custom Pattern Definition

Patterns are defined inline within scanner methods for simplicity. For advanced use cases, patterns can be externalized to JSON configuration files.

## Security Considerations

### Safe Execution
- No code execution from scanned files
- Read-only file access
- Sandboxed pattern matching
- Input sanitization for file paths

### Privacy
- No data transmission to external services
- All analysis performed locally
- Reports contain only code-derived information

## Testing Strategy

### Unit Tests
Individual scanner components tested in isolation with known vulnerable and safe code samples.

### Integration Tests
End-to-end scanning of real projects to validate:
- Multi-threading correctness
- Report accuracy
- Performance benchmarks

### Regression Tests
Prevent reintroduction of fixed bugs through automated test suite.

## Dependencies

### Core Dependencies
- **rich**: Terminal UI and progress tracking
- **click**: Command-line interface
- **networkx**: Graph analysis (for advanced features)

### Optional Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **mypy**: Type checking

## Configuration

Configuration is primarily through command-line arguments. Future versions may support configuration files for:
- Custom pattern definitions
- Language-specific settings
- Output formatting preferences
- Performance tuning

## Future Enhancements

Planned features for future releases:
- Machine learning-based pattern detection
- IDE integration plugins
- Real-time scanning during development
- Custom rule engine
- Advanced data flow analysis
- Incremental scanning support

## Performance Benchmarks

Measured on standard hardware (4-core CPU, 8GB RAM):

| Project Size | Files | Time | Throughput |
|-------------|-------|------|------------|
| Small | 100 | 0.3s | 333 f/s |
| Medium | 1,000 | 3.2s | 313 f/s |
| Large | 10,000 | 32s | 313 f/s |
| Huge | 50,000 | 165s | 303 f/s |

Throughput remains consistent across project sizes, demonstrating linear scalability.

## Technical Decisions

### Why Multi-Threading vs Multi-Processing?
Threading chosen for file I/O bound operations. GIL impact minimal due to I/O waits.

### Why Regex Over Full Parsers?
Balance between accuracy and performance. AST used selectively for Python where deeper analysis provides value.

### Why HTML Over PDF?
HTML reports are universally accessible, searchable, and require no additional dependencies.

## Contributing to Architecture

Architectural changes should:
- Maintain backward compatibility
- Include performance impact analysis
- Update relevant documentation
- Provide migration path if breaking changes necessary

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.
