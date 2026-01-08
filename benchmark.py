#!/usr/bin/env python3
"""
Performance Benchmark Script
============================

Compare sequential vs parallel scanning performance
"""

import time
import sys
from pathlib import Path
from tabulate import tabulate

try:
    from src.core.scanner import Scanner
    from src.core.fast_scanner import FastScanner
except ImportError:
    print("Error: Could not import required modules")
    sys.exit(1)


def benchmark_sequential(files, sample_size=50):
    print(f"\n1. Sequential Scan ({sample_size} files)...")
    
    scanner = Scanner()
    files_sample = files[:sample_size]
    
    start = time.time()
    results = []
    
    for file in files_sample:
        try:
            result = scanner.scan_file(file)
            results.append(result)
        except Exception as e:
            pass
    
    duration = time.time() - start
    
    return {
        'method': 'Sequential',
        'files': len(files_sample),
        'duration': duration,
        'files_per_sec': len(files_sample) / duration if duration > 0 else 0
    }


def benchmark_parallel(files, sample_size=50, workers=4):
    print(f"\n2. Parallel Scan ({sample_size} files, {workers} workers)...")
    
    scanner = FastScanner(
        max_workers=workers,
        use_cache=False,
        use_incremental=False
    )
    
    files_sample = files[:sample_size]
    
    start = time.time()
    results = scanner.parallel.scan_files(
        files_sample,
        lambda f: scanner._analyze_with_cache(f)
    )
    duration = time.time() - start
    
    return {
        'method': f'Parallel ({workers} workers)',
        'files': len(files_sample),
        'duration': duration,
        'files_per_sec': len(files_sample) / duration if duration > 0 else 0
    }


def benchmark_with_cache(files, sample_size=50):
    print(f"\n3. With Cache (2nd run, {sample_size} files)...")
    
    scanner = FastScanner(
        max_workers=4,
        use_cache=True,
        use_incremental=False
    )
    
    files_sample = files[:sample_size]
    
    print("   First run (populating cache)...")
    scanner.parallel.scan_files(
        files_sample,
        lambda f: scanner._analyze_with_cache(f)
    )
    
    print("   Second run (using cache)...")
    start = time.time()
    results = scanner.parallel.scan_files(
        files_sample,
        lambda f: scanner._analyze_with_cache(f)
    )
    duration = time.time() - start
    
    cache_stats = scanner.cache.get_stats()
    
    return {
        'method': 'With Cache (2nd run)',
        'files': len(files_sample),
        'duration': duration,
        'files_per_sec': len(files_sample) / duration if duration > 0 else 0,
        'cache_hit_rate': cache_stats['hit_rate']
    }


def benchmark_incremental(files, sample_size=50):
    print(f"\n4. Incremental (5 changed, {sample_size} total)...")
    
    scanner = FastScanner(
        max_workers=4,
        use_cache=True,
        use_incremental=True
    )
    
    files_sample = files[:sample_size]
    
    print("   First run (full scan)...")
    scanner.incremental.update_state(files_sample)
    
    print("   Second run (no changes)...")
    changed = scanner.incremental.get_changed_files(files_sample)
    
    start = time.time()
    duration = time.time() - start
    
    return {
        'method': 'Incremental (no changes)',
        'files': len(files_sample),
        'changed': len(changed),
        'duration': duration,
        'files_per_sec': 'N/A (instant)'
    }


def main():
    print("="*70)
    print("CodePulse Performance Benchmark")
    print("="*70)
    
    project_path = Path('./src')
    if not project_path.exists():
        print(f"\nError: {project_path} not found")
        print("Run this script from CodePulse root directory")
        sys.exit(1)
    
    files = list(project_path.rglob('*.py'))
    
    if len(files) < 10:
        print(f"\nWarning: Only {len(files)} files found. Using smaller sample size.")
        sample_size = min(len(files), 10)
    else:
        sample_size = min(len(files), 50)
    
    print(f"\nFound {len(files)} Python files")
    print(f"Running benchmarks with {sample_size} files...\n")
    
    results = []
    
    try:
        result1 = benchmark_sequential(files, sample_size)
        results.append(result1)
    except Exception as e:
        print(f"Sequential benchmark failed: {e}")
    
    try:
        result2 = benchmark_parallel(files, sample_size, workers=4)
        results.append(result2)
    except Exception as e:
        print(f"Parallel benchmark failed: {e}")
    
    try:
        result3 = benchmark_with_cache(files, sample_size)
        results.append(result3)
    except Exception as e:
        print(f"Cache benchmark failed: {e}")
    
    try:
        result4 = benchmark_incremental(files, sample_size)
        results.append(result4)
    except Exception as e:
        print(f"Incremental benchmark failed: {e}")
    
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70 + "\n")
    
    table_data = []
    for r in results:
        row = [
            r['method'],
            r['files'],
            f"{r['duration']:.2f}s" if isinstance(r['duration'], float) else r['duration'],
            f"{r['files_per_sec']:.1f}" if isinstance(r['files_per_sec'], float) else r['files_per_sec']
        ]
        if 'cache_hit_rate' in r:
            row.append(r['cache_hit_rate'])
        table_data.append(row)
    
    headers = ['Method', 'Files', 'Duration', 'Files/sec']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    if len(results) >= 2:
        seq_time = results[0]['duration']
        par_time = results[1]['duration']
        speedup = seq_time / par_time if par_time > 0 else 0
        print(f"\nSpeedup: {speedup:.1f}x faster with parallel processing")
    
    if len(results) >= 3:
        par_time = results[1]['duration']
        cache_time = results[2]['duration']
        speedup = par_time / cache_time if cache_time > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster with caching (2nd run)")
    
    print("\n" + "="*70)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
