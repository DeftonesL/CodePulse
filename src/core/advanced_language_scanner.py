"""
Advanced Multi-Language Security Scanner
=========================================

Supports: Python, JavaScript, TypeScript, PHP, Java, C#, Go, Ruby, Rust, Kotlin
"""

import re
import os
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict


@dataclass
class SecurityIssue:
    """Security vulnerability found"""
    type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str
    description: str
    file: str
    line: int
    code_snippet: str
    recommendation: str
    cwe_id: str = ""
    language: str = ""
    
    def to_dict(self):
        return asdict(self)


class LanguagePatterns:
    """Security patterns for different languages"""
    
    # Common patterns across languages
    COMMON = {
        'sql_injection': [
            (r'(execute|exec)\s*\([^)]*\+', 'SQL Injection via concatenation'),
            (r'query.*\+.*["\']', 'SQL query concatenation'),
            (r'SELECT.*FROM.*WHERE.*\+', 'SQL WHERE clause concatenation'),
        ],
        'xss': [
            (r'innerHTML\s*=', 'XSS via innerHTML'),
            (r'document\.write\s*\(', 'XSS via document.write'),
            (r'eval\s*\(', 'Code injection via eval'),
        ],
        'hardcoded_secrets': [
            (r'password\s*=\s*["\'][^"\']{8,}["\']', 'Hardcoded password'),
            (r'api[_-]?key\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded API key'),
            (r'secret\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded secret'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
            (r'sk-[a-zA-Z0-9]{32,}', 'OpenAI API Key'),
        ],
        'path_traversal': [
            (r'\.\./', 'Path traversal pattern'),
            (r'open\s*\([^)]*\+', 'Dynamic file path'),
        ],
    }
    
    # JavaScript/TypeScript specific
    JAVASCRIPT = {
        'dangerous_functions': [
            (r'eval\s*\(', 'eval() - code injection', 'CRITICAL'),
            (r'Function\s*\(', 'Function() constructor - code injection', 'HIGH'),
            (r'setTimeout\s*\(\s*["\']', 'setTimeout with string - code injection', 'HIGH'),
            (r'setInterval\s*\(\s*["\']', 'setInterval with string - code injection', 'HIGH'),
        ],
        'dom_xss': [
            (r'\.innerHTML\s*=', 'innerHTML assignment', 'HIGH'),
            (r'\.outerHTML\s*=', 'outerHTML assignment', 'HIGH'),
            (r'document\.write', 'document.write', 'HIGH'),
            (r'dangerouslySetInnerHTML', 'React dangerouslySetInnerHTML', 'HIGH'),
        ],
        'storage': [
            (r'localStorage\.setItem\([^,]+,\s*password', 'Password in localStorage', 'HIGH'),
            (r'sessionStorage\.setItem\([^,]+,\s*password', 'Password in sessionStorage', 'HIGH'),
        ],
    }
    
    # PHP specific
    PHP = {
        'dangerous_functions': [
            (r'eval\s*\(', 'eval() - code injection', 'CRITICAL'),
            (r'exec\s*\(', 'exec() - command injection', 'CRITICAL'),
            (r'system\s*\(', 'system() - command injection', 'CRITICAL'),
            (r'shell_exec\s*\(', 'shell_exec() - command injection', 'CRITICAL'),
            (r'passthru\s*\(', 'passthru() - command injection', 'CRITICAL'),
            (r'assert\s*\(', 'assert() - code injection', 'HIGH'),
            (r'unserialize\s*\(', 'unserialize() - object injection', 'HIGH'),
        ],
        'file_inclusion': [
            (r'include\s*\(\s*\$', 'Dynamic include - LFI/RFI', 'CRITICAL'),
            (r'require\s*\(\s*\$', 'Dynamic require - LFI/RFI', 'CRITICAL'),
            (r'include_once\s*\(\s*\$', 'Dynamic include_once - LFI/RFI', 'CRITICAL'),
            (r'require_once\s*\(\s*\$', 'Dynamic require_once - LFI/RFI', 'CRITICAL'),
        ],
        'sql': [
            (r'mysql_query\s*\([^)]*\$', 'SQL injection - mysql_query', 'CRITICAL'),
            (r'\$wpdb->query\s*\([^)]*\$', 'SQL injection - WordPress', 'CRITICAL'),
        ],
    }
    
    # Java specific
    JAVA = {
        'dangerous_functions': [
            (r'Runtime\.getRuntime\(\)\.exec', 'Runtime.exec - command injection', 'CRITICAL'),
            (r'ProcessBuilder\s*\(', 'ProcessBuilder - command injection risk', 'HIGH'),
            (r'\.setAccessible\s*\(\s*true', 'Reflection setAccessible - security bypass', 'HIGH'),
        ],
        'deserialization': [
            (r'ObjectInputStream', 'Object deserialization - injection risk', 'HIGH'),
            (r'readObject\s*\(', 'readObject() - deserialization', 'HIGH'),
        ],
        'sql': [
            (r'Statement\.executeQuery\s*\([^)]*\+', 'SQL injection - concatenation', 'CRITICAL'),
            (r'createQuery\s*\([^)]*\+', 'SQL injection - JPA', 'HIGH'),
        ],
    }
    
    # C# specific
    CSHARP = {
        'dangerous_functions': [
            (r'Process\.Start\s*\(', 'Process.Start - command injection risk', 'HIGH'),
            (r'SqlCommand\s*\([^)]*\+', 'SQL injection - SqlCommand', 'CRITICAL'),
            (r'\.Invoke\s*\(', 'Dynamic invocation - injection risk', 'MEDIUM'),
        ],
        'deserialization': [
            (r'BinaryFormatter', 'BinaryFormatter - insecure deserialization', 'CRITICAL'),
            (r'JavaScriptSerializer', 'JavaScriptSerializer - type confusion', 'HIGH'),
        ],
    }
    
    # Go specific
    GO = {
        'dangerous_functions': [
            (r'exec\.Command\s*\(', 'exec.Command - command injection risk', 'HIGH'),
            (r'os\.Exec\s*\(', 'os.Exec - command injection risk', 'HIGH'),
            (r'template\.HTML\s*\(', 'Unsafe HTML - XSS risk', 'HIGH'),
        ],
        'sql': [
            (r'db\.Exec\s*\([^)]*\+', 'SQL injection - concatenation', 'CRITICAL'),
            (r'db\.Query\s*\([^)]*fmt\.Sprintf', 'SQL injection - Sprintf', 'CRITICAL'),
        ],
    }


class AdvancedLanguageScanner:
    """Advanced scanner for multiple programming languages"""
    
    def __init__(self):
        self.issues = []
        self.patterns = LanguagePatterns()
        
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan file based on extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        # Determine language
        language_map = {
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.php': 'PHP',
            '.java': 'Java',
            '.cs': 'C#',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.rs': 'Rust',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
        }
        
        language = language_map.get(ext, 'Unknown')
        
        if language == 'Unknown':
            return {'error': f'Unsupported file type: {ext}'}
        
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return {'error': str(e)}
        
        # Scan based on language
        if language in ['JavaScript', 'TypeScript']:
            self._scan_javascript(lines, file_path, language)
        elif language == 'PHP':
            self._scan_php(lines, file_path)
        elif language == 'Java':
            self._scan_java(lines, file_path)
        elif language == 'C#':
            self._scan_csharp(lines, file_path)
        elif language == 'Go':
            self._scan_go(lines, file_path)
        
        # Common patterns for all languages
        self._scan_common(lines, file_path, language)
        
        # Calculate score
        score = self._calculate_score()
        
        return {
            'language': language,
            'total_issues': len(self.issues),
            'issues': [i.to_dict() for i in self.issues],
            'score': score,
            'by_severity': self._count_by_severity(),
            'by_category': self._count_by_category(),
        }
    
    def _scan_javascript(self, lines: List[str], file_path: str, language: str):
        """Scan JavaScript/TypeScript"""
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip comments
            if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                continue
            
            # Skip if it's in a string literal (common false positive)
            if "includes('eval" in stripped or '"eval' in stripped or "'eval" in stripped:
                continue
            
            # Skip documentation/examples
            if 'example' in stripped.lower() or 'avoid' in stripped.lower():
                continue
            
            # Dangerous functions
            for pattern, desc, severity in self.patterns.JAVASCRIPT['dangerous_functions']:
                if re.search(pattern, stripped, re.IGNORECASE):
                    self.issues.append(SecurityIssue(
                        type='Dangerous Function',
                        severity=severity,
                        category='Code Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Avoid eval and Function constructor. Use safe alternatives.',
                        cwe_id='CWE-95',
                        language=language
                    ))
            
            # DOM XSS
            for pattern, desc, severity in self.patterns.JAVASCRIPT['dom_xss']:
                if re.search(pattern, stripped):
                    # Skip if it's checking for the pattern (not using it)
                    if '.test(' in stripped or 'includes(' in stripped:
                        continue
                    
                    self.issues.append(SecurityIssue(
                        type='XSS Vulnerability',
                        severity=severity,
                        category='Cross-Site Scripting',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Sanitize user input. Use textContent or safe rendering methods.',
                        cwe_id='CWE-79',
                        language=language
                    ))
            
            # Storage
            for pattern, desc, severity in self.patterns.JAVASCRIPT['storage']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Insecure Storage',
                        severity=severity,
                        category='Sensitive Data',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Never store passwords in browser storage. Use secure session management.',
                        cwe_id='CWE-312',
                        language=language
                    ))
    
    def _scan_php(self, lines: List[str], file_path: str):
        """Scan PHP"""
        for i, line in enumerate(lines, 1):
            # Dangerous functions
            for pattern, desc, severity in self.patterns.PHP['dangerous_functions']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Dangerous Function',
                        severity=severity,
                        category='Code/Command Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Avoid dangerous functions. Use safe alternatives and input validation.',
                        cwe_id='CWE-78',
                        language='PHP'
                    ))
            
            # File inclusion
            for pattern, desc, severity in self.patterns.PHP['file_inclusion']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='File Inclusion',
                        severity=severity,
                        category='LFI/RFI',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Whitelist allowed files. Never include based on user input.',
                        cwe_id='CWE-98',
                        language='PHP'
                    ))
            
            # SQL injection
            for pattern, desc, severity in self.patterns.PHP['sql']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='SQL Injection',
                        severity=severity,
                        category='Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Use prepared statements. Never concatenate SQL queries.',
                        cwe_id='CWE-89',
                        language='PHP'
                    ))
    
    def _scan_java(self, lines: List[str], file_path: str):
        """Scan Java"""
        for i, line in enumerate(lines, 1):
            # Dangerous functions
            for pattern, desc, severity in self.patterns.JAVA['dangerous_functions']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Dangerous Function',
                        severity=severity,
                        category='Command Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Validate all inputs to Runtime.exec. Use ProcessBuilder with list.',
                        cwe_id='CWE-78',
                        language='Java'
                    ))
            
            # Deserialization
            for pattern, desc, severity in self.patterns.JAVA['deserialization']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Insecure Deserialization',
                        severity=severity,
                        category='Deserialization',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Never deserialize untrusted data. Use safe formats like JSON.',
                        cwe_id='CWE-502',
                        language='Java'
                    ))
    
    def _scan_csharp(self, lines: List[str], file_path: str):
        """Scan C#"""
        for i, line in enumerate(lines, 1):
            # Dangerous functions
            for pattern, desc, severity in self.patterns.CSHARP['dangerous_functions']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Dangerous Function',
                        severity=severity,
                        category='Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Use parameterized commands and validate inputs.',
                        cwe_id='CWE-89',
                        language='C#'
                    ))
            
            # Deserialization
            for pattern, desc, severity in self.patterns.CSHARP['deserialization']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Insecure Deserialization',
                        severity=severity,
                        category='Deserialization',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Avoid BinaryFormatter. Use DataContractSerializer or JSON.NET.',
                        cwe_id='CWE-502',
                        language='C#'
                    ))
    
    def _scan_go(self, lines: List[str], file_path: str):
        """Scan Go"""
        for i, line in enumerate(lines, 1):
            # Dangerous functions
            for pattern, desc, severity in self.patterns.GO['dangerous_functions']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Dangerous Function',
                        severity=severity,
                        category='Command Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Validate command arguments. Use CommandContext with timeout.',
                        cwe_id='CWE-78',
                        language='Go'
                    ))
            
            # SQL
            for pattern, desc, severity in self.patterns.GO['sql']:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='SQL Injection',
                        severity=severity,
                        category='Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Use parameterized queries with ? placeholders.',
                        cwe_id='CWE-89',
                        language='Go'
                    ))
    
    def _scan_common(self, lines: List[str], file_path: str, language: str):
        """Scan for common patterns across all languages"""
        for i, line in enumerate(lines, 1):
            # SQL injection
            for pattern, desc in self.patterns.COMMON['sql_injection']:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(SecurityIssue(
                        type='SQL Injection',
                        severity='CRITICAL',
                        category='Injection',
                        description=desc,
                        file=file_path,
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Use parameterized queries or ORMs.',
                        cwe_id='CWE-89',
                        language=language
                    ))
            
            # Hardcoded secrets
            for pattern, desc in self.patterns.COMMON['hardcoded_secrets']:
                if re.search(pattern, line, re.IGNORECASE):
                    # Avoid false positives
                    if 'example' not in line.lower() and 'placeholder' not in line.lower():
                        self.issues.append(SecurityIssue(
                            type='Hardcoded Secret',
                            severity='CRITICAL',
                            category='Sensitive Data',
                            description=desc,
                            file=file_path,
                            line=i,
                            code_snippet='***REDACTED***',
                            recommendation='Use environment variables or secret management systems.',
                            cwe_id='CWE-798',
                            language=language
                        ))
    
    def _calculate_score(self) -> float:
        """Calculate security score"""
        score = 100.0
        for issue in self.issues:
            if issue.severity == 'CRITICAL':
                score -= 20
            elif issue.severity == 'HIGH':
                score -= 10
            elif issue.severity == 'MEDIUM':
                score -= 5
            elif issue.severity == 'LOW':
                score -= 2
        return max(0, round(score, 1))
    
    def _count_by_severity(self) -> Dict[str, int]:
        """Count issues by severity"""
        counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for issue in self.issues:
            counts[issue.severity] += 1
        return counts
    
    def _count_by_category(self) -> Dict[str, int]:
        """Count issues by category"""
        counts = {}
        for issue in self.issues:
            counts[issue.category] = counts.get(issue.category, 0) + 1
        return counts


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python advanced_language_scanner.py <file>")
        sys.exit(1)
    
    scanner = AdvancedLanguageScanner()
    result = scanner.scan_file(sys.argv[1])
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"SECURITY SCAN - {result['language']}")
    print(f"{'='*70}")
    print(f"\nScore: {result['score']}/100")
    print(f"Total Issues: {result['total_issues']}\n")
    
    if result['total_issues'] > 0:
        print("By Severity:")
        for sev, count in result['by_severity'].items():
            if count > 0:
                icon = '🔴' if sev == 'CRITICAL' else '🟠' if sev == 'HIGH' else '🟡' if sev == 'MEDIUM' else '🟢'
                print(f"  {icon} {sev}: {count}")
        
        print(f"\nTop Issues:")
        for issue in result['issues'][:5]:
            print(f"\n[{issue['severity']}] {issue['type']} (Line {issue['line']})")
            print(f"  {issue['description']}")
            print(f"  💡 {issue['recommendation']}")
    else:
        print("✅ No issues found!")
