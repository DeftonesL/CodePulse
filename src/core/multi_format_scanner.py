import re
import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class SecurityIssue:
    pass
    type: str
    severity: str
    description: str
    line: int
    code_snippet: str
    recommendation: str

class HTMLScanner:
    pass
    
    def __init__(self):
        self.issues = []
        
    def scan(self, file_path: str) -> List[SecurityIssue]:
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except:
            return []
        
        # Check for XSS vulnerabilities
        self._check_inline_scripts(lines, file_path)
        self._check_dangerous_attributes(lines, file_path)
        self._check_external_resources(lines, file_path)
        self._check_form_security(lines, file_path)
        self._check_iframe_usage(lines, file_path)
        self._check_meta_tags(lines, file_path)
        
        return self.issues
    
    def _check_inline_scripts(self, lines: List[str], file_path: str):
        dangerous_patterns = [
            (r'<script[^>]*>.*?</script>', 'Inline Script', 'HIGH'),
            (r'on\w+\s*=\s*["\']', 'Inline Event Handler', 'HIGH'),
            (r'javascript:', 'JavaScript Protocol', 'HIGH'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, issue_type, severity in dangerous_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(SecurityIssue(
                        type=issue_type,
                        severity=severity,
                        description=f'Found {issue_type.lower()} - potential XSS vector',
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Use Content Security Policy (CSP) and avoid inline scripts. Move to external .js files.'
                    ))
    
    def _check_dangerous_attributes(self, lines: List[str], file_path: str):
        dangerous_attrs = [
            (r'innerHTML\s*=', 'innerHTML Assignment', 'Use textContent or sanitize input'),
            (r'document\.write', 'document.write', 'Use modern DOM methods'),
            (r'eval\s*\(', 'eval() Usage', 'Never use eval() - code injection risk'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, issue_type, recommendation in dangerous_attrs:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(SecurityIssue(
                        type=issue_type,
                        severity='HIGH',
                        description=f'Dangerous pattern: {issue_type}',
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation=recommendation
                    ))
    
    def _check_external_resources(self, lines: List[str], file_path: str):
        for i, line in enumerate(lines, 1):
            # HTTP resources (should be HTTPS)
            if re.search(r'(src|href)\s*=\s*["\']http://', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    type='Insecure Resource',
                    severity='MEDIUM',
                    description='Loading resource over HTTP instead of HTTPS',
                    line=i,
                    code_snippet=line.strip()[:80],
                    recommendation='Use HTTPS for all external resources to prevent MITM attacks'
                ))
            
            # CDN without SRI
            if 'cdn' in line.lower() and 'integrity=' not in line:
                self.issues.append(SecurityIssue(
                    type='Missing SRI',
                    severity='MEDIUM',
                    description='CDN resource without Subresource Integrity',
                    line=i,
                    code_snippet=line.strip()[:80],
                    recommendation='Add integrity and crossorigin attributes for CDN resources'
                ))
    
    def _check_form_security(self, lines: List[str], file_path: str):
        for i, line in enumerate(lines, 1):
            if '<form' in line.lower():
                # Check for CSRF token
                form_block = '\n'.join(lines[i-1:min(i+10, len(lines))])
                
                if 'action=' in form_block and 'csrf' not in form_block.lower():
                    self.issues.append(SecurityIssue(
                        type='Missing CSRF Protection',
                        severity='HIGH',
                        description='Form without CSRF token',
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Add CSRF token to all forms that modify data'
                    ))
                
                # Check for autocomplete on sensitive fields
                if 'password' in form_block.lower() and 'autocomplete="off"' not in form_block:
                    self.issues.append(SecurityIssue(
                        type='Autocomplete on Password',
                        severity='LOW',
                        description='Password field allows autocomplete',
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Add autocomplete="off" to sensitive fields'
                    ))
    
    def _check_iframe_usage(self, lines: List[str], file_path: str):
        for i, line in enumerate(lines, 1):
            if '<iframe' in line.lower():
                if 'sandbox=' not in line:
                    self.issues.append(SecurityIssue(
                        type='Unsafe iframe',
                        severity='HIGH',
                        description='iframe without sandbox attribute',
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Add sandbox attribute to restrict iframe capabilities'
                    ))
    
    def _check_meta_tags(self, lines: List[str], file_path: str):
        content = '\n'.join(lines)
        
        # Check for CSP
        if 'Content-Security-Policy' not in content:
            self.issues.append(SecurityIssue(
                type='Missing CSP',
                severity='MEDIUM',
                description='No Content-Security-Policy meta tag',
                line=1,
                code_snippet='<head>',
                recommendation='Add CSP meta tag to prevent XSS: <meta http-equiv="Content-Security-Policy" content="default-src \'self\'">'
            ))
        
        # Check for X-Frame-Options
        if 'X-Frame-Options' not in content and '<iframe' in content:
            self.issues.append(SecurityIssue(
                type='Missing X-Frame-Options',
                severity='MEDIUM',
                description='No clickjacking protection',
                line=1,
                code_snippet='<head>',
                recommendation='Add X-Frame-Options to prevent clickjacking'
            ))

class JSONScanner:
    pass
    
    def __init__(self):
        self.issues = []
    
    def scan(self, file_path: str) -> List[SecurityIssue]:
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return []
        
        # Check syntax
        try:
            data = json.loads(content)
            self._check_sensitive_data(data, file_path)
            self._check_structure(data, file_path)
        except json.JSONDecodeError as e:
            self.issues.append(SecurityIssue(
                type='JSON Syntax Error',
                severity='CRITICAL',
                description=f'Invalid JSON: {e.msg}',
                line=e.lineno,
                code_snippet=content.split('\n')[e.lineno-1] if e.lineno <= len(content.split('\n')) else '',
                recommendation=f'Fix JSON syntax at line {e.lineno}, column {e.colno}'
            ))
        
        # Check for secrets in raw content
        self._check_secrets(content, file_path)
        
        return self.issues
    
    def _check_sensitive_data(self, data: Any, file_path: str):
        sensitive_keys = ['password', 'secret', 'api_key', 'token', 'private_key', 'aws_access']
        
        def check_dict(d, path=''):
            if isinstance(d, dict):
                for key, value in d.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Check key names
                    for sensitive in sensitive_keys:
                        if sensitive in key.lower():
                            self.issues.append(SecurityIssue(
                                type='Sensitive Data Exposure',
                                severity='HIGH',
                                description=f'Sensitive key "{key}" found in JSON',
                                line=1,
                                code_snippet=f'"{key}": "{str(value)[:30]}..."',
                                recommendation='Never store secrets in JSON config files. Use environment variables or secure vaults.'
                            ))
                    
                    check_dict(value, current_path)
            elif isinstance(d, list):
                for item in d:
                    check_dict(item, path)
        
        check_dict(data)
    
    def _check_structure(self, data: Any, file_path: str):
        if isinstance(data, dict):
            # Very large objects
            if len(str(data)) > 1000000:  # 1MB
                self.issues.append(SecurityIssue(
                    type='Large JSON Object',
                    severity='LOW',
                    description='JSON file is very large (>1MB)',
                    line=1,
                    code_snippet='{ ... }',
                    recommendation='Consider splitting into smaller files or using database'
                ))
    
    def _check_secrets(self, content: str, file_path: str):
        secret_patterns = [
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
            (r'sk-[a-zA-Z0-9]{32,}', 'OpenAI API Key'),
            (r'ghp_[a-zA-Z0-9]{36,}', 'GitHub Token'),
            (r'xox[a-zA-Z]-[a-zA-Z0-9-]+', 'Slack Token'),
        ]
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, secret_type in secret_patterns:
                if re.search(pattern, line):
                    self.issues.append(SecurityIssue(
                        type='Hardcoded Secret',
                        severity='CRITICAL',
                        description=f'{secret_type} found in JSON file',
                        line=i,
                        code_snippet=line.strip()[:60] + '...',
                        recommendation='Remove secret immediately. Use environment variables or secret management.'
                    ))

class SQLScanner:
    pass
    
    def __init__(self):
        self.issues = []
    
    def scan(self, file_path: str) -> List[SecurityIssue]:
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except:
            return []
        
        self._check_sql_injection_patterns(lines, file_path)
        self._check_dangerous_operations(lines, file_path)
        self._check_authentication(lines, file_path)
        self._check_permissions(lines, file_path)
        
        return self.issues
    
    def _check_sql_injection_patterns(self, lines: List[str], file_path: str):
        dangerous_patterns = [
            (r'EXEC\s*\(', 'Dynamic SQL Execution'),
            (r'EXECUTE\s+IMMEDIATE', 'Dynamic SQL Execution'),
            (r';\s*DROP\s+TABLE', 'DROP TABLE Statement'),
            (r';\s*DELETE\s+FROM', 'DELETE Statement'),
            (r'--', 'SQL Comment (potential injection)'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, issue_type in dangerous_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(SecurityIssue(
                        type=issue_type,
                        severity='HIGH',
                        description=f'Potentially dangerous SQL pattern: {issue_type}',
                        line=i,
                        code_snippet=line.strip()[:80],
                        recommendation='Use parameterized queries. Never concatenate user input in SQL.'
                    ))
    
    def _check_dangerous_operations(self, lines: List[str], file_path: str):
        for i, line in enumerate(lines, 1):
            # DROP DATABASE
            if re.search(r'DROP\s+DATABASE', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    type='DROP DATABASE',
                    severity='CRITICAL',
                    description='DROP DATABASE command found',
                    line=i,
                    code_snippet=line.strip(),
                    recommendation='Ensure this is intentional and has proper safeguards'
                ))
            
            # TRUNCATE
            if re.search(r'TRUNCATE\s+TABLE', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    type='TRUNCATE TABLE',
                    severity='HIGH',
                    description='TRUNCATE TABLE command (irreversible)',
                    line=i,
                    code_snippet=line.strip(),
                    recommendation='Ensure backup exists before truncating'
                ))
            
            # SELECT *
            if re.search(r'SELECT\s+\*\s+FROM', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    type='SELECT *',
                    severity='LOW',
                    description='Using SELECT * - performance and security issue',
                    line=i,
                    code_snippet=line.strip(),
                    recommendation='Explicitly list required columns instead of SELECT *'
                ))
    
    def _check_authentication(self, lines: List[str], file_path: str):
        for i, line in enumerate(lines, 1):
            # Hardcoded passwords
            if re.search(r'PASSWORD\s*=\s*[\'"][^\'"]+[\'"]', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    type='Hardcoded Password',
                    severity='CRITICAL',
                    description='Hardcoded password in SQL file',
                    line=i,
                    code_snippet='PASSWORD = \'***\'',
                    recommendation='Use environment variables or secure configuration'
                ))
            
            # Weak password storage
            if re.search(r'PASSWORD\s*,\s*VARCHAR', line, re.IGNORECASE):
                if 'HASH' not in line.upper() and 'ENCRYPT' not in line.upper():
                    self.issues.append(SecurityIssue(
                        type='Plain Text Password Storage',
                        severity='CRITICAL',
                        description='Password column without hash/encryption',
                        line=i,
                        code_snippet=line.strip(),
                        recommendation='Always hash passwords (bcrypt, Argon2). Never store plain text.'
                    ))
    
    def _check_permissions(self, lines: List[str], file_path: str):
        for i, line in enumerate(lines, 1):
            # GRANT ALL
            if re.search(r'GRANT\s+ALL', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    type='Excessive Permissions',
                    severity='HIGH',
                    description='GRANT ALL PRIVILEGES - too permissive',
                    line=i,
                    code_snippet=line.strip(),
                    recommendation='Grant only necessary permissions (principle of least privilege)'
                ))
            
            # Public access
            if re.search(r'TO\s+PUBLIC', line, re.IGNORECASE):
                self.issues.append(SecurityIssue(
                    type='Public Access',
                    severity='HIGH',
                    description='Granting permissions to PUBLIC',
                    line=i,
                    code_snippet=line.strip(),
                    recommendation='Grant to specific users/roles, not PUBLIC'
                ))

class MultiFormatScanner:
    pass
    
    def __init__(self):
        self.html_scanner = HTMLScanner()
        self.json_scanner = JSONScanner()
        self.sql_scanner = SQLScanner()
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        
        issues = []
        file_type = 'unknown'
        
        if ext in ['.html', '.htm']:
            issues = self.html_scanner.scan(file_path)
            file_type = 'HTML'
        elif ext == '.json':
            issues = self.json_scanner.scan(file_path)
            file_type = 'JSON'
        elif ext == '.sql':
            issues = self.sql_scanner.scan(file_path)
            file_type = 'SQL'
        
        # Convert to dict
        issues_dict = [
            {
                'type': i.type,
                'severity': i.severity,
                'description': i.description,
                'line': i.line,
                'code_snippet': i.code_snippet,
                'recommendation': i.recommendation
            }
            for i in issues
        ]
        
        # Calculate score
        score = 100.0
        for issue in issues:
            if issue.severity == 'CRITICAL':
                score -= 20
            elif issue.severity == 'HIGH':
                score -= 10
            elif issue.severity == 'MEDIUM':
                score -= 5
            elif issue.severity == 'LOW':
                score -= 2
        score = max(0, score)
        
        return {
            'file_type': file_type,
            'total_issues': len(issues),
            'issues': issues_dict,
            'score': round(score, 1),
            'by_severity': self._count_by_severity(issues)
        }
    
    def _count_by_severity(self, issues: List[SecurityIssue]) -> Dict[str, int]:
        counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for issue in issues:
            counts[issue.severity] = counts.get(issue.severity, 0) + 1
        return counts

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python multi_format_scanner.py <file>")
        sys.exit(1)
    
    scanner = MultiFormatScanner()
    result = scanner.scan_file(sys.argv[1])
    
    print(f"\n{'='*70}")
    print(f"FILE SECURITY SCAN - {result['file_type']}")
    print(f"{'='*70}")
    print(f"\nScore: {result['score']}/100")
    print(f"Total Issues: {result['total_issues']}\n")
    
    if result['total_issues'] > 0:
        print("By Severity:")
        for sev, count in result['by_severity'].items():
            if count > 0:
                print(f"  {sev}: {count}")
        
        print(f"\nIssues:")
        for issue in result['issues'][:10]:
            print(f"\n[{issue['severity']}] {issue['type']} (Line {issue['line']})")
            print(f"  {issue['description']}")
            print(f"  💡 {issue['recommendation']}")
    else:
        print("✅ No issues found!")
