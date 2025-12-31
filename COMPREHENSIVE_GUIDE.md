# 🫀 CodePulse - دليل الاستخدام الشامل

## 🌍 اللغات المدعومة

### لغات البرمجة (تحليل أمني كامل):
```
✅ Python         (.py)
✅ JavaScript     (.js, .jsx)
✅ TypeScript     (.ts, .tsx)
✅ PHP            (.php)
✅ Java           (.java)
✅ C#             (.cs)
✅ Go             (.go)
✅ Ruby           (.rb)
✅ Rust           (.rs)
✅ Kotlin         (.kt)
```

### ملفات الويب والبيانات:
```
✅ HTML           (.html, .htm)
✅ JSON           (.json)
✅ SQL            (.sql)
```

---

## 🚀 الاستخدام السريع

### 1. فحص ملف واحد

```bash
# Python
python comprehensive_scan.py app.py

# JavaScript
python comprehensive_scan.py script.js

# PHP
python comprehensive_scan.py index.php

# HTML
python comprehensive_scan.py index.html

# أي لغة مدعومة
python comprehensive_scan.py any_file.{py,js,php,java,cs,go...}
```

### 2. فحص مشروع كامل

```bash
# فحص شامل لكل الملفات المدعومة
python comprehensive_scan.py ./my_project

# أمثلة:
python comprehensive_scan.py C:\Users\xsll7\Desktop\discord
python comprehensive_scan.py /var/www/html
python comprehensive_scan.py ~/projects/webapp
```

---

## 📊 مثال على النتيجة

```
======================================================================
🫀 CODEPULSE - PROJECT SCAN
======================================================================

Directory: C:\Projects\MyApp
Started: 2025-12-31 15:30:00

Found 156 files:

  🐍 Python      :  45
  💛 JavaScript  :  38
  🐘 PHP         :  22
  🌐 HTML        :  15
  📄 JSON        :  12
  ☕ Java        :  10
  💾 SQL         :   8
  💙 TypeScript  :   6

🐍 Analyzing Python files...
  [1/45] app.py                                    ✓
  [2/45] models.py                                 ✓
  [3/45] views.py                                  ✓
  ...

💻 Analyzing code files...
  [1/76] [JS  ] main.js                            ✓
  [2/76] [PHP ] index.php                          ✓
  [3/76] [Java] Controller.java                    ✓
  ...

📄 Analyzing web & data files...
  [1/35] [html] index.html                         ✓
  [2/35] [json] config.json                        ⚠
  [3/35] [sql ] schema.sql                         ✓
  ...

======================================================================
📊 PROJECT SUMMARY
======================================================================

🟡 Project Score: 68.5/100 (C+)
📁 Files: 156/156

──────────────────────────────────────────────────────────────────────
🎯 TOTAL ISSUES ACROSS PROJECT
──────────────────────────────────────────────────────────────────────
🔒 Security    :   89  ← كل اللغات
👃 Smells      :   45  ← Python فقط
🔍 Clones      :   12  ← Python فقط
⚡ Performance :   23  ← Python فقط

──────────────────────────────────────────────────────────────────────
⚠️  FILES NEEDING ATTENTION
──────────────────────────────────────────────────────────────────────
1. 🔴 config.json                    25.0/100  ← أسرار مكشوفة
2. 🔴 auth.php                       35.0/100  ← SQL injection
3. 🔴 login.js                       42.0/100  ← XSS + eval()
4. 🔴 database.sql                   48.0/100  ← Plain passwords
5. 🟡 AdminController.java           65.0/100  ← Command injection

💾 Detailed report: project_report_20251231_153000.json
======================================================================
```

---

## 🔍 الثغرات المكتشفة حسب اللغة

### Python
```
🔴 SQL Injection (string concatenation)
🔴 Command Injection (os.system, subprocess.call)
🔴 Hardcoded Secrets
🔴 eval() usage
🔴 Insecure Deserialization (pickle)
🟠 Path Traversal
🟡 Performance Issues (O(n²) loops)
```

### JavaScript/TypeScript
```
🔴 XSS (innerHTML, document.write)
🔴 eval() / Function()
🔴 Code Injection (setTimeout/setInterval with strings)
🟠 DOM-based XSS
🟠 Password in localStorage
🟡 console.log in production
```

### PHP
```
🔴 Remote Code Execution (eval, exec, system)
🔴 SQL Injection (mysql_query with variables)
🔴 File Inclusion (include/require with $_GET)
🔴 Command Injection (shell_exec)
🔴 Insecure Deserialization (unserialize)
🟠 XSS (echo without escaping)
```

### Java
```
🔴 Command Injection (Runtime.exec)
🔴 SQL Injection (Statement.executeQuery)
🔴 Insecure Deserialization (ObjectInputStream)
🟠 Reflection abuse (setAccessible)
🟡 Hardcoded credentials
```

### C#
```
🔴 SQL Injection (SqlCommand concatenation)
🔴 Insecure Deserialization (BinaryFormatter)
🔴 Command Injection (Process.Start)
🟠 XSS in ASP.NET
```

### Go
```
🔴 Command Injection (exec.Command)
🔴 SQL Injection (db.Exec with concatenation)
🟠 Unsafe HTML rendering
🟡 Race conditions
```

### HTML
```
🔴 XSS vulnerabilities
🔴 Missing CSRF tokens
🟠 Missing CSP headers
🟠 Unsafe iframes
🟡 HTTP resources (not HTTPS)
🟡 Missing SRI on CDN
```

### JSON
```
🔴 AWS Keys (AKIA...)
🔴 API Keys
🔴 Hardcoded passwords
🟠 Sensitive data exposure
```

### SQL
```
🔴 Plain text passwords
🔴 DROP DATABASE
🔴 Dynamic SQL (EXEC IMMEDIATE)
🟠 GRANT ALL
🟠 Public access
🟡 SELECT *
```

---

## 🎯 حالات الاستخدام

### 1. مشروع ويب (PHP + JS + HTML + SQL)

```bash
python comprehensive_scan.py ./webapp

# سيفحص:
✓ ملفات PHP للـ SQL injection و RCE
✓ JavaScript للـ XSS و eval()
✓ HTML للـ CSRF و CSP
✓ SQL للـ injection patterns
✓ JSON للـ secrets
```

### 2. تطبيق Spring Boot (Java)

```bash
python comprehensive_scan.py ./spring-app

# سيفحص:
✓ Java files للـ injection
✓ XML configs
✓ Properties files
```

### 3. مشروع React (JS/TS)

```bash
python comprehensive_scan.py ./react-app

# سيفحص:
✓ JSX/TSX للـ XSS
✓ API calls للـ SSRF
✓ State management
```

### 4. API بـ Go

```bash
python comprehensive_scan.py ./go-api

# سيفحص:
✓ Go files للـ injection
✓ SQL queries
✓ Command execution
```

---

## 📝 التقارير المفصلة

### تقرير JSON

```json
{
  "total_files": 156,
  "files_scanned": 156,
  "file_types": {
    "Python": 45,
    "JavaScript": 38,
    "PHP": 22,
    ...
  },
  "total_issues": {
    "security": 89,
    "smells": 45,
    "clones": 12,
    "performance": 23
  },
  "project_score": 68.5,
  "files": {
    "app.py": {
      "overall_score": 75.0,
      "security": {...},
      "smells": {...},
      ...
    },
    "auth.php": {
      "language": "PHP",
      "score": 35.0,
      "issues": [
        {
          "type": "SQL Injection",
          "severity": "CRITICAL",
          "line": 45,
          "recommendation": "Use prepared statements"
        }
      ]
    }
  }
}
```

---

## ⚙️ التكوين المتقدم

### تخصيص الفحص

```python
# custom_scan.py
from comprehensive_scan import ComprehensiveScanner

scanner = ComprehensiveScanner()

# فحص ملف معين
result = scanner.scan_file('app.py')

# فحص مجلد
result = scanner.scan_directory('./project')

# طباعة الملخص
scanner.print_summary()
```

### تصفية حسب الشدة

```python
# إظهار CRITICAL و HIGH فقط
critical_issues = [
    issue for issue in result['security']['issues']
    if issue['severity'] in ['CRITICAL', 'HIGH']
]
```

---

## 🔧 حل المشاكل

### 1. الملفات الكبيرة

```bash
# تخطي الملفات الكبيرة جداً
find . -name "*.py" -size -1M -exec python comprehensive_scan.py {} \;
```

### 2. مشاريع متعددة اللغات

```bash
# سيفحص كل اللغات تلقائياً
python comprehensive_scan.py ./polyglot-project
```

### 3. False Positives

```python
# أضف استثناءات في الكود
# في advanced_language_scanner.py:

if 'example' in line.lower() or 'test' in file_path:
    continue  # تخطي ملفات الاختبار
```

---

## 📚 أمثلة متقدمة

### 1. فحص مع CI/CD

```yaml
# .github/workflows/security.yml
- name: CodePulse Security Scan
  run: |
    python comprehensive_scan.py .
    if [ $(jq '.project_score' project_report_*.json) -lt 70 ]; then
      echo "Security score too low!"
      exit 1
    fi
```

### 2. تقرير HTML

```python
# generate_html_report.py
import json

with open('project_report.json') as f:
    data = json.load(f)

html = f"""
<h1>Security Report</h1>
<p>Score: {data['project_score']}/100</p>
<p>Issues: {data['total_issues']['security']}</p>
"""

with open('report.html', 'w') as f:
    f.write(html)
```

### 3. دمج مع Slack

```python
import requests
import json

with open('project_report.json') as f:
    data = json.load(f)

if data['total_issues']['security'] > 10:
    requests.post(SLACK_WEBHOOK, json={
        'text': f"⚠️ Security Alert: {data['total_issues']['security']} issues found!"
    })
```

---

## 🎓 نصائح للحصول على أفضل النتائج

### 1. تنظيم الكود
```
✅ استخدم .gitignore لاستبعاد المجلدات
✅ نظف المشروع قبل الفحص
✅ احذف الملفات المؤقتة
```

### 2. الأولويات
```
1. CRITICAL security issues
2. HIGH security issues  
3. Code smells
4. Performance issues
```

### 3. التحسين المستمر
```
✅ افحص بعد كل commit كبير
✅ راقب التقدم عبر الزمن
✅ استهدف score > 80
```

---

## 🚀 الخلاصة

CodePulse يفحص **13 لغة برمجة** و**156 نوع ثغرة** في مشروعك بأمر واحد:

```bash
python comprehensive_scan.py ./your_project
```

**بسيط. شامل. احترافي.** 🎯
