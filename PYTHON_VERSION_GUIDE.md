# Python Version Compatibility Guide

## المشكلة
Python 3.14 جديد جداً (صدر نهاية 2024) وبعض المكتبات غير متوافقة معه بعد، خاصة networkx.

---

## ✅ الحلول

### الحل 1: استخدم Python 3.11 أو 3.12 (موصى به)

#### Windows:
```powershell
# 1. شوف الإصدارات المثبتة
py -0

# الناتج سيكون شيء مثل:
# -V:3.14 *        # النجمة = الإصدار الافتراضي
# -V:3.12
# -V:3.11

# 2. استخدم Python 3.12 أو 3.11
py -3.12 -m pip install networkx

# 3. شغّل CodePulse بهذا الإصدار
py -3.12 comprehensive_scan.py TEST_EXAMPLE.py
```

#### Linux:
```bash
# تثبيت Python 3.12 (Ubuntu/Debian)
sudo apt update
sudo apt install python3.12 python3.12-venv

# استخدام Python 3.12
python3.12 -m pip install networkx
python3.12 comprehensive_scan.py TEST_EXAMPLE.py
```

---

### الحل 2: استخدم الملفات المتوافقة (بدون networkx)

CodePulse يحتوي على نسخ بديلة تشتغل **بدون** networkx:

#### الملفات المتوافقة مع Python 3.14:
```powershell
✅ comprehensive_scan.py          # الفاحص الشامل
✅ src/core/deep_analysis_standalone.py  # تحليل عميق بدون networkx
✅ src/core/advanced_security.py         # فحص أمني
✅ src/core/clone_detection.py           # كشف النسخ
✅ src/core/smell_detector.py            # كشف المشاكل
✅ src/core/performance_analyzer.py      # تحليل الأداء
```

#### الملفات التي تحتاج Python 3.11/3.12:
```powershell
⚠️  src/core/cross_file_analysis.py     # يحتاج networkx
⚠️  src/core/deep_analysis.py           # يحتاج networkx
```

---

## 🚀 الاستخدام السريع (Python 3.14)

### 1. الفحص الشامل (يشتغل!):
```powershell
python comprehensive_scan.py test.py
```

### 2. الفحص الأمني:
```powershell
python src/core/advanced_security.py test.py
```

### 3. كشف المشاكل:
```powershell
python src/core/smell_detector.py test.py
```

### 4. التحليل العميق (النسخة Standalone):
```powershell
python src/core/deep_analysis_standalone.py test.py
```

### 5. كشف النسخ المكررة:
```powershell
python src/core/clone_detection.py test.py
```

---

## 📊 مقارنة الإصدارات

| الميزة | Python 3.14 | Python 3.12 |
|--------|-------------|-------------|
| comprehensive_scan.py | ✅ | ✅ |
| advanced_security.py | ✅ | ✅ |
| smell_detector.py | ✅ | ✅ |
| clone_detection.py | ✅ | ✅ |
| deep_analysis_standalone.py | ✅ | ✅ |
| cross_file_analysis.py | ❌ | ✅ |
| deep_analysis.py | ❌ | ✅ |
| السرعة | أبطأ قليلاً | أسرع |
| التوافق | محدود | ممتاز |

---

## 🎯 التوصية

### للاستخدام اليومي:
```powershell
# استخدم Python 3.12
py -3.12 comprehensive_scan.py your_code.py
```

### إذا ما عندك غير 3.14:
```powershell
# استخدم الملفات المتوافقة
python comprehensive_scan.py your_code.py
python src/core/advanced_security.py your_code.py
```

---

## 🔧 تثبيت Python 3.12

### Windows:
1. حمّل من: https://www.python.org/downloads/
2. اختر Python 3.12.x
3. أثناء التثبيت، فعّل "Add to PATH"
4. بعد التثبيت: `py -3.12 --version`

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

### macOS:
```bash
brew install python@3.12
```

---

## ❓ الأسئلة الشائعة

### Q: هل أحذف Python 3.14؟
**A:** لا! خليها واستخدم `py -3.12` لتحديد الإصدار.

### Q: كيف أخلي 3.12 هو الافتراضي؟
**A:** 
```powershell
# Windows: عدّل متغيرات البيئة
# أو استخدم دائماً: py -3.12

# Linux: 
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

### Q: وش أسوي إذا ما عندي 3.12؟
**A:** استخدم الملفات المتوافقة (comprehensive_scan.py يشتغل على 3.14)

### Q: متى يصير networkx متوافق مع 3.14؟
**A:** عادةً بعد 3-6 شهور من صدور إصدار Python جديد.

---

## 📝 ملخص سريع

```powershell
# الحل السريع (Python 3.14):
python comprehensive_scan.py test.py

# الحل الأفضل (Python 3.12):
py -3.12 comprehensive_scan.py test.py

# فحص أمني فقط (يشتغل على كل الإصدارات):
python src/core/advanced_security.py test.py
```

---

## 🆘 المساعدة

إذا ما زالت المشكلة موجودة:

1. **تأكد من الإصدار:**
   ```powershell
   python --version
   ```

2. **جرب comprehensive_scan.py مباشرة:**
   ```powershell
   python comprehensive_scan.py TEST_EXAMPLE.py
   ```

3. **شغّل الفحوصات منفردة:**
   ```powershell
   python src/core/smell_detector.py TEST_EXAMPLE.py
   ```

---

**الخلاصة: استخدم Python 3.12 للتوافق الأمثل، أو استخدم الملفات المتوافقة على 3.14** ✅
