import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AnalysisCache:
    
    def __init__(self, cache_dir: str = ".codepulse_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.stats = {
            'hits': 0,
            'misses': 0
        }
        logger.info(f"Cache initialized at {self.cache_dir}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error hashing {file_path}: {e}")
            return ""
    
    def _get_cache_path(self, file_hash: str) -> Path:
        return self.cache_dir / f"{file_hash[:16]}.json"
    
    def get(self, file_path: Path) -> Optional[Dict[str, Any]]:
        try:
            file_hash = self._get_file_hash(file_path)
            if not file_hash:
                return None
            
            cache_path = self._get_cache_path(file_hash)
            
            if cache_path.exists():
                with open(cache_path, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                self.stats['hits'] += 1
                logger.debug(f"Cache HIT: {file_path.name}")
                return result
            
            self.stats['misses'] += 1
            logger.debug(f"Cache MISS: {file_path.name}")
            return None
            
        except Exception as e:
            logger.error(f"Cache read error for {file_path}: {e}")
            return None
    
    def set(self, file_path: Path, result: Dict[str, Any]) -> bool:
        try:
            file_hash = self._get_file_hash(file_path)
            if not file_hash:
                return False
            
            cache_path = self._get_cache_path(file_hash)
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            
            logger.debug(f"Cached: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Cache write error for {file_path}: {e}")
            return False
    
    def clear(self):
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir()
        self.stats = {'hits': 0, 'misses': 0}
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        total = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total * 100) if total > 0 else 0
        
        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'total_requests': total,
            'hit_rate': f"{hit_rate:.1f}%"
        }
    
    def get_size(self) -> str:
        total_size = sum(f.stat().st_size for f in self.cache_dir.rglob('*.json'))
        
        if total_size < 1024:
            return f"{total_size} B"
        elif total_size < 1024 * 1024:
            return f"{total_size / 1024:.1f} KB"
        else:
            return f"{total_size / (1024 * 1024):.1f} MB"
