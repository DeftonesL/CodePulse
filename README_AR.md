# CodePulse

أداة احترافية لتحليل الكود الثابت تدعم أكثر من 50 لغة برمجة مع كشف متقدم لأنماط الأمان وتقارير شاملة.

## المميزات

- دعم متعدد اللغات (Python, JavaScript, Java, C/C++, PHP, Ruby, Go, Rust وأكثر من 40 لغة أخرى)
- كشف متقدم للثغرات الأمنية (OWASP Top 10)
- فحص متعدد الخيوط للمشاريع على مستوى المؤسسات
- تقارير احترافية بصيغة HTML و JSON
- إعدادات قابلة للتخصيص لعمق الفحص والأداء
- لا يوجد اعتماديات خارجية للفحص الأساسي

## البدء السريع

### التثبيت

```bash
# استنساخ المستودع
git clone https://github.com/DeftonesL/codepulse.git
cd codepulse

# تثبيت المتطلبات
pip install -r requirements.txt

# أو استخدام سكريبتات الإعداد
./setup.sh        # Linux/Mac
setup.bat         # Windows
```

### الاستخدام الأساسي

```bash
# الوضع التفاعلي
python codepulse.py

# فحص سريع
python codepulse.py --scan quick --path /your/project

# فحص أمني مركز
python codepulse.py --scan security --path /your/project --format both
```

## التوثيق

- [نظرة عامة](docs/OVERVIEW.md) - البنية والقرارات التصميمية
- [اللغات المدعومة](docs/LANGUAGES.md) - قائمة كاملة بأنواع الملفات المدعومة
- [الأنماط الأمنية](docs/SECURITY.md) - أنماط الكشف والقواعد
- [الإعدادات](docs/CONFIG.md) - خيارات الإعدادات المتقدمة
- [المساهمة](CONTRIBUTING.md) - إرشادات المساهمة
- [سجل التغييرات](CHANGELOG.md) - تاريخ الإصدارات

## أنواع الفحص

### الفحص السريع
فحوصات أمنية سريعة عبر جميع اللغات المدعومة. مثالي لدمج CI/CD.

### الفحص العميق
تحليل شامل يتضمن الاعتماديات بين الملفات ومطابقة الأنماط المتقدمة.

### الفحص الأمني
كشف الثغرات الأمنية مع التركيز على OWASP مع إرشادات معالجة مفصلة.

### المؤسسي الكامل
تحليل احترافي كامل مع تفعيل جميع المميزات لإصدارات الإنتاج.

## اللغات المدعومة

**أنظمة**: C, C++, Rust, Go  
**JVM**: Java, Kotlin, Scala, Groovy  
**ويب**: JavaScript, TypeScript, PHP, Ruby, Python  
**موبايل**: Swift, Objective-C, Dart  
**بيانات**: SQL, JSON, YAML, XML  
**سكريبتات**: Shell, PowerShell, Batch  

[عرض القائمة الكاملة](docs/LANGUAGES.md)

## الإعدادات

### خيوط المعالجة
```bash
# استخدم 8 معالجات متوازية لفحص أسرع
python codepulse.py --workers 8
```

### صيغة الإخراج
```bash
# إنشاء تقارير HTML و JSON معاً
python codepulse.py --format both
```

### الأنماط المخصصة
أضف أنماط أمنية مخصصة في `config/patterns.json`

## الأداء

- المشاريع الصغيرة (< 1,000 ملف): < 5 ثواني
- المشاريع المتوسطة (1,000-10,000 ملف): 30-60 ثانية
- المشاريع الكبيرة (10,000+ ملف): 2-5 دقائق

الأداء يتناسب خطياً مع عدد المعالجات على الأنظمة متعددة النوى.

## دمج CI/CD

### GitHub Actions
```yaml
- name: تشغيل CodePulse
  run: |
    pip install -r requirements.txt
    python codepulse.py --scan security --format json --output results.json
```

### GitLab CI
```yaml
codepulse:
  script:
    - pip install -r requirements.txt
    - python codepulse.py --scan quick --format json
```

## المتطلبات

- Python 3.9 أو أعلى
- 2GB RAM كحد أدنى (4GB موصى به)
- معالج متعدد النوى موصى به للفحص المتوازي

## الترخيص

ترخيص MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل

## الدعم

- المشاكل: [GitHub Issues](https://github.com/DeftonesL/codepulse/issues)
- التوثيق: [Wiki](https://github.com/DeftonesL/codepulse/wiki)
- الأمان: [SECURITY.md](SECURITY.md)

## الاعتمادات

تم التطوير مع التركيز على الأمان والأداء وسهولة الاستخدام لفرق التطوير الاحترافية.

---

[English Version](README.md)
