import json
from pathlib import Path
from typing import Dict, List, Set, Any
import logging

logger = logging.getLogger(__name__)


class IncrementalAnalyzer:
    
    def __init__(self, state_file: str = ".codepulse_state.json"):
        self.state_file = Path(state_file)
        self.state = self._load_state()
        logger.info(f"Incremental analyzer initialized with {len(self.state.get('files', {}))} tracked files")
    
    def _load_state(self) -> Dict:
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading state: {e}")
                return {'files': {}}
        return {'files': {}}
    
    def _save_state(self):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
            logger.debug("State saved successfully")
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    def _get_file_mtime(self, file_path: Path) -> float:
        try:
            return file_path.stat().st_mtime
        except Exception as e:
            logger.error(f"Error getting mtime for {file_path}: {e}")
            return 0.0
    
    def get_changed_files(self, files: List[Path]) -> Set[Path]:
        changed = set()
        
        for file in files:
            file_str = str(file)
            current_mtime = self._get_file_mtime(file)
            
            if file_str not in self.state['files']:
                changed.add(file)
                logger.debug(f"New file: {file.name}")
            elif self.state['files'][file_str] != current_mtime:
                changed.add(file)
                logger.debug(f"Modified file: {file.name}")
        
        logger.info(f"Found {len(changed)}/{len(files)} changed files")
        return changed
    
    def update_state(self, files: List[Path]):
        for file in files:
            file_str = str(file)
            mtime = self._get_file_mtime(file)
            self.state['files'][file_str] = mtime
        
        self._save_state()
        logger.info(f"State updated with {len(files)} files")
    
    def reset(self):
        self.state = {'files': {}}
        if self.state_file.exists():
            self.state_file.unlink()
        logger.info("State reset")
    
    def get_stats(self) -> Dict[str, int]:
        return {
            'tracked_files': len(self.state.get('files', {}))
        }
