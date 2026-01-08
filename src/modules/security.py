import re
import os
import logging
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    pass
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class VulnerabilityType(Enum):
    pass
    SECRET_EXPOSURE = "secret_exposure"
    SQL_INJECTION = "sql_injection"
    XSS = "cross_site_scripting"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    WEAK_CRYPTO = "weak_cryptography"
    HARDCODED_CREDENTIALS = "hardcoded_credentials"

@dataclass
class SecurityIssue:
    pass
    file_path: str
    line_number: int
    severity: SecurityLevel
    vulnerability_type: VulnerabilityType
    title: str
    description: str
    remediation: str
    code_snippet: Optional[str] = None
    cwe_id: Optional[str] = None  # Common Weakness Enumeration ID
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['severity'] = self.severity.value
        data['vulnerability_type'] = self.vulnerability_type.value
        return data

class SecurityScanner:
    pass
    
    # Patterns for detecting secrets and credentials
    SECRET_PATTERNS = {
        'aws_access_key': (
            r'AKIA[0-9A-Z]{16}',
            'AWS Access Key ID',
            'CWE-798'
        ),
        'aws_secret_key': (
            r'(?i)aws_secret_access_key["\']?\s*[:=]\s*["\']?([A-Za-z0-9/+=]{40})',
            'AWS Secret Access Key',
            'CWE-798'
        ),
        'github_token': (
            r'ghp_[a-zA-Z0-9]{36}',
            'GitHub Personal Access Token',
            'CWE-798'
        ),
        'google_api_key': (
            r'AIza[0-9A-Za-z\\-_]{35}',
            'Google API Key',
            'CWE-798'
        ),
        'slack_token': (
            r'xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[a-zA-Z0-9]{24,32}',
            'Slack Token',
            'CWE-798'
        ),
        'generic_api_key': (
            r'(?i)(api[_-]?key|apikey|api[_-]?secret)["\']?\s*[:=]\s*["\']([a-zA-Z0-9]{20,})',
            'Generic API Key',
            'CWE-798'
        ),
        'private_key': (
            r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
            'Private Key',
            'CWE-798'
        ),
        'password': (
            r'(?i)(password|passwd|pwd)["\']?\s*[:=]\s*["\'](?![\s*$\{])[^"\'\s]{8,}',
            'Hardcoded Password',
            'CWE-798'
        ),
        'jwt_token': (
            r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
            'JWT Token',
            'CWE-798'
        )
    }
    
    # Patterns for SQL injection vulnerabilities
    SQL_INJECTION_PATTERNS = [
        (r'execute\([^)]*%s', 'String formatting in SQL execute'),
        (r'execute\([^)]*\.format\(', 'String format in SQL execute'),
        (r'execute\([^)]*f["\']', 'f-string in SQL execute'),
        (r'cursor\.execute\([^)]*\+', 'String concatenation in SQL execute'),
        (r'SELECT.*FROM.*WHERE.*\+', 'SQL query with string concatenation'),
        (r'SELECT.*FROM.*WHERE.*\.format\(', 'SQL query with format method'),
        (r'SELECT.*FROM.*WHERE.*f["\']', 'SQL query with f-string'),
    ]
    
    # Patterns for command injection
    COMMAND_INJECTION_PATTERNS = [
        (r'os\.system\([^)]*\+', 'Command injection via os.system'),
        (r'subprocess\.(call|run|Popen)\([^)]*\+', 'Command injection via subprocess'),
        (r'eval\(', 'Dangerous use of eval()'),
        (r'exec\(', 'Dangerous use of exec()'),
    ]
    
    # Weak cryptographic patterns
    WEAK_CRYPTO_PATTERNS = [
        (r'hashlib\.md5\(', 'Use of MD5 (cryptographically broken)'),
        (r'hashlib\.sha1\(', 'Use of SHA1 (weak for security)'),
        (r'random\.random\(', 'Use of random instead of secrets for security'),
        (r'(?i)des|rc4|rc2', 'Weak encryption algorithm'),
    ]
    
    # Path traversal patterns
    PATH_TRAVERSAL_PATTERNS = [
        (r'open\([^)]*\+', 'Potential path traversal in file open'),
        (r'os\.path\.join\([^)]*input', 'User input in path join'),
        (r'\.\./|\.\.\\\\', 'Directory traversal pattern in string'),
    ]
    
    def __init__(self):
        logger.info("Initialized Security Scanner")
    
    def scan_for_secrets(self, content: str, file_path: str) -> List[SecurityIssue]:
        issues = []
        lines = content.split('\n')
        
        for secret_type, (pattern, description, cwe) in self.SECRET_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                # Skip comments
                if line.strip().startswith('#'):
                    continue
                
                matches = re.finditer(pattern, line)
                for match in matches:
                    # Create a masked version of the secret
                    secret = match.group(0) if match.lastindex is None else match.group(1)
                    masked_secret = secret[:4] + '*' * (len(secret) - 8) + secret[-4:] if len(secret) > 8 else '*' * len(secret)
                    
                    issue = SecurityIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity=SecurityLevel.CRITICAL,
                        vulnerability_type=VulnerabilityType.SECRET_EXPOSURE,
                        title=f"{description} detected",
                        description=f"Hardcoded secret found: {masked_secret}. Secrets should never be stored in code.",
                        remediation="Move secrets to environment variables or a secure secret management system (e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).",
                        code_snippet=line.strip(),
                        cwe_id=cwe
                    )
                    issues.append(issue)
        
        return issues
    
    def scan_for_sql_injection(self, content: str, file_path: str) -> List[SecurityIssue]:
        issues = []
        lines = content.split('\n')
        
        for pattern, description in self.SQL_INJECTION_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    issue = SecurityIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity=SecurityLevel.HIGH,
                        vulnerability_type=VulnerabilityType.SQL_INJECTION,
                        title="Potential SQL Injection vulnerability",
                        description=f"{description}. This could allow attackers to execute arbitrary SQL commands.",
                        remediation="Use parameterized queries or an ORM. Replace string concatenation/formatting with query parameters.",
                        code_snippet=line.strip(),
                        cwe_id="CWE-89"
                    )
                    issues.append(issue)
        
        return issues
    
    def scan_for_command_injection(self, content: str, file_path: str) -> List[SecurityIssue]:
        issues = []
        lines = content.split('\n')
        
        for pattern, description in self.COMMAND_INJECTION_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    severity = SecurityLevel.CRITICAL if 'eval' in pattern or 'exec' in pattern else SecurityLevel.HIGH
                    
                    issue = SecurityIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity=severity,
                        vulnerability_type=VulnerabilityType.COMMAND_INJECTION,
                        title="Command injection vulnerability",
                        description=f"{description}. Attackers could execute arbitrary system commands.",
                        remediation="Avoid using shell=True, validate and sanitize all inputs, use subprocess with list arguments instead of strings.",
                        code_snippet=line.strip(),
                        cwe_id="CWE-78"
                    )
                    issues.append(issue)
        
        return issues
    
    def scan_for_weak_crypto(self, content: str, file_path: str) -> List[SecurityIssue]:
        issues = []
        lines = content.split('\n')
        
        for pattern, description in self.WEAK_CRYPTO_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    issue = SecurityIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity=SecurityLevel.MEDIUM,
                        vulnerability_type=VulnerabilityType.WEAK_CRYPTO,
                        title="Weak cryptographic algorithm",
                        description=f"{description}. This algorithm is not suitable for security-sensitive operations.",
                        remediation="Use SHA-256 or SHA-3 for hashing, secrets module for random values, and AES-256 for encryption.",
                        code_snippet=line.strip(),
                        cwe_id="CWE-327"
                    )
                    issues.append(issue)
        
        return issues
    
    def scan_for_path_traversal(self, content: str, file_path: str) -> List[SecurityIssue]:
        issues = []
        lines = content.split('\n')
        
        for pattern, description in self.PATH_TRAVERSAL_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    issue = SecurityIssue(
                        file_path=file_path,
                        line_number=line_num,
                        severity=SecurityLevel.HIGH,
                        vulnerability_type=VulnerabilityType.PATH_TRAVERSAL,
                        title="Path traversal vulnerability",
                        description=f"{description}. Attackers could access files outside intended directory.",
                        remediation="Validate file paths, use os.path.abspath() and check if result is within allowed directory.",
                        code_snippet=line.strip(),
                        cwe_id="CWE-22"
                    )
                    issues.append(issue)
        
        return issues
    
    def scan_file(self, file_path: str) -> List[SecurityIssue]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Could not read {file_path}: {e}")
            return []
        
        all_issues = []
        
        # Run all security scans
        all_issues.extend(self.scan_for_secrets(content, file_path))
        all_issues.extend(self.scan_for_sql_injection(content, file_path))
        all_issues.extend(self.scan_for_command_injection(content, file_path))
        all_issues.extend(self.scan_for_weak_crypto(content, file_path))
        all_issues.extend(self.scan_for_path_traversal(content, file_path))
        
        return all_issues
    
    def generate_report(self, issues: List[SecurityIssue]) -> Dict:
        # Count by severity
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        # Count by type
        type_counts = {}
        
        for issue in issues:
            severity_counts[issue.severity.value] += 1
            vuln_type = issue.vulnerability_type.value
            type_counts[vuln_type] = type_counts.get(vuln_type, 0) + 1
        
        # Calculate security score (0-100)
        total_issues = len(issues)
        if total_issues == 0:
            security_score = 100
        else:
            # Weight issues by severity
            weighted_score = (
                severity_counts['critical'] * 10 +
                severity_counts['high'] * 5 +
                severity_counts['medium'] * 2 +
                severity_counts['low'] * 1
            )
            security_score = max(0, 100 - weighted_score)
        
        return {
            'total_issues': total_issues,
            'security_score': security_score,
            'severity_breakdown': severity_counts,
            'vulnerability_types': type_counts,
            'issues': [issue.to_dict() for issue in issues]
        }

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python security.py <file_or_directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = SecurityScanner()
    
    # Scan target
    all_issues = []
    if os.path.isfile(target):
        all_issues = scanner.scan_file(target)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    all_issues.extend(scanner.scan_file(file_path))
    
    # Generate report
    report = scanner.generate_report(all_issues)
    
    # Display results
    print(f"\n{'='*60}")
    print(f"🔒 Security Scan Results")
    print(f"{'='*60}\n")
    print(f"Security Score: {report['security_score']}/100")
    print(f"Total Issues: {report['total_issues']}\n")
    
    print("Severity Breakdown:")
    for severity, count in report['severity_breakdown'].items():
        if count > 0:
            print(f"  • {severity.upper()}: {count}")
    
    if report['total_issues'] > 0:
        print(f"\n🔴 Critical Issues:")
        for issue_dict in report['issues']:
            if issue_dict['severity'] == 'critical':
                print(f"\n  {issue_dict['title']}")
                print(f"  File: {issue_dict['file_path']}:{issue_dict['line_number']}")
                print(f"  {issue_dict['description']}")

if __name__ == '__main__':
    main()
