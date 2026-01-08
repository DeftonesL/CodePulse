import pytest
import time
from pathlib import Path
import tempfile
import shutil

from src.core.parallel_scanner import ParallelScanner
from src.core.cache import AnalysisCache
from src.core.incremental_analyzer import IncrementalAnalyzer
from src.core.fast_scanner import FastScanner


def create_test_files(directory, count=10):
    files = []
    for i in range(count):
        file = directory / f"test_{i}.py"
        file.write_text(f"# Test file {i}\ndef test():\n    pass\n")
        files.append(file)
    return files


class TestParallelScanner:
    
    def test_parallel_faster_than_sequential(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            files = create_test_files(tmppath, 20)
            
            def dummy_analyzer(file):
                time.sleep(0.05)
                return {'file': str(file), 'result': 'ok'}
            
            start = time.time()
            for f in files:
                dummy_analyzer(f)
            seq_time = time.time() - start
            
            scanner = ParallelScanner(max_workers=4)
            start = time.time()
            results = scanner.scan_files(files, dummy_analyzer)
            par_time = time.time() - start
            
            assert len(results) == len(files)
            assert par_time < seq_time / 2
    
    def test_handles_errors_gracefully(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            files = create_test_files(tmppath, 5)
            
            def error_analyzer(file):
                if 'test_2' in str(file):
                    raise ValueError("Test error")
                return {'file': str(file), 'result': 'ok'}
            
            scanner = ParallelScanner(max_workers=2)
            results = scanner.scan_files(files, error_analyzer)
            
            assert len(results) == len(files)
            errors = [r for r in results if r.get('status') == 'failed']
            assert len(errors) == 1


class TestAnalysisCache:
    
    def test_cache_hit_and_miss(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = AnalysisCache(cache_dir=tmpdir)
            
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def test(): pass")
            
            result = cache.get(test_file)
            assert result is None
            
            test_result = {'issues': [], 'score': 100}
            cache.set(test_file, test_result)
            
            cached = cache.get(test_file)
            assert cached == test_result
            
            stats = cache.get_stats()
            assert stats['hits'] == 1
            assert stats['misses'] == 1
    
    def test_cache_invalidation_on_file_change(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = AnalysisCache(cache_dir=tmpdir)
            
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def test(): pass")
            
            result1 = {'version': 1}
            cache.set(test_file, result1)
            
            test_file.write_text("def test2(): pass")
            
            cached = cache.get(test_file)
            assert cached is None
    
    def test_cache_clear(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = AnalysisCache(cache_dir=tmpdir)
            
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def test(): pass")
            
            cache.set(test_file, {'data': 'test'})
            assert cache.get(test_file) is not None
            
            cache.clear()
            assert cache.get(test_file) is None
            assert cache.stats['hits'] == 0


class TestIncrementalAnalyzer:
    
    def test_detects_new_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            state_file = tmppath / "state.json"
            
            analyzer = IncrementalAnalyzer(str(state_file))
            
            files = create_test_files(tmppath, 5)
            
            changed = analyzer.get_changed_files(files)
            assert len(changed) == 5
            
            analyzer.update_state(files)
            
            changed = analyzer.get_changed_files(files)
            assert len(changed) == 0
    
    def test_detects_modified_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            state_file = tmppath / "state.json"
            
            analyzer = IncrementalAnalyzer(str(state_file))
            
            files = create_test_files(tmppath, 3)
            analyzer.update_state(files)
            
            time.sleep(0.01)
            files[1].write_text("# Modified\ndef test(): pass")
            
            changed = analyzer.get_changed_files(files)
            assert len(changed) == 1
            assert files[1] in changed
    
    def test_reset(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            state_file = tmppath / "state.json"
            
            analyzer = IncrementalAnalyzer(str(state_file))
            
            files = create_test_files(tmppath, 3)
            analyzer.update_state(files)
            
            assert len(analyzer.state['files']) == 3
            
            analyzer.reset()
            
            assert len(analyzer.state['files']) == 0
            assert not state_file.exists()


class TestFastScanner:
    
    def test_fast_scanner_integration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            create_test_files(tmppath, 5)
            
            scanner = FastScanner(
                max_workers=2,
                use_cache=True,
                use_incremental=True
            )
            
            results = scanner.scan_project(str(tmppath))
            
            assert 'results' in results
            assert 'stats' in results
            
            stats = results['stats']
            assert stats['total_files'] == 5
            assert stats['analyzed_files'] > 0
    
    def test_performance_with_cache(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            create_test_files(tmppath, 10)
            
            scanner = FastScanner(use_cache=True)
            
            start = time.time()
            results1 = scanner.scan_project(str(tmppath))
            first_run = time.time() - start
            
            start = time.time()
            results2 = scanner.scan_project(str(tmppath))
            second_run = time.time() - start
            
            assert second_run < first_run
            
            cache_stats = results2['stats'].get('cache', {})
            assert cache_stats.get('hits', 0) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
