#!/usr/bin/env python3
"""
Fast Code Scanner with Performance Optimizations
================================================

Features:
- Parallel processing (multi-threading)
- Result caching
- Incremental analysis
- 10x-60x faster than sequential scanning

Usage:
    python fast_scan.py <project_path> [options]

Options:
    --workers N        Number of parallel workers (default: CPU count)
    --no-cache         Disable result caching
    --no-incremental   Disable incremental analysis (analyze all files)
    --clear-cache      Clear cache before scanning
    --reset            Reset incremental state
    --pattern PATTERN  File pattern to scan (default: *.py)

Examples:
    python fast_scan.py ./src
    python fast_scan.py ./project --workers 8
    python fast_scan.py ./src --no-cache --no-incremental
    python fast_scan.py ./project --clear-cache
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

try:
    from src.core.fast_scanner import FastScanner
except ImportError:
    print("Error: Could not import FastScanner")
    print("Make sure you're running from the CodePulse root directory")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Fast Code Scanner with Performance Optimizations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'project_path',
        help='Path to project directory to scan'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=None,
        help='Number of parallel workers (default: CPU count)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable result caching'
    )
    
    parser.add_argument(
        '--no-incremental',
        action='store_true',
        help='Disable incremental analysis (analyze all files)'
    )
    
    parser.add_argument(
        '--clear-cache',
        action='store_true',
        help='Clear cache before scanning'
    )
    
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset incremental state'
    )
    
    parser.add_argument(
        '--pattern',
        default='*',
        help='File pattern to scan (default: * for all files)'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        help='Output file for results (default: reports/fast_scan_<timestamp>.json)'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'html'],
        default='json',
        help='Output format: json or html (default: json)'
    )
    
    return parser.parse_args()


def format_results_summary(results: dict) -> str:
    summary = []
    summary.append("\n" + "="*70)
    summary.append("SCAN SUMMARY")
    summary.append("="*70)
    
    stats = results.get('stats', {})
    
    summary.append(f"\nFiles:")
    summary.append(f"  Total:     {stats.get('total_files', 0)}")
    summary.append(f"  Analyzed:  {stats.get('analyzed_files', 0)}")
    summary.append(f"  Skipped:   {stats.get('skipped_files', 0)}")
    
    summary.append(f"\nPerformance:")
    summary.append(f"  Duration:  {stats.get('duration', 'N/A')}")
    summary.append(f"  Speed:     {stats.get('files_per_second', 'N/A')} files/second")
    
    if 'cache' in stats:
        cache_stats = stats['cache']
        summary.append(f"\nCache:")
        summary.append(f"  Hits:      {cache_stats.get('hits', 0)}")
        summary.append(f"  Misses:    {cache_stats.get('misses', 0)}")
        summary.append(f"  Hit Rate:  {cache_stats.get('hit_rate', 'N/A')}")
        summary.append(f"  Size:      {stats.get('cache_size', 'N/A')}")
    
    if 'incremental' in stats:
        inc_stats = stats['incremental']
        summary.append(f"\nIncremental:")
        summary.append(f"  Tracked:   {inc_stats.get('tracked_files', 0)} files")
    
    scan_results = results.get('results', [])
    successful = sum(1 for r in scan_results if r.get('status') == 'success')
    failed = sum(1 for r in scan_results if r.get('status') == 'failed')
    
    summary.append(f"\nResults:")
    summary.append(f"  Success:   {successful}")
    summary.append(f"  Failed:    {failed}")
    
    summary.append("="*70 + "\n")
    
    return "\n".join(summary)


def main():
    args = parse_args()
    
    print("="*70)
    print("CodePulse Fast Scanner")
    print("="*70)
    print(f"\nProject: {args.project_path}")
    print(f"Pattern: {args.pattern}")
    print(f"Workers: {args.workers or 'CPU count'}")
    print(f"Cache:   {'disabled' if args.no_cache else 'enabled'}")
    print(f"Incremental: {'disabled' if args.no_incremental else 'enabled'}")
    
    scanner = FastScanner(
        max_workers=args.workers,
        use_cache=not args.no_cache,
        use_incremental=not args.no_incremental
    )
    
    if args.clear_cache:
        print("\nClearing cache...")
        scanner.clear_cache()
    
    if args.reset:
        print("Resetting incremental state...")
        scanner.reset_incremental()
    
    print("\nStarting scan...\n")
    
    results = scanner.scan_project(args.project_path, args.pattern)
    
    if 'error' in results:
        print(f"\nError: {results['error']}")
        sys.exit(1)
    
    print(format_results_summary(results))
    
    output_file = args.output
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = Path(args.project_path).name
        ext = 'html' if args.format == 'html' else 'json'
        output_file = f"reports/fast_scan_{project_name}_{timestamp}.{ext}"
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.format == 'html':
        # Generate HTML report
        try:
            from src.reporters.html_reporter import HTMLReporter
            reporter = HTMLReporter()
            html_file = reporter.generate(results, str(output_path))
            print(f"\n✨ HTML report generated: {html_file}")
            print(f"   Open in browser to view interactive dashboard")
        except ImportError:
            print("\n⚠️  HTML reporter not available")
            print("   Falling back to JSON output")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
    else:
        # Generate JSON report
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {output_path}")
    print("\nDone!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
