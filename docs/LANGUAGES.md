# Supported Languages

CodePulse provides comprehensive support for 50+ programming languages and file formats.

## Programming Languages

### Systems Programming

**C/C++**
- Extensions: `.c`, `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`, `.hxx`
- Detection: Buffer overflows, memory leaks, unsafe functions
- Patterns: `strcpy`, `sprintf`, pointer arithmetic issues

**Rust**
- Extensions: `.rs`
- Detection: Unsafe blocks, unwrap without handling, memory safety
- Patterns: `unsafe {}`, `.unwrap()`, `.expect()`

**Go**
- Extensions: `.go`
- Detection: Error handling, goroutine leaks, SQL injection
- Patterns: `exec.Command()`, ignored errors, unsafe SQL queries

### JVM Languages

**Java**
- Extensions: `.java`
- Detection: SQL injection, XXE, deserialization, command injection
- Patterns: `Runtime.exec()`, `ProcessBuilder`, reflection issues

**Kotlin**
- Extensions: `.kt`, `.kts`
- Detection: Similar to Java with Kotlin-specific patterns
- Patterns: Unsafe casts, null pointer risks

**Scala**
- Extensions: `.scala`
- Detection: Type safety issues, unsafe operations
- Patterns: Pattern matching vulnerabilities

**Groovy**
- Extensions: `.groovy`
- Detection: Code injection, unsafe evaluation
- Patterns: `evaluate()`, dynamic code execution

### .NET Languages

**C#**
- Extensions: `.cs`
- Detection: SQL injection, XSS, deserialization
- Patterns: String concatenation in queries, unsafe XML parsing

**F#**
- Extensions: `.fs`, `.fsx`
- Detection: Type safety issues, unsafe operations
- Patterns: Mutable state issues

**VB.NET**
- Extensions: `.vb`
- Detection: Similar to C# patterns
- Patterns: SQL string building, unsafe input handling

### Web Backend

**Python**
- Extensions: `.py`, `.pyw`, `.pyx`
- Detection: SQL injection, command injection, XSS, deserialization
- Patterns: String formatting in SQL, `eval()`, `exec()`, pickle usage
- Analysis: AST-based deep analysis

**JavaScript**
- Extensions: `.js`, `.mjs`, `.cjs`
- Detection: XSS, prototype pollution, code injection
- Patterns: `eval()`, `innerHTML`, `document.write()`, dangerous functions

**TypeScript**
- Extensions: `.ts`
- Detection: Type bypass, unsafe operations, XSS
- Patterns: Type assertions, `any` usage in sensitive contexts

**PHP**
- Extensions: `.php`, `.phtml`
- Detection: SQL injection, file inclusion, command execution
- Patterns: `eval()`, `exec()`, `system()`, `include()` with variables

**Ruby**
- Extensions: `.rb`, `.rake`
- Detection: Command injection, SQL injection, YAML deserialization
- Patterns: `eval()`, `system()`, backtick commands, unsafe YAML

**Perl**
- Extensions: `.pl`, `.pm`
- Detection: Code injection, SQL issues
- Patterns: `eval`, unsafe regular expressions

### Web Frontend

**HTML**
- Extensions: `.html`, `.htm`, `.xhtml`
- Detection: XSS vectors, inline scripts, insecure resources
- Patterns: Inline event handlers, `javascript:` protocol, HTTP resources

**CSS**
- Extensions: `.css`, `.scss`, `.sass`, `.less`
- Detection: CSS injection, data exfiltration
- Patterns: `url()` with user input, `@import` issues

**Vue**
- Extensions: `.vue`
- Detection: XSS in templates, unsafe v-html
- Patterns: Dynamic template rendering, unsafe bindings

**Svelte**
- Extensions: `.svelte`
- Detection: XSS, unsafe HTML rendering
- Patterns: `@html` directive misuse

**React**
- Extensions: `.jsx`, `.tsx`
- Detection: XSS, dangerouslySetInnerHTML usage
- Patterns: Unsafe props, innerHTML assignments

### Mobile Development

**Swift**
- Extensions: `.swift`
- Detection: Memory safety, data exposure, insecure storage
- Patterns: Unsafe pointer usage, keychain issues

**Objective-C**
- Extensions: `.m`, `.mm`
- Detection: Memory management, buffer overflows
- Patterns: Manual memory management issues

**Dart**
- Extensions: `.dart`
- Detection: Type safety, insecure communication
- Patterns: Dynamic type usage, HTTP connections

### Functional Languages

**Haskell**
- Extensions: `.hs`
- Detection: Unsafe operations, partial functions
- Patterns: `undefined`, `error`, unsafe IO

**Erlang**
- Extensions: `.erl`
- Detection: Process management, message passing issues
- Patterns: Unhandled messages, atom exhaustion

**Elixir**
- Extensions: `.ex`, `.exs`
- Detection: Similar to Erlang with Elixir patterns
- Patterns: Unsafe code evaluation

### Data and Configuration

**SQL**
- Extensions: `.sql`
- Detection: Dangerous queries, permission issues, hardcoded credentials
- Patterns: `DROP TABLE`, `DELETE` without WHERE, password comments

**JSON**
- Extensions: `.json`
- Detection: Sensitive data exposure, hardcoded secrets
- Patterns: Keys containing "password", "secret", "api_key", "token"

**YAML**
- Extensions: `.yml`, `.yaml`
- Detection: Deserialization issues, sensitive data
- Patterns: Unsafe tags, credential exposure

**XML**
- Extensions: `.xml`
- Detection: XXE vulnerabilities, entity expansion
- Patterns: External entity declarations, DOCTYPE

**TOML**
- Extensions: `.toml`
- Detection: Configuration issues, secret exposure
- Patterns: Credentials in configuration

### Shell Scripts

**Bash**
- Extensions: `.sh`, `.bash`, `.zsh`
- Detection: Command injection, unsafe variable expansion
- Patterns: Unquoted variables, `eval` usage

**PowerShell**
- Extensions: `.ps1`, `.psm1`
- Detection: Command execution, script injection
- Patterns: `Invoke-Expression`, unvalidated input

**Batch**
- Extensions: `.bat`, `.cmd`
- Detection: Command injection, unsafe paths
- Patterns: Unescaped special characters

### Other Languages

**Lua**
- Extensions: `.lua`
- Detection: Code injection, unsafe loading
- Patterns: `loadstring`, `dofile` with user input

**R**
- Extensions: `.r`, `.R`
- Detection: Code execution, unsafe evaluation
- Patterns: `eval()`, `parse()` with untrusted data

**Julia**
- Extensions: `.jl`
- Detection: Code injection, unsafe macros
- Patterns: `eval()`, unsafe macro expansion

## Detection Capabilities by Language

### High Confidence Detection
Languages with AST-based or comprehensive pattern analysis:
- Python (AST analysis)
- JavaScript/TypeScript
- HTML
- SQL
- JSON

### Medium Confidence Detection
Languages with pattern-based detection:
- Java, C#, PHP, Ruby, Go
- Shell scripts
- Configuration files

### Basic Detection
All languages include:
- Hardcoded secrets detection
- API key and token detection
- Password exposure
- Private key detection

## Universal Patterns

These patterns are checked across all file types:

**API Keys and Tokens**
- AWS Access Keys: `AKIA[0-9A-Z]{16}`
- GitHub Tokens: `ghp_[a-zA-Z0-9]{36}`
- OpenAI Keys: `sk-[a-zA-Z0-9]{48}`
- Google API Keys: `AIza[0-9A-Za-z\\-_]{35}`

**Private Keys**
- RSA, EC, DSA private keys
- PEM format detection
- Certificate files

**Credentials**
- Hardcoded passwords (8+ characters)
- Connection strings with passwords
- Authentication tokens

## Adding New Language Support

To request support for a new language:

1. Open an issue describing the language
2. Provide common vulnerability patterns
3. Include sample vulnerable code
4. Reference security documentation

See [CONTRIBUTING.md](../CONTRIBUTING.md) for implementation details.

## Language Priority

Language support is prioritized based on:
- Community usage and demand
- Security vulnerability prevalence
- Available security research and patterns
- Maintenance complexity

## Detection Accuracy

Accuracy varies by language and pattern complexity:
- **High**: Python, JavaScript, SQL, HTML
- **Medium**: Java, C#, PHP, Ruby
- **Improving**: Newer languages with evolving best practices

False positive rates are actively minimized through context-aware pattern matching.
