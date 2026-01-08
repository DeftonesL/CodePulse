import re
from typing import Dict, List, Any
from pathlib import Path

class JavaScriptScanner:
    pass
    
    def __init__(self):
        # Common patterns for JS/TS
        self.patterns = {
            'import': re.compile(r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]'),
            'require': re.compile(r'require\([\'"](.+?)[\'"]\)'),
            'function': re.compile(r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>|(\w+)\s*:\s*(?:async\s+)?\([^)]*\)\s*=>)'),
            'class': re.compile(r'class\s+(\w+)'),
            'const': re.compile(r'const\s+(\w+)'),
            'let': re.compile(r'let\s+(\w+)'),
            'var': re.compile(r'var\s+(\w+)'),
            'export': re.compile(r'export\s+(?:default\s+)?(?:class|function|const)\s+(\w+)'),
            'async': re.compile(r'async\s+function'),
            'promise': re.compile(r'new\s+Promise|\.then\(|\.catch\(|await\s+'),
            'comment_single': re.compile(r'//.*$', re.MULTILINE),
            'comment_multi': re.compile(r'/\*.*?\*/', re.DOTALL),
        }
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Basic metrics
            lines = content.split('\n')
            total_lines = len(lines)
            code_lines = self._count_code_lines(lines)
            
            # Extract information
            imports = self._extract_imports(content)
            functions = self._extract_functions(content)
            classes = self._extract_classes(content)
            exports = self._extract_exports(content)
            
            # Calculate complexity
            complexity = self._calculate_complexity(content)
            
            # Detect features
            has_async = bool(self.patterns['async'].search(content))
            has_promises = bool(self.patterns['promise'].search(content))
            
            language = 'TypeScript' if file_path.endswith('.ts') or file_path.endswith('.tsx') else 'JavaScript'
            
            return {
                'path': file_path,
                'language': language,
                'total_lines': total_lines,
                'code_lines': code_lines,
                'imports': imports,
                'functions': functions,
                'classes': classes,
                'exports': exports,
                'complexity': complexity,
                'features': {
                    'async': has_async,
                    'promises': has_promises,
                },
                'type': self._detect_file_type(file_path, content)
            }
        
        except Exception as e:
            return {
                'path': file_path,
                'error': str(e)
            }
    
    def _count_code_lines(self, lines: List[str]) -> int:
        code_lines = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                continue
            
            # Handle multiline comments
            if '/*' in stripped:
                in_multiline_comment = True
            if '*/' in stripped:
                in_multiline_comment = False
                continue
            
            if in_multiline_comment:
                continue
            
            # Skip single-line comments
            if stripped.startswith('//'):
                continue
            
            code_lines += 1
        
        return code_lines
    
    def _extract_imports(self, content: str) -> List[str]:
        imports = []
        
        # ES6 imports
        for match in self.patterns['import'].finditer(content):
            imports.append(match.group(1))
        
        # CommonJS requires
        for match in self.patterns['require'].finditer(content):
            imports.append(match.group(1))
        
        return list(set(imports))  # Remove duplicates
    
    def _extract_functions(self, content: str) -> List[Dict[str, str]]:
        functions = []
        
        # Find all function definitions
        for match in self.patterns['function'].finditer(content):
            # Get the first non-None group
            name = next((g for g in match.groups() if g is not None), None)
            if name:
                functions.append({
                    'name': name,
                    'type': 'function'
                })
        
        return functions
    
    def _extract_classes(self, content: str) -> List[str]:
        classes = []
        
        for match in self.patterns['class'].finditer(content):
            classes.append(match.group(1))
        
        return classes
    
    def _extract_exports(self, content: str) -> List[str]:
        exports = []
        
        for match in self.patterns['export'].finditer(content):
            exports.append(match.group(1))
        
        return exports
    
    def _calculate_complexity(self, content: str) -> int:
        complexity = 1  # Base complexity
        
        # Keywords that add to complexity
        complexity_keywords = [
            r'\bif\b', r'\belse\b', r'\bfor\b', r'\bwhile\b',
            r'\bcase\b', r'\bcatch\b', r'\b\?\b', r'\b&&\b', r'\b\|\|\b'
        ]
        
        for keyword in complexity_keywords:
            complexity += len(re.findall(keyword, content))
        
        return complexity
    
    def _detect_file_type(self, file_path: str, content: str) -> str:
        path = Path(file_path)
        
        # React components
        if '.jsx' in path.suffixes or '.tsx' in path.suffixes:
            return 'React Component'
        
        if 'import React' in content or 'from "react"' in content:
            return 'React Component'
        
        # Node.js
        if 'require(' in content and 'module.exports' in content:
            return 'Node.js Module'
        
        # TypeScript
        if path.suffix in ['.ts', '.tsx']:
            if 'interface ' in content or 'type ' in content:
                return 'TypeScript with Types'
            return 'TypeScript'
        
        # Vue
        if 'Vue.component' in content or 'new Vue' in content:
            return 'Vue Component'
        
        # Generic
        return 'JavaScript Module'

def scan_javascript_file(file_path: str) -> Dict[str, Any]:
    scanner = JavaScriptScanner()
    return scanner.scan_file(file_path)

# Example usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python js_scanner.py <file.js>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = scan_javascript_file(file_path)
    
    import json
    print(json.dumps(result, indent=2))
