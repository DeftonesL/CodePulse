# Performance Features

## Overview

CodePulse v0.8.0 introduces significant performance improvements through:
- **Parallel Processing** - Multi-threaded file analysis
- **Result Caching** - Avoid re-analyzing unchanged files
- **Incremental Analysis** - Only analyze modified files

## Performance Gains

| Scenario | Before | After | Speedup |
|----------|--------|-------|---------|
| 100 files (first run) | 60s | 6s | **10x** |
| 100 files (second run) | 60s | 1s | **60x** |
| 1000 files (5 changed) | 10m | 30s | **20x** |

## Quick Start

### Using Fast Scanner

```bash
# Basic usage (recommended)
python fast_scan.py ./project

# Custom number of workers
python fast_scan.py ./project --workers 8

# Disable caching
python fast_scan.py ./project --no-cache

# Full scan (no incremental)
python fast_scan.py ./project --no-incremental

# Clear cache
python fast_scan.py ./project --clear-cache
```

### Programmatic Usage

```python
from src.core.fast_scanner import FastScanner

# Initialize scanner
scanner = FastScanner(
    max_workers=4,          # Number of parallel workers
    use_cache=True,         # Enable caching
    use_incremental=True    # Enable incremental analysis
)

# Scan project
results = scanner.scan_project('./project')

# Access statistics
stats = results['stats']
print(f"Analyzed {stats['analyzed_files']} files in {stats['duration']}")
print(f"Cache hit rate: {stats['cache']['hit_rate']}")
```

## Features

### 1. Parallel Processing

Analyzes multiple files simultaneously using multiprocessing.

**Benefits:**
- 10x faster on multi-core systems
- Automatic CPU core detection
- Configurable worker count

**Example:**
```python
from src.core.parallel_scanner import ParallelScanner

scanner = ParallelScanner(max_workers=8)
results = scanner.scan_files(files, analyze_function)
```

### 2. Result Caching

Caches analysis results based on file content hash.

**Benefits:**
- 60x faster on unchanged files
- Automatic cache invalidation
- Configurable cache directory

**Example:**
```python
from src.core.cache import AnalysisCache

cache = AnalysisCache(cache_dir='.codepulse_cache')

# Check cache
cached = cache.get(file_path)
if cached:
    return cached

# Analyze and cache
result = analyze(file_path)
cache.set(file_path, result)

# Get statistics
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate']}")
```

**Cache Management:**
```bash
# Clear cache
python fast_scan.py ./project --clear-cache

# Disable cache
python fast_scan.py ./project --no-cache
```

### 3. Incremental Analysis

Tracks file modification times and only analyzes changed files.

**Benefits:**
- 20x faster when few files changed
- Automatic change detection
- State persistence

**Example:**
```python
from src.core.incremental_analyzer import IncrementalAnalyzer

analyzer = IncrementalAnalyzer()

# Get changed files
changed = analyzer.get_changed_files(all_files)
print(f"Found {len(changed)} changed files")

# Analyze only changed files
for file in changed:
    analyze(file)

# Update state
analyzer.update_state(all_files)
```

**State Management:**
```bash
# Reset state
python fast_scan.py ./project --reset

# Disable incremental
python fast_scan.py ./project --no-incremental
```

## Configuration

### Command-Line Options

```bash
python fast_scan.py <project_path> [options]

Options:
  --workers N           Number of parallel workers (default: CPU count)
  --no-cache           Disable result caching
  --no-incremental     Disable incremental analysis
  --clear-cache        Clear cache before scanning
  --reset              Reset incremental state
  --pattern PATTERN    File pattern to scan (default: *.py)
  --output FILE        Output file for results
```

### Configuration File

Create `.codepulse.yml` in your project:

```yaml
performance:
  parallel: true
  max_workers: 4
  
  cache:
    enabled: true
    directory: .codepulse_cache
  
  incremental:
    enabled: true
    state_file: .codepulse_state.json
```

## Benchmarking

Run performance benchmarks:

```bash
python benchmark.py
```

**Sample Output:**
```
╔═════════════════════════╦═══════╦══════════╦═══════════╗
║ Method                  ║ Files ║ Duration ║ Files/sec ║
╠═════════════════════════╬═══════╬══════════╬═══════════╣
║ Sequential              ║    50 ║   30.5s  ║    1.6    ║
║ Parallel (4 workers)    ║    50 ║    3.2s  ║   15.6    ║
║ With Cache (2nd run)    ║    50 ║    0.5s  ║  100.0    ║
║ Incremental (no change) ║    50 ║    0.1s  ║    N/A    ║
╚═════════════════════════╩═══════╩══════════╩═══════════╝

Speedup: 9.5x faster with parallel processing
Speedup: 6.4x faster with caching (2nd run)
```

## Best Practices

### 1. Use Parallel Processing for Large Projects

```bash
# Good: Use all CPU cores
python fast_scan.py ./large_project --workers 8

# Bad: Sequential scanning
python comprehensive_scan.py ./large_project
```

### 2. Enable Caching for Repeated Scans

```bash
# Good: Cache enabled (default)
python fast_scan.py ./project

# Only disable when necessary
python fast_scan.py ./project --no-cache
```

### 3. Use Incremental for Development

```bash
# Good: Only analyze changed files
python fast_scan.py ./project

# Full scan when needed
python fast_scan.py ./project --no-incremental
```

### 4. Clear Cache Periodically

```bash
# Clear old cache
python fast_scan.py ./project --clear-cache
```

## Troubleshooting

### High Memory Usage

If parallel processing uses too much memory:

```bash
# Reduce workers
python fast_scan.py ./project --workers 2

# Or disable parallelism
python fast_scan.py ./project --workers 1
```

### Cache Size Growing

Check cache size:

```python
from src.core.cache import AnalysisCache

cache = AnalysisCache()
print(f"Cache size: {cache.get_size()}")
```

Clear cache:

```bash
python fast_scan.py ./project --clear-cache
```

### Incremental Not Detecting Changes

Reset state:

```bash
python fast_scan.py ./project --reset
```

## Performance Tips

1. **First Run:** Use full parallel processing
   ```bash
   python fast_scan.py ./project --workers 8
   ```

2. **Development:** Use incremental analysis
   ```bash
   python fast_scan.py ./project
   ```

3. **CI/CD:** Disable cache and incremental
   ```bash
   python fast_scan.py ./project --no-cache --no-incremental
   ```

4. **Large Projects:** Optimize workers
   ```bash
   # Test different worker counts
   python fast_scan.py ./project --workers 4
   python fast_scan.py ./project --workers 8
   python fast_scan.py ./project --workers 16
   ```

## Integration

### With CI/CD

```yaml
# .github/workflows/code-analysis.yml
- name: Analyze Code
  run: |
    python fast_scan.py ./src \
      --workers 4 \
      --no-incremental \
      --output analysis-results.json
```

### With Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
python fast_scan.py ./src --workers 4
```

### With VS Code Task

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Fast Scan",
      "type": "shell",
      "command": "python fast_scan.py ./src",
      "group": "build"
    }
  ]
}
```

## API Reference

See individual module documentation:
- [parallel_scanner.py](../src/core/parallel_scanner.py)
- [cache.py](../src/core/cache.py)
- [incremental_analyzer.py](../src/core/incremental_analyzer.py)
- [fast_scanner.py](../src/core/fast_scanner.py)
