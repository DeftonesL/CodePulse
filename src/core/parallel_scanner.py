import multiprocessing
from pathlib import Path
from typing import List, Dict, Any, Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


class ParallelScanner:
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers or multiprocessing.cpu_count()
        logger.info(f"Initialized parallel scanner with {self.max_workers} workers")
    
    def scan_files(self, files: List[Path], analyzer_func: Callable) -> List[Dict[str, Any]]:
        results = []
        total_files = len(files)
        
        logger.info(f"Scanning {total_files} files using {self.max_workers} workers")
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(analyzer_func, file): file 
                for file in files
            }
            
            completed = 0
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                completed += 1
                
                try:
                    result = future.result()
                    results.append(result)
                    
                    if completed % 10 == 0 or completed == total_files:
                        logger.debug(f"Progress: {completed}/{total_files} files")
                        
                except Exception as e:
                    logger.error(f"Error analyzing {file}: {e}")
                    results.append({
                        'file': str(file),
                        'error': str(e),
                        'status': 'failed'
                    })
        
        logger.info(f"Completed scanning {total_files} files")
        return results


def analyze_file_wrapper(file_path):
    from pathlib import Path
    import re
    
    try:
        file_path = Path(file_path)
        ext = file_path.suffix.lower()
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        language_map = {
            '.py': 'Python', '.pyw': 'Python',
            '.js': 'JavaScript', '.jsx': 'JavaScript', '.mjs': 'JavaScript',
            '.ts': 'TypeScript', '.tsx': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++', '.cc': 'C++', '.cxx': 'C++', '.hpp': 'C++', '.h': 'C/C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin', '.kts': 'Kotlin',
            '.cs': 'C#',
            '.scala': 'Scala',
            '.r': 'R',
            '.dart': 'Dart',
            '.lua': 'Lua',
            '.sh': 'Shell', '.bash': 'Shell',
            '.sql': 'SQL',
            '.html': 'HTML', '.htm': 'HTML',
            '.css': 'CSS', '.scss': 'CSS', '.sass': 'CSS',
            '.json': 'JSON',
            '.yaml': 'YAML', '.yml': 'YAML',
            '.xml': 'XML',
            '.md': 'Markdown'
        }
        
        language = language_map.get(ext, 'Unknown')
        
        result = {
            'file': str(file_path),
            'language': language,
            'total_lines': len(lines),
            'code_lines': len(non_empty_lines),
            'size': len(code),
            'extension': ext
        }
        
        if ext == '.py':
            try:
                import ast
                tree = ast.parse(code)
                result.update({
                    'functions': len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                    'classes': len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
                    'imports': len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]),
                })
            except:
                pass
        
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            result.update({
                'functions': len(re.findall(r'\bfunction\s+\w+|\b\w+\s*=\s*(?:async\s+)?(?:function|\(.*?\)\s*=>)', code)),
                'classes': len(re.findall(r'\bclass\s+\w+', code)),
                'imports': len(re.findall(r'\bimport\s+.*?from|require\(', code)),
            })
        
        elif ext == '.java':
            result.update({
                'classes': len(re.findall(r'\b(?:public|private|protected)?\s*class\s+\w+', code)),
                'methods': len(re.findall(r'\b(?:public|private|protected)\s+(?:static\s+)?[\w<>\[\]]+\s+\w+\s*\(', code)),
                'imports': len(re.findall(r'\bimport\s+', code)),
            })
        
        elif ext in ['.c', '.cpp', '.cc', '.cxx', '.h', '.hpp']:
            result.update({
                'functions': len(re.findall(r'\b[\w:]+\s+\w+\s*\([^)]*\)\s*\{', code)),
                'classes': len(re.findall(r'\bclass\s+\w+', code)),
                'includes': len(re.findall(r'#include\s*[<"]', code)),
            })
        
        elif ext == '.go':
            result.update({
                'functions': len(re.findall(r'\bfunc\s+\w+', code)),
                'structs': len(re.findall(r'\btype\s+\w+\s+struct', code)),
                'imports': len(re.findall(r'\bimport\s+', code)),
            })
        
        elif ext == '.rs':
            result.update({
                'functions': len(re.findall(r'\bfn\s+\w+', code)),
                'structs': len(re.findall(r'\bstruct\s+\w+', code)),
                'traits': len(re.findall(r'\btrait\s+\w+', code)),
            })
        
        security_issues = []
        quality_issues = []
        
        if 'eval(' in code:
            security_issues.append('Use of eval() detected')
        if re.search(r'password\s*=\s*["\']', code, re.I):
            security_issues.append('Hardcoded password detected')
        if 'exec(' in code:
            security_issues.append('Use of exec() detected')
        
        if len(non_empty_lines) > 500:
            quality_issues.append('Large file (>500 lines)')
        if len(code) > 10000:
            quality_issues.append('Large file size (>10KB)')
        
        result['security_issues'] = security_issues
        result['quality_issues'] = quality_issues
        result['issue_count'] = len(security_issues) + len(quality_issues)
        
        return {
            'file': str(file_path),
            'result': result,
            'status': 'success'
        }
        
    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e),
            'status': 'failed'
        }
