"""
Advanced Security Scanner
==========================

Comprehensive security analysis including:
- SQL Injection detection
- XSS vulnerabilities
- Command Injection
- Path Traversal
- Insecure Deserialization
- Hardcoded Secrets
- Cryptographic Issues
- Authentication/Authorization Issues
"""

import ast
import re
import os
from typing import Dict, List, Any, Set
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SecurityIssue:
    """Security vulnerability"""
    type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str
    description: str
    file: str
    line: int
    code_snippet: str
    recommendation: str
    cwe_id: str  # Common Weakness Enumeration ID
    owasp: str   # OWASP Top 10 reference


class AdvancedSecurityScanner:
    """
    Advanced security vulnerability scanner.
    Detects OWASP Top 10 and common security issues.
    """
    
    def __init__(self):
        self.issues = []
        self.secrets_patterns = self._load_secrets_patterns()
        self.sql_patterns = self._load_sql_patterns()
        self.xss_patterns = self._load_xss_patterns()
        
    def scan_file(self, file_path: str) -> List[SecurityIssue]:
        """Comprehensive security scan"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except (IOError, UnicodeDecodeError) as e:
            # Failed to read file
            return []
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []
        
        # Run all security checks
        self._detect_sql_injection(tree, file_path, lines)
        self._detect_xss(tree, file_path, lines)
        self._detect_command_injection(tree, file_path, lines)
        self._detect_path_traversal(tree, file_path, lines)
        self._detect_hardcoded_secrets(content, file_path, lines)
        self._detect_weak_crypto(tree, file_path, lines)
        self._detect_insecure_deserialization(tree, file_path, lines)
        self._detect_xxe(tree, file_path, lines)
        self._detect_ssrf(tree, file_path, lines)
        self._detect_authentication_issues(tree, file_path, lines)
        self._detect_authorization_issues(tree, file_path, lines)
        self._detect_session_issues(tree, file_path, lines)
        self._detect_file_upload_issues(tree, file_path, lines)
        self._detect_regex_dos(tree, file_path, lines)
        
        return self.issues
    
    def _load_secrets_patterns(self) -> List[tuple]:
        """Load patterns for secret detection"""
        return [
            # API Keys
            (r'api[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9]{20,})', 'API Key', 'HIGH'),
            (r'api[_-]?secret["\s]*[:=]["\s]*([a-zA-Z0-9]{20,})', 'API Secret', 'HIGH'),
            
            # AWS
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key', 'CRITICAL'),
            (r'aws[_-]?secret[_-]?access[_-]?key["\s]*[:=]["\s]*([a-zA-Z0-9/+=]{40})', 'AWS Secret', 'CRITICAL'),
            
            # Database
            (r'postgresql://[^:]+:[^@]+@', 'PostgreSQL Connection String', 'CRITICAL'),
            (r'mysql://[^:]+:[^@]+@', 'MySQL Connection String', 'CRITICAL'),
            (r'mongodb://[^:]+:[^@]+@', 'MongoDB Connection String', 'CRITICAL'),
            
            # Private Keys
            (r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----', 'Private Key', 'CRITICAL'),
            
            # Tokens
            (r'github[_-]?token["\s]*[:=]["\s]*([a-zA-Z0-9]{35,})', 'GitHub Token', 'HIGH'),
            (r'slack[_-]?token["\s]*[:=]["\s]*(xox[a-zA-Z]-[a-zA-Z0-9-]+)', 'Slack Token', 'HIGH'),
            
            # Generic Secrets
            (r'password["\s]*[:=]["\s]*["\'](?!.*\{|\}|%|\$)[^"\']{8,}["\']', 'Hardcoded Password', 'HIGH'),
            (r'secret["\s]*[:=]["\s]*["\'](?!.*\{|\}|%|\$)[^"\']{8,}["\']', 'Hardcoded Secret', 'HIGH'),
        ]
    
    def _load_sql_patterns(self) -> List[str]:
        """Load SQL injection patterns"""
        return [
            'execute', 'executemany', 'cursor.execute',
            'raw', 'RawSQL', 'extra',
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP'
        ]
    
    def _load_xss_patterns(self) -> List[str]:
        """Load XSS patterns"""
        return [
            'innerHTML', 'document.write', 'eval',
            'dangerouslySetInnerHTML', '__html'
        ]
    
    def _detect_sql_injection(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect SQL injection vulnerabilities"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check for string formatting in SQL
                if self._is_sql_call(node):
                    # Check if using string concatenation/formatting
                    for arg in ast.walk(node):
                        if isinstance(arg, (ast.BinOp, ast.JoinedStr)):
                            # Check if concatenating with variables
                            if self._has_variable_in_sql(arg):
                                self.issues.append(SecurityIssue(
                                    type='SQL Injection',
                                    severity='CRITICAL',
                                    category='Injection',
                                    description='Potential SQL injection via string concatenation',
                                    file=file_path,
                                    line=node.lineno,
                                    code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                    recommendation='Use parameterized queries or ORM methods. Never concatenate user input into SQL.',
                                    cwe_id='CWE-89',
                                    owasp='A03:2021 - Injection'
                                ))
    
    def _is_sql_call(self, node: ast.Call) -> bool:
        """Check if call is SQL-related"""
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ['execute', 'executemany', 'raw']:
                return True
        elif isinstance(node.func, ast.Name):
            if node.func.id in ['execute', 'executemany']:
                return True
        return False
    
    def _has_variable_in_sql(self, node: ast.AST) -> bool:
        """Check if SQL contains variables"""
        for child in ast.walk(node):
            if isinstance(child, (ast.Name, ast.Attribute)):
                return True
        return False
    
    def _detect_xss(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect XSS vulnerabilities"""
        for node in ast.walk(tree):
            # Check for dangerous functions
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['innerHTML', 'write']:
                        self.issues.append(SecurityIssue(
                            type='Cross-Site Scripting (XSS)',
                            severity='HIGH',
                            category='Injection',
                            description='Potentially unsafe HTML rendering',
                            file=file_path,
                            line=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                            recommendation='Sanitize all user input. Use safe rendering methods or templating engines with auto-escaping.',
                            cwe_id='CWE-79',
                            owasp='A03:2021 - Injection'
                        ))
                
                # Check for eval
                if isinstance(node.func, ast.Name):
                    if node.func.id == 'eval':
                        self.issues.append(SecurityIssue(
                            type='Code Injection',
                            severity='CRITICAL',
                            category='Injection',
                            description='Use of eval() with potential user input',
                            file=file_path,
                            line=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                            recommendation='Never use eval(). Use ast.literal_eval() for safe evaluation or redesign the logic.',
                            cwe_id='CWE-95',
                            owasp='A03:2021 - Injection'
                        ))
    
    def _detect_command_injection(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect command injection"""
        dangerous_functions = ['system', 'popen', 'exec', 'spawn', 'call']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = None
                
                if isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                elif isinstance(node.func, ast.Name):
                    func_name = node.func.id
                
                if func_name in dangerous_functions:
                    # Check if shell=True
                    has_shell = False
                    for keyword in node.keywords:
                        if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant):
                            if keyword.value.value is True:
                                has_shell = True
                    
                    if has_shell or func_name in ['system', 'popen']:
                        self.issues.append(SecurityIssue(
                            type='Command Injection',
                            severity='CRITICAL',
                            category='Injection',
                            description=f'Potential command injection via {func_name}()',
                            file=file_path,
                            line=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                            recommendation='Avoid shell=True. Use subprocess with list arguments. Sanitize all inputs.',
                            cwe_id='CWE-78',
                            owasp='A03:2021 - Injection'
                        ))
    
    def _detect_path_traversal(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect path traversal vulnerabilities"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == 'open':
                        # Check if filename comes from user input
                        if node.args and isinstance(node.args[0], (ast.Name, ast.BinOp, ast.JoinedStr)):
                            self.issues.append(SecurityIssue(
                                type='Path Traversal',
                                severity='HIGH',
                                category='Injection',
                                description='File path constructed from user input',
                                file=file_path,
                                line=node.lineno,
                                code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                recommendation='Validate file paths. Use os.path.basename() and check against whitelist.',
                                cwe_id='CWE-22',
                                owasp='A01:2021 - Broken Access Control'
                            ))
    
    def _detect_hardcoded_secrets(self, content: str, file_path: str, lines: List[str]):
        """Detect hardcoded secrets"""
        for pattern, secret_type, severity in self.secrets_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:match.start()].count('\n') + 1
                
                self.issues.append(SecurityIssue(
                    type='Hardcoded Secret',
                    severity=severity,
                    category='Sensitive Data Exposure',
                    description=f'{secret_type} hardcoded in source',
                    file=file_path,
                    line=line_num,
                    code_snippet=lines[line_num - 1] if line_num <= len(lines) else '',
                    recommendation='Use environment variables or secure vaults (e.g., AWS Secrets Manager, HashiCorp Vault).',
                    cwe_id='CWE-798',
                    owasp='A02:2021 - Cryptographic Failures'
                ))
    
    def _detect_weak_crypto(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect weak cryptography"""
        weak_algos = {
            'md5': ('MD5', 'Use SHA-256 or better'),
            'sha1': ('SHA-1', 'Use SHA-256 or better'),
            'DES': ('DES', 'Use AES-256'),
            'RC4': ('RC4', 'Use AES-256'),
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    algo = node.func.attr.lower()
                    for weak, (name, recommendation) in weak_algos.items():
                        if weak.lower() in algo:
                            self.issues.append(SecurityIssue(
                                type='Weak Cryptography',
                                severity='HIGH',
                                category='Cryptographic Failures',
                                description=f'Use of weak algorithm: {name}',
                                file=file_path,
                                line=node.lineno,
                                code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                recommendation=recommendation,
                                cwe_id='CWE-327',
                                owasp='A02:2021 - Cryptographic Failures'
                            ))
    
    def _detect_insecure_deserialization(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect insecure deserialization"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['loads', 'load']:
                        # Check if pickle
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id == 'pickle':
                                self.issues.append(SecurityIssue(
                                    type='Insecure Deserialization',
                                    severity='CRITICAL',
                                    category='Deserialization',
                                    description='Unsafe deserialization with pickle',
                                    file=file_path,
                                    line=node.lineno,
                                    code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                    recommendation='Never unpickle untrusted data. Use JSON or other safe formats.',
                                    cwe_id='CWE-502',
                                    owasp='A08:2021 - Software and Data Integrity Failures'
                                ))
    
    def _detect_xxe(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect XML External Entity (XXE) vulnerabilities"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if 'parse' in node.func.attr.lower() and 'xml' in str(node.func.value).lower():
                        self.issues.append(SecurityIssue(
                            type='XML External Entity (XXE)',
                            severity='HIGH',
                            category='Injection',
                            description='Potentially unsafe XML parsing',
                            file=file_path,
                            line=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                            recommendation='Disable external entities in XML parser. Use defusedxml library.',
                            cwe_id='CWE-611',
                            owasp='A05:2021 - Security Misconfiguration'
                        ))
    
    def _detect_ssrf(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect Server-Side Request Forgery"""
        http_functions = ['get', 'post', 'request', 'urlopen']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in http_functions:
                        # Check if URL comes from user input
                        if node.args and isinstance(node.args[0], (ast.Name, ast.BinOp, ast.JoinedStr)):
                            self.issues.append(SecurityIssue(
                                type='Server-Side Request Forgery (SSRF)',
                                severity='HIGH',
                                category='SSRF',
                                description='HTTP request with user-controlled URL',
                                file=file_path,
                                line=node.lineno,
                                code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                recommendation='Validate URLs against whitelist. Block internal IPs.',
                                cwe_id='CWE-918',
                                owasp='A10:2021 - Server-Side Request Forgery'
                            ))
    
    def _detect_authentication_issues(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect authentication issues"""
        for node in ast.walk(tree):
            # Check for == comparison with passwords
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, ast.Eq):
                        # Check if comparing with password-like variables
                        for comparator in [node.left] + node.comparators:
                            if isinstance(comparator, ast.Name):
                                if 'password' in comparator.id.lower():
                                    self.issues.append(SecurityIssue(
                                        type='Insecure Authentication',
                                        severity='CRITICAL',
                                        category='Authentication',
                                        description='Password comparison using == (timing attack)',
                                        file=file_path,
                                        line=node.lineno,
                                        code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                        recommendation='Use constant-time comparison (hmac.compare_digest)',
                                        cwe_id='CWE-208',
                                        owasp='A07:2021 - Identification and Authentication Failures'
                                    ))
    
    def _detect_authorization_issues(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect authorization issues"""
        # This is a simplified check - would need more context in real implementation
        pass
    
    def _detect_session_issues(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect session management issues"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if 'session' in target.id.lower():
                            # Check if using secure flags
                            if isinstance(node.value, ast.Dict):
                                keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
                                if 'secure' not in [k.lower() if isinstance(k, str) else k for k in keys]:
                                    self.issues.append(SecurityIssue(
                                        type='Insecure Session',
                                        severity='MEDIUM',
                                        category='Session Management',
                                        description='Session cookie without Secure flag',
                                        file=file_path,
                                        line=node.lineno,
                                        code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                        recommendation='Set Secure, HttpOnly, and SameSite flags on session cookies',
                                        cwe_id='CWE-614',
                                        owasp='A07:2021 - Identification and Authentication Failures'
                                    ))
    
    def _detect_file_upload_issues(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect file upload vulnerabilities"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if 'save' in node.func.attr.lower():
                        self.issues.append(SecurityIssue(
                            type='Insecure File Upload',
                            severity='HIGH',
                            category='File Upload',
                            description='Potential insecure file upload',
                            file=file_path,
                            line=node.lineno,
                            code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                            recommendation='Validate file type, size, and extension. Store outside webroot. Use random filenames.',
                            cwe_id='CWE-434',
                            owasp='A04:2021 - Insecure Design'
                        ))
    
    def _detect_regex_dos(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Detect ReDoS vulnerabilities"""
        dangerous_patterns = [
            r'(a+)+',
            r'(a*)*',
            r'(a|a)*',
            r'(a|ab)*',
        ]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['match', 'search', 'findall', 'compile']:
                        if node.args:
                            pattern_node = node.args[0]
                            if isinstance(pattern_node, ast.Constant):
                                pattern = str(pattern_node.value)
                                # Simple ReDoS check
                                if '(.*)*' in pattern or '(.+)+' in pattern:
                                    self.issues.append(SecurityIssue(
                                        type='Regular Expression DoS',
                                        severity='MEDIUM',
                                        category='DoS',
                                        description='Potentially catastrophic regex pattern',
                                        file=file_path,
                                        line=node.lineno,
                                        code_snippet=lines[node.lineno - 1] if node.lineno <= len(lines) else '',
                                        recommendation='Avoid nested quantifiers. Use atomic groups or possessive quantifiers.',
                                        cwe_id='CWE-1333',
                                        owasp='A04:2021 - Insecure Design'
                                    ))
    
    def get_report(self) -> Dict[str, Any]:
        """Generate security report"""
        by_severity = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        by_category = {}
        
        for issue in self.issues:
            by_severity[issue.severity] += 1
            by_category[issue.category] = by_category.get(issue.category, 0) + 1
        
        # Calculate security score
        score = 100.0
        score -= by_severity['CRITICAL'] * 25
        score -= by_severity['HIGH'] * 15
        score -= by_severity['MEDIUM'] * 8
        score -= by_severity['LOW'] * 3
        score = max(0, score)
        
        return {
            'total_issues': len(self.issues),
            'by_severity': by_severity,
            'by_category': by_category,
            'security_score': round(score, 1),
            'issues': [
                {
                    'type': i.type,
                    'severity': i.severity,
                    'category': i.category,
                    'description': i.description,
                    'line': i.line,
                    'recommendation': i.recommendation,
                    'cwe': i.cwe_id,
                    'owasp': i.owasp
                }
                for i in self.issues
            ]
        }


if __name__ == '__main__':
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python advanced_security.py <file.py>")
        sys.exit(1)
    
    scanner = AdvancedSecurityScanner()
    issues = scanner.scan_file(sys.argv[1])
    report = scanner.get_report()
    
    print("="*70)
    print("ADVANCED SECURITY SCAN")
    print("="*70)
    print(f"\nSecurity Score: {report['security_score']}/100")
    print(f"Total Issues: {report['total_issues']}")
    print(f"\nBy Severity:")
    for sev, count in report['by_severity'].items():
        if count > 0:
            print(f"  {sev}: {count}")
    
    if report['issues']:
        print(f"\nTop Issues:")
        for issue in report['issues'][:5]:
            print(f"\n[{issue['severity']}] {issue['type']} (Line {issue['line']})")
            print(f"  {issue['description']}")
            print(f"  💡 {issue['recommendation']}")
            print(f"  🔗 {issue['owasp']}")
