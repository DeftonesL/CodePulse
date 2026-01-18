# Security Patterns and Detection Rules

This document describes the security patterns CodePulse detects and the methodology behind vulnerability identification.

## OWASP Top 10 Coverage

CodePulse addresses all OWASP Top 10 categories:

### A01:2021 - Broken Access Control
**Detection Patterns:**
- Missing authorization checks
- Insecure direct object references
- Path traversal attempts: `../`, directory traversal
- Unrestricted file access

**Languages:** All
**Severity:** High to Critical

### A02:2021 - Cryptographic Failures
**Detection Patterns:**
- Hardcoded passwords and secrets
- Weak hashing algorithms: MD5, SHA1 for passwords
- Insecure random number generation
- Unencrypted sensitive data storage

**Languages:** Python, JavaScript, Java, C#, PHP, Ruby
**Severity:** High to Critical

### A03:2021 - Injection
**Detection Patterns:**

**SQL Injection:**
- String concatenation in SQL: `"SELECT * FROM users WHERE id = " + userId`
- String formatting: `f"SELECT * FROM table WHERE {column}"`
- Unsafe query building without parameterization

**Command Injection:**
- `os.system()`, `subprocess.call()` with user input
- `eval()`, `exec()` with untrusted data
- Shell command construction with string concatenation

**Code Injection:**
- `eval()` in JavaScript, Python, Ruby, PHP
- `Function()` constructor in JavaScript
- Dynamic code loading with user input

**Languages:** All major languages
**Severity:** Critical

### A04:2021 - Insecure Design
**Detection Patterns:**
- Missing rate limiting indicators
- Absence of input validation
- Insecure session management patterns

**Languages:** All
**Severity:** Medium to High

### A05:2021 - Security Misconfiguration
**Detection Patterns:**
- Debug mode enabled in production
- Default credentials in configuration
- Unnecessary services enabled
- Missing security headers

**Languages:** Configuration files, Python, JavaScript, Java
**Severity:** Medium to High

### A06:2021 - Vulnerable and Outdated Components
**Detection Patterns:**
- Import of deprecated modules
- Usage of known vulnerable functions
- Outdated library patterns

**Languages:** All with package management
**Severity:** Varies

### A07:2021 - Identification and Authentication Failures
**Detection Patterns:**
- Weak password policies
- Missing multi-factor authentication
- Insecure session tokens
- Credential exposure in code

**Languages:** All
**Severity:** High to Critical

### A08:2021 - Software and Data Integrity Failures
**Detection Patterns:**
- Insecure deserialization: `pickle.loads()`, `unserialize()`
- Missing integrity checks on downloads
- Auto-update without verification

**Languages:** Python, PHP, Java, JavaScript
**Severity:** High to Critical

### A09:2021 - Security Logging and Monitoring Failures
**Detection Patterns:**
- Sensitive data in logs
- Missing error handling
- Inadequate logging of security events

**Languages:** All
**Severity:** Medium

### A10:2021 - Server-Side Request Forgery (SSRF)
**Detection Patterns:**
- HTTP requests with user-controlled URLs
- Unvalidated redirect targets
- URL parameter injection

**Languages:** Python, JavaScript, PHP, Java, Go
**Severity:** High to Critical

## Language-Specific Patterns

### Python

**High Severity:**
```python
eval(user_input)
exec(user_code)
__import__(module_name)
pickle.loads(data)
yaml.load(content)
subprocess.call(shell=True)
```

**Medium Severity:**
```python
open(filename, 'w')
os.remove(path)
shutil.rmtree(directory)
```

**Detection Method:** AST analysis for context-aware detection

### JavaScript/TypeScript

**High Severity:**
```javascript
eval(userInput)
Function(code)()
innerHTML = userContent
document.write(data)
dangerouslySetInnerHTML={{__html: content}}
```

**Medium Severity:**
```javascript
localStorage.setItem('password', pwd)
sessionStorage.setItem('token', token)
```

**Detection Method:** Regex patterns with context analysis

### PHP

**Critical Severity:**
```php
eval($code)
exec($command)
system($cmd)
passthru($command)
assert($code)
unserialize($data)
```

**High Severity:**
```php
include($_GET['file'])
require($user_path)
mysql_query($sql)
```

**Detection Method:** Pattern matching with common vulnerable functions

### Java

**Critical Severity:**
```java
Runtime.getRuntime().exec(command)
ProcessBuilder(userInput)
ScriptEngineManager.eval(code)
ObjectInputStream.readObject()
```

**High Severity:**
```java
setAccessible(true)
Class.forName(className).newInstance()
```

**Detection Method:** Pattern recognition for dangerous APIs

### SQL

**Critical Severity:**
```sql
DELETE FROM table WHERE 1=1
DROP TABLE users
GRANT ALL PRIVILEGES
```

**High Severity:**
```sql
-- Contains password
admin/password123
```

**Detection Method:** Keyword and pattern analysis

## Secrets Detection

### API Keys

**AWS:**
- Access Key: `AKIA[0-9A-Z]{16}`
- Secret Key: 40 characters base64

**GitHub:**
- Personal Access Token: `ghp_[a-zA-Z0-9]{36}`
- OAuth Token: `gho_[a-zA-Z0-9]{36}`

**OpenAI:**
- API Key: `sk-[a-zA-Z0-9]{48}`

**Google:**
- API Key: `AIza[0-9A-Za-z\-_]{35}`

**Slack:**
- Token: `xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[a-zA-Z0-9]{24,32}`

**SendGrid:**
- API Key: `SG\.[a-zA-Z0-9]{22}\.[a-zA-Z0-9]{43}`

### Private Keys

**Patterns:**
```
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN EC PRIVATE KEY-----
-----BEGIN DSA PRIVATE KEY-----
-----BEGIN PRIVATE KEY-----
```

**Detection:** Exact string matching with context validation

### Credentials

**Patterns:**
- `password = "hardcoded123"`
- `api_key = "1234567890abcdef"`
- `secret = "my_secret_token"`
- Connection strings with embedded passwords

**Detection:** Regex with length and context validation

## Cross-Site Scripting (XSS)

### Reflected XSS

**HTML:**
```html
<script>user_input</script>
<img src=x onerror="user_code">
<a href="javascript:user_input">
```

**JavaScript:**
```javascript
element.innerHTML = userInput
document.write(userContent)
eval("code" + userInput)
```

### Stored XSS

**Detection:** Database writes without sanitization
**Patterns:** Unsafe storage of user input before display

### DOM-Based XSS

**Patterns:**
```javascript
location.href = userInput
window.location = untrustedURL
document.cookie = userInput
```

## Path Traversal

**Patterns:**
- `../` sequences in file paths
- `..%2F` URL encoded traversal
- Absolute paths from user input
- `open()` with unvalidated paths

**Languages:** All file-handling languages
**Severity:** High

## XML External Entity (XXE)

**Patterns:**
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
```

**Python:**
```python
xml.etree.ElementTree.parse(untrusted)
lxml.etree.parse(user_xml)
```

**Java:**
```java
DocumentBuilder.parse(userXML)
SAXParser.parse(input)
```

**Detection:** XML parsing without disabling external entities

## Insecure Deserialization

**Python:**
```python
pickle.loads(data)
yaml.load(content)  # without Loader=SafeLoader
```

**PHP:**
```php
unserialize($data)
```

**Java:**
```java
ObjectInputStream.readObject()
```

**Severity:** Critical - Can lead to Remote Code Execution

## False Positive Mitigation

### Context Analysis
- Check if input is validated before use
- Verify sanitization functions are applied
- Consider parameterized queries vs raw concatenation

### Confidence Levels
- **High:** Clear vulnerability with no mitigation
- **Medium:** Potential issue requiring manual review
- **Low:** Suspicious pattern needing context

### Suppression
Users can add inline comments to suppress false positives:
```python
pickle.loads(data)  # nosec - data from trusted internal source
```

## Severity Classification

**Critical:**
- Remote Code Execution
- SQL Injection in authentication
- Hardcoded admin credentials
- Private key exposure

**High:**
- SQL Injection in non-critical areas
- XSS vulnerabilities
- Command injection
- SSRF
- Insecure deserialization

**Medium:**
- Path traversal
- Missing input validation
- Weak cryptography
- Information disclosure

**Low:**
- Code quality issues
- Deprecated function usage
- Minor configuration issues

## Pattern Updates

Security patterns are continuously updated based on:
- CVE database analysis
- Security research publications
- Community feedback
- New attack vectors

See [CONTRIBUTING.md](../CONTRIBUTING.md) to propose new patterns.

## References

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)
- [NIST Vulnerability Database](https://nvd.nist.gov/)
