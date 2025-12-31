# 🫀 CodePulse - Deep Code Intelligence Engine

> Beyond surface-level analysis - Understanding code at a fundamental level

**By Saleh Almqati** | IT Student | Python 3.9+ | MIT License

[![GitHub](https://img.shields.io/badge/GitHub-DeftonesL-black?logo=github)](https://github.com/DeftonesL)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Saleh%20Almqati-blue?logo=linkedin)](https://linkedin.com/in/Saleh-almqati)
[![Twitter](https://img.shields.io/badge/Twitter-@Remindedwithyou-1DA1F2?logo=twitter)](https://twitter.com/Remindedwithyou)

---

## 🎯 What Makes CodePulse Different?

CodePulse doesn't just count lines or run simple checks. It **understands your code** using:

### 🧠 Graph-Based Analysis
- **Control Flow Graphs (CFG)** - Maps every execution path
- **Data Flow Analysis (DFA)** - Tracks how data moves through variables  
- **Call Graphs** - Shows function dependency chains
- **Dependency Networks** - Identifies coupling and cohesion issues

### 🔬 Deep Algorithms
Custom algorithms developed specifically for CodePulse:
- Rolling hash for clone detection
- AST structural comparison
- Behavioral fingerprinting
- Context-aware pattern matching
- Custom complexity formulas

### 🎓 Research-Based
Implements academic research in software engineering:
- SQALE methodology for technical debt
- Halstead complexity metrics
- Information flow theory
- Graph theory for dependency analysis

---

## 🚀 Core Features

### 1. 🧬 Deep Code Intelligence (`deep_analysis.py`)

**What it does**: Builds complete graphs of your code structure

**Analyzes:**
- Control flow through your program
- Data dependencies between variables
- Function call relationships
- Unreachable code detection
- Infinite loop detection
- Complex branching patterns

**Example Output:**
```
Control Flow Analysis:
  • Total execution paths: 247
  • Branch points: 45
  • Unreachable blocks: 2 ⚠️
  • Potential infinite loops: 1 🔴
  • Cyclomatic complexity: 68

Data Flow Analysis:
  • Variables tracked: 89
  • Data dependencies: 156
  • Undefined variables: 0 ✅
  • Unused variables: 7 ⚠️
```

### 2. 🔍 Clone Detection Engine (`clone_detection.py`)

**What it does**: Finds duplicated code using 4 different algorithms

**Clone Types:**
- **Type 1**: Exact copies (except for whitespace)
- **Type 2**: Renamed variables (same structure)
- **Type 3**: Modified statements (similar code)
- **Type 4**: Semantic clones (same functionality, different code)

**Algorithms:**
- Rolling hash for exact matching (O(n) complexity)
- AST structural comparison for renamed clones
- Behavioral fingerprinting for semantic clones
- Fuzzy sequence matching

**Example Output:**
```
Clone Detection Report:
  📊 Total clones found: 12
  📏 Duplicated lines: 347
  
  By Type:
    • Type 1 (Exact): 5 clones
    • Type 2 (Renamed): 4 clones
    • Type 4 (Semantic): 3 clones
  
  Severity:
    • HIGH: 3 (> 50 lines duplicated)
    • MEDIUM: 9
```

### 3. 👃 Intelligent Smell Detector (`smell_detector.py`)

**What it does**: Context-aware code smell detection with refactoring suggestions

**Categories:**
- **Bloaters**: Long methods, large classes, long parameters
- **OO Abusers**: Inappropriate intimacy, feature envy
- **Change Preventers**: Divergent change, shotgun surgery
- **Dispensables**: Dead code, lazy classes
- **Couplers**: Message chains, middle man

**Special Features:**
- Each smell includes **specific refactoring suggestion**
- **Code examples** showing before/after
- **Impact analysis** explaining why it matters
- **Severity scoring** to prioritize fixes

**Example Output:**
```
[HIGH] Long Method (Line 45)
  Method 'processData' is 127 lines
  
  Impact: Difficult to understand and maintain. 
  Higher bug probability.
  
  Refactoring:
  Extract smaller methods:
    • validateInput() - lines 45-68
    • transformData() - lines 69-102
    • saveResults() - lines 103-127
  
  Code Example:
  # Before: 127 lines
  def processData(data):
      # validation
      # transformation
      # saving
  
  # After: 3 focused functions
  def processData(data):
      validateInput(data)
      result = transformData(data)
      saveResults(result)
```

### 4. 📊 Advanced Metrics Calculator

**Custom Metrics:**
- **Structural Complexity Index (SCI)** - My own formula
- **Information Flow Complexity** - Data movement analysis
- **Graph Complexity** - Based on CFG structure
- **Combined Complexity Score** - Weighted formula

**Standard Metrics:**
- Halstead (Volume, Difficulty, Effort, Bugs)
- Maintainability Index (0-100)
- Technical Debt (hours)
- Cyclomatic & Cognitive Complexity

### 5. 🎯 Pattern Detection

**Design Patterns:**
- Singleton
- Factory
- Builder
- Observer (coming soon)

**Anti-Patterns:**
- God Class
- Spaghetti Code
- Lava Flow
- Golden Hammer

### 6. ⚡ Performance Analysis

**Detects:**
- O(n²), O(n³) nested loops
- Memory leaks
- Inefficient operations
- String concatenation in loops
- Repeated function calls

### 7. 🔒 Security Scanning

**Finds:**
- SQL Injection vulnerabilities
- XSS risks
- Hardcoded secrets
- Code injection points
- Insecure cryptography

---

## 📊 Analysis Depth Comparison

| Feature | Simple Tools | CodePulse |
|---------|-------------|-----------|
| Line counting | ✅ | ✅ |
| Basic patterns | ✅ | ✅ |
| AST parsing | ❌ | ✅ |
| Control flow graphs | ❌ | ✅ |
| Data flow analysis | ❌ | ✅ |
| Clone detection (4 types) | ❌ | ✅ |
| Context-aware smells | ❌ | ✅ |
| Refactoring suggestions | ❌ | ✅ |
| Technical debt (hours) | ❌ | ✅ |
| Dependency graphs | ❌ | ✅ |
| Semantic analysis | ❌ | ✅ |

---

## 🎮 Quick Start

### Installation
```bash
git clone https://github.com/DeftonesL/CodePulse.git
cd CodePulse
pip install -e .
```

### Basic Usage
```bash
# Deep analysis
python3 src/core/deep_analysis.py yourfile.py

# Clone detection
python3 src/core/clone_detection.py yourfile.py

# Smell detection
python3 src/core/smell_detector.py yourfile.py

# Complete analysis (all features)
python3 src/core/analyzer.py ./your-project
```

---

## 💻 Example Output

```
════════════════════════════════════════════════════════════════
🫀 CODEPULSE - DEEP CODE INTELLIGENCE REPORT
════════════════════════════════════════════════════════════════

PROJECT: MyApp
FILES ANALYZED: 42
LINES OF CODE: 5,234

OVERALL HEALTH: 82.5/100 (B+)

════════════════════════════════════════════════════════════════
📊 DEEP ANALYSIS
════════════════════════════════════════════════════════════════

Control Flow:
  ✓ Execution paths: 1,247
  ✓ Branch points: 312
  ⚠ Unreachable code: 3 blocks
  ⚠ Infinite loops: 1 detected

Data Flow:
  ✓ Variables: 456
  ✓ Dependencies: 892
  ⚠ Unused variables: 23

Call Graph:
  ✓ Functions: 187
  ✓ Max depth: 7 levels
  ⚠ Circular dependencies: 2

════════════════════════════════════════════════════════════════
🔍 CLONE DETECTION
════════════════════════════════════════════════════════════════

Total Clones: 15
Duplicated Lines: 487 (9.3%)

By Type:
  • Type 1 (Exact): 6 clones
  • Type 2 (Renamed): 5 clones  
  • Type 4 (Semantic): 4 clones

Top Clone:
  📄 database.py:45-98 ↔ cache.py:120-173
  📏 54 lines duplicated
  💡 Extract to shared utility module

════════════════════════════════════════════════════════════════
👃 CODE SMELLS
════════════════════════════════════════════════════════════════

Health Score: 78/100

Detected: 18 smells
  🔴 HIGH: 3
  🟡 MEDIUM: 8
  🟢 LOW: 7

Critical Issues:
  1. [HIGH] Long Method - processUserData() (156 lines)
     💡 Extract to 4 smaller methods
  
  2. [HIGH] God Class - UserManager (847 lines, 34 methods)
     💡 Split into UserRepository, UserValidator, UserService
  
  3. [HIGH] Feature Envy - calculateDiscount() 
     💡 Move to Product class

════════════════════════════════════════════════════════════════
📈 ADVANCED METRICS
════════════════════════════════════════════════════════════════

Halstead Metrics:
  • Volume: 45,678
  • Difficulty: 28.3
  • Effort: 1,292,447
  • Estimated Bugs: 15.2

Maintainability:
  • Index: 78.5/100 (B - Moderately Maintainable)
  • Comment Ratio: 12.3%
  • Test Coverage: ~65%

Technical Debt:
  • Total: 23.7 hours
  • Critical: 8.2 hours
  • Medium: 12.5 hours
  • Low: 3.0 hours

════════════════════════════════════════════════════════════════
🎯 PRIORITY RECOMMENDATIONS
════════════════════════════════════════════════════════════════

1. ⚡ URGENT: Fix infinite loop in scheduler.py:234
2. 🔴 HIGH: Refactor UserManager class (violates SRP)
3. 🟡 MEDIUM: Remove 487 lines of duplicated code
4. 🟢 LOW: Add docstrings to 23 functions

Estimated Impact:
  • Reduce bugs by ~40%
  • Improve maintainability by 15 points
  • Reduce technical debt by 12 hours
```

---

## 🏗️ Architecture

```
CodePulse/
├── src/core/
│   ├── deep_analysis.py      # Graph-based analysis ⭐
│   ├── clone_detection.py    # 4-type clone detection ⭐
│   ├── smell_detector.py     # Intelligent smells ⭐
│   ├── advanced_metrics.py   # Halstead, MI, TD
│   ├── code_patterns.py      # Pattern detection
│   ├── performance_analyzer.py
│   └── scanner.py            # AST parsing
│
├── src/modules/
│   └── security.py           # Security scanning
│
└── docs/
    └── ADVANCED_FEATURES.md  # Detailed docs
```

---

## 🔬 Technical Details

### Algorithms Implemented

1. **Control Flow Graph Construction**
   - Recursive AST traversal
   - Edge creation for branches/loops
   - Cycle detection using DFS

2. **Clone Detection**
   - Rolling hash (Rabin-Karp algorithm)
   - AST structural hashing
   - Sequence alignment (Smith-Waterman inspired)

3. **Data Flow Analysis**
   - Reaching definitions
   - Use-def chains
   - Live variable analysis

4. **Smell Detection**
   - Pattern matching with context
   - Threshold-based scoring
   - Category classification

### Dependencies

- `networkx` - Graph algorithms
- `ast` (built-in) - AST parsing
- `difflib` (built-in) - Sequence matching
- No external AI APIs - all algorithms are custom!

---

## 📚 Documentation

- **[ADVANCED_FEATURES.md](docs/ADVANCED_FEATURES.md)** - Detailed feature guide
- **[REPORTS_MANAGEMENT.md](docs/REPORTS_MANAGEMENT.md)** - Managing analysis reports
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

---

## 🎓 About the Developer

I'm **Saleh Almqati**, an IT student who built CodePulse to:
- Understand how professional code analysis tools work
- Learn graph theory and algorithms
- Practice software engineering principles
- Create something useful for the community

**This isn't just a wrapper around existing tools** - every algorithm is custom-built and thoroughly tested.

### Connect with Me:
- 📧 Email: xsll7c@gmail.com
- 💼 LinkedIn: [Saleh-almqati](https://linkedin.com/in/Saleh-almqati)
- 🐙 GitHub: [DeftonesL](https://github.com/DeftonesL)
- 🐦 Twitter: [@Remindedwithyou](https://twitter.com/Remindedwithyou)

---

## ⭐ Support the Project

If CodePulse helped you:
- ⭐ Star the repository
- 🔄 Share with colleagues
- 💬 Give feedback
- 🐛 Report bugs
- 🤝 Contribute improvements

---

## 📊 Project Stats

- 📝 **10,000+ lines of code**
- 🧪 **Custom algorithms** (not wrappers)
- 🔬 **8 analysis engines**
- 📊 **4 clone detection types**
- 🎯 **5 smell categories**
- 📈 **10+ metrics**

---

## 🛠️ Advanced Usage

### Analyze Specific Modules

```bash
# Deep analysis only
python3 src/core/deep_analysis.py src/mymodule.py

# Clone detection only  
python3 src/core/clone_detection.py src/

# Smell detection only
python3 src/core/smell_detector.py src/
```

### Integrate in CI/CD

```yaml
# .github/workflows/code-quality.yml
- name: CodePulse Analysis
  run: |
    python3 src/core/analyzer.py .
    if [ $? -ne 0 ]; then
      echo "Code quality check failed"
      exit 1
    fi
```

### Custom Thresholds

```python
from src.core.smell_detector import IntelligentSmellDetector

detector = IntelligentSmellDetector()
detector.max_method_length = 30  # Custom threshold
smells = detector.detect_smells('myfile.py')
```

---

## 🔮 Roadmap

- [ ] Machine learning for pattern recognition
- [ ] Cross-file clone detection
- [ ] Automated refactoring suggestions
- [ ] HTML report generation with graphs
- [ ] VS Code extension
- [ ] Support for more languages (Java, C++, Go)
- [ ] Real-time analysis

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file

---

**Built with ❤️ and deep understanding of software engineering principles**

*Healthy code, happy developers* 🫀
