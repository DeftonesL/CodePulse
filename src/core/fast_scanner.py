from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import time

from .parallel_scanner import ParallelScanner, analyze_file_wrapper
from .cache import AnalysisCache
from .incremental_analyzer import IncrementalAnalyzer

logger = logging.getLogger(__name__)


class FastScanner:
    
    def __init__(self, max_workers: Optional[int] = None, use_cache: bool = True, use_incremental: bool = True):
        self.parallel = ParallelScanner(max_workers)
        self.cache = AnalysisCache() if use_cache else None
        self.incremental = IncrementalAnalyzer() if use_incremental else None
        self.use_cache = use_cache
        self.use_incremental = use_incremental
        
        logger.info(f"FastScanner initialized:")
        logger.info(f"  - Parallel processing: {self.parallel.max_workers} workers")
        logger.info(f"  - Caching: {'enabled' if use_cache else 'disabled'}")
        logger.info(f"  - Incremental: {'enabled' if use_incremental else 'disabled'}")
    
    def _analyze_with_cache(self, file_path: Path) -> Dict[str, Any]:
        if self.use_cache and self.cache:
            cached = self.cache.get(file_path)
            if cached:
                return cached
        
        result = analyze_file_wrapper(file_path)
        
        if self.use_cache and self.cache and result.get('status') == 'success':
            self.cache.set(file_path, result)
        
        return result
    
    def scan_project(self, project_path: str, file_pattern: str = '*.py') -> Dict[str, Any]:
        project = Path(project_path)
        start_time = time.time()
        
        if not project.exists():
            return {
                'error': f"Project path does not exist: {project_path}",
                'stats': {}
            }
        
        all_files = list(project.rglob(file_pattern))
        logger.info(f"Found {len(all_files)} {file_pattern} files")
        
        if not all_files:
            return {
                'results': [],
                'stats': {
                    'total_files': 0,
                    'analyzed_files': 0,
                    'skipped_files': 0,
                    'duration': 0
                }
            }
        
        files_to_analyze = all_files
        
        if self.use_incremental and self.incremental:
            changed_files = self.incremental.get_changed_files(all_files)
            if changed_files:
                files_to_analyze = list(changed_files)
                logger.info(f"Incremental mode: analyzing {len(files_to_analyze)} changed files")
            else:
                logger.info("No changes detected")
        
        results = self.parallel.scan_files(files_to_analyze, self._analyze_with_cache)
        
        if self.use_incremental and self.incremental:
            self.incremental.update_state(all_files)
        
        duration = time.time() - start_time
        
        stats = {
            'total_files': len(all_files),
            'analyzed_files': len(files_to_analyze),
            'skipped_files': len(all_files) - len(files_to_analyze),
            'duration': f"{duration:.2f}s",
            'files_per_second': f"{len(files_to_analyze) / duration:.1f}" if duration > 0 else "N/A"
        }
        
        if self.use_cache and self.cache:
            stats['cache'] = self.cache.get_stats()
            stats['cache_size'] = self.cache.get_size()
        
        if self.use_incremental and self.incremental:
            stats['incremental'] = self.incremental.get_stats()
        
        logger.info(f"Analysis complete in {duration:.2f}s")
        logger.info(f"  - Files analyzed: {stats['analyzed_files']}/{stats['total_files']}")
        logger.info(f"  - Speed: {stats['files_per_second']} files/second")
        
        if self.use_cache and self.cache:
            cache_stats = self.cache.get_stats()
            logger.info(f"  - Cache hit rate: {cache_stats['hit_rate']}")
        
        return {
            'results': results,
            'stats': stats
        }
    
    def clear_cache(self):
        if self.cache:
            self.cache.clear()
            logger.info("Cache cleared")
    
    def reset_incremental(self):
        if self.incremental:
            self.incremental.reset()
            logger.info("Incremental state reset")
