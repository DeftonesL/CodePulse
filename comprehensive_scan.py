"""
Comprehensive Code Scanner
===========================

Runs ALL analysis engines in one command:
1. Deep Analysis (CFG, DFG, Call Graphs)
2. Clone Detection (4 types)
3. Code Smells (5 categories)
4. Advanced Security (OWASP Top 10)
5. Performance Analysis
6. Code Metrics
7. Best Practices

Usage:
    python comprehensive_scan.py <file_or_directory>
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Import all analysis engines
try:
    from deep_analysis_standalone import DeepAnalysisEngine
except:
    from src.core.deep_analysis_standalone import DeepAnalysisEngine

try:
    from clone_detection import CloneDetector, SemanticCloneDetector
except:
    from src.core.clone_detection import CloneDetector, SemanticCloneDetector

try:
    from smell_detector import IntelligentSmellDetector
except:
    from src.core.smell_detector import IntelligentSmellDetector

try:
    from advanced_security import AdvancedSecurityScanner
except:
    from src.core.advanced_security import AdvancedSecurityScanner

try:
    from multi_format_scanner import MultiFormatScanner
except:
    try:
        from src.core.multi_format_scanner import MultiFormatScanner
    except:
        MultiFormatScanner = None

try:
    from advanced_language_scanner import AdvancedLanguageScanner
except:
    try:
        from src.core.advanced_language_scanner import AdvancedLanguageScanner
    except:
        AdvancedLanguageScanner = None

try:
    from performance_analyzer import PerformanceAnalyzer
except:
    try:
        from src.core.performance_analyzer import PerformanceAnalyzer
    except:
        PerformanceAnalyzer = None

# Disable cross_file_analysis for Python 3.14 (networkx incompatibility)
ENABLE_CROSS_FILE = False
try:
    import networkx
    ENABLE_CROSS_FILE = True
except:
    pass

try:
    from advanced_metrics import AdvancedMetricsCalculator
except:
    try:
        from src.core.advanced_metrics import AdvancedMetricsCalculator
    except:
        AdvancedMetricsCalculator = None


class ComprehensiveScanner:
    """
    Runs all analysis engines and generates unified report.
    """
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Comprehensive scan of single file"""
        self.start_time = time.time()
        
        # 1. Deep Analysis
        deep_engine = DeepAnalysisEngine()
        deep_results = deep_engine.analyze_file(file_path)
        self.results['deep_analysis'] = deep_results
        
        # 2. Clone Detection
        clone_detector = CloneDetector(min_lines=6)
        clones = clone_detector.detect_clones_in_file(file_path)
        clone_report = clone_detector.get_clone_report()
        self.results['clone_detection'] = clone_report
        
        # 3. Code Smells
        smell_detector = IntelligentSmellDetector()
        smells = smell_detector.detect_smells(file_path)
        smell_report = smell_detector.get_smell_report()
        self.results['code_smells'] = smell_report
        
        # 4. Security Scan
        security_scanner = AdvancedSecurityScanner()
        security_issues = security_scanner.scan_file(file_path)
        security_report = security_scanner.get_report()
        self.results['security'] = security_report
        
        # 5. Performance Analysis
        if PerformanceAnalyzer:
            try:
                perf_analyzer = PerformanceAnalyzer()
                perf_issues = perf_analyzer.analyze_file(file_path)
                self.results['performance'] = {
                    'total_issues': len(perf_issues),
                    'issues': perf_issues
                }
            except:
                pass
        
        # 6. Advanced Metrics
        if AdvancedMetricsCalculator:
            try:
                metrics_calc = AdvancedMetricsCalculator()
                metrics = metrics_calc.calculate_file_metrics(file_path)
                self.results['metrics'] = metrics
            except:
                pass
        
        self.end_time = time.time()
        
        # Calculate overall score
        self.results['overall_score'] = self._calculate_overall_score()
        self.results['scan_time'] = round(self.end_time - self.start_time, 2)
        
        return self.results
    
    def _make_json_serializable(self, obj):
        """Convert objects to JSON-serializable format - handles all Python types"""
        # Handle None
        if obj is None:
            return None
        
        # Handle primitives (str, int, float, bool)
        if isinstance(obj, (str, int, float, bool)):
            return obj
        
        # Handle dict
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        
        # Handle list
        if isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        
        # Handle tuple
        if isinstance(obj, tuple):
            return [self._make_json_serializable(item) for item in obj]
        
        # Handle set
        if isinstance(obj, set):
            return [self._make_json_serializable(item) for item in obj]
        
        # Handle mappingproxy (from __dict__)
        if str(type(obj)) == "<class 'mappingproxy'>":
            return {k: self._make_json_serializable(v) for k, v in dict(obj).items()}
        
        # Handle staticmethod, classmethod, property
        if isinstance(obj, (staticmethod, classmethod, property)):
            return str(obj)
        
        # Handle functions and methods
        if callable(obj) and not isinstance(obj, type):
            return f"<function {getattr(obj, '__name__', 'unknown')}>"
        
        # Handle classes
        if isinstance(obj, type):
            return f"<class {obj.__name__}>"
        
        # Handle objects with __dict__
        if hasattr(obj, '__dict__'):
            try:
                return self._make_json_serializable(dict(obj.__dict__))
            except:
                return str(obj)
        
        # Handle iterables (but not strings/bytes)
        if hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
            try:
                return [self._make_json_serializable(item) for item in obj]
            except:
                return str(obj)
        
        # Fallback: convert to string
        try:
            return str(obj)
        except:
            return "<unserializable object>"
    
    def scan_directory(self, dir_path: str) -> Dict[str, Any]:
        """Scan all supported files in directory"""
        print(f"\n{'='*70}")
        print(f"🫀 CODEPULSE - PROJECT SCAN")
        print(f"{'='*70}")
        print(f"\nDirectory: {dir_path}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Supported file extensions
        code_extensions = {
            '.py': 'Python',
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
        }
        
        web_extensions = {
            '.html': 'HTML',
            '.htm': 'HTML',
        }
        
        data_extensions = {
            '.json': 'JSON',
            '.sql': 'SQL',
        }
        
        all_extensions = {**code_extensions, **web_extensions, **data_extensions}
        
        # Find all supported files
        all_files = []
        file_counts = {}
        
        for root, dirs, files in os.walk(dir_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.git', 'node_modules', 'vendor', 'target', 'build', 'dist']]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in all_extensions:
                    all_files.append(os.path.join(root, file))
                    lang = all_extensions[ext]
                    file_counts[lang] = file_counts.get(lang, 0) + 1
        
        # Display file counts
        print(f"Found {len(all_files)} files:\n")
        for lang in sorted(file_counts.keys()):
            icon = self._get_language_icon(lang)
            print(f"  {icon} {lang:12s}: {file_counts[lang]:3d}")
        print()
        
        # Scan files
        all_results = {}
        total_issues = {
            'security': 0,
            'smells': 0,
            'clones': 0,
            'performance': 0
        }
        
        # Group files by type for better progress display
        python_files = [f for f in all_files if f.endswith('.py')]
        code_files = [f for f in all_files if os.path.splitext(f)[1] in code_extensions and not f.endswith('.py')]
        web_files = [f for f in all_files if os.path.splitext(f)[1] in web_extensions]
        data_files = [f for f in all_files if os.path.splitext(f)[1] in data_extensions]
        
        # Scan Python files (full analysis)
        if python_files:
            print(f"🐍 Analyzing Python files...")
            for i, file_path in enumerate(python_files, 1):
                filename = os.path.basename(file_path)
                print(f"  [{i}/{len(python_files)}] {filename:40s}", end=" ", flush=True)
                
                try:
                    result = self.scan_file(file_path)
                    all_results[file_path] = self._make_json_serializable(result)
                    
                    total_issues['security'] += result.get('security', {}).get('total_issues', 0)
                    total_issues['smells'] += result.get('code_smells', {}).get('total_smells', 0)
                    total_issues['clones'] += result.get('clone_detection', {}).get('total_clones', 0)
                    total_issues['performance'] += result.get('performance', {}).get('total_issues', 0)
                    
                    print("✓")
                except Exception as e:
                    print(f"❌")
            print()
        
        # Scan other code files (security only)
        if code_files and AdvancedLanguageScanner:
            print(f"💻 Analyzing code files...")
            lang_scanner = AdvancedLanguageScanner()
            
            for i, file_path in enumerate(code_files, 1):
                filename = os.path.basename(file_path)
                ext = os.path.splitext(file_path)[1]
                lang = code_extensions.get(ext, 'Unknown')
                
                print(f"  [{i}/{len(code_files)}] [{lang:4s}] {filename:30s}", end=" ", flush=True)
                
                try:
                    result = lang_scanner.scan_file(file_path)
                    if 'error' not in result:
                        all_results[file_path] = self._make_json_serializable(result)
                        total_issues['security'] += result.get('total_issues', 0)
                        print("✓")
                    else:
                        print("⚠")
                except Exception as e:
                    print("❌")
            print()
        
        # Scan web/data files
        if (web_files or data_files) and MultiFormatScanner:
            print(f"📄 Analyzing web & data files...")
            multi_scanner = MultiFormatScanner()
            
            for file_list in [web_files, data_files]:
                for i, file_path in enumerate(file_list, 1):
                    filename = os.path.basename(file_path)
                    ext = os.path.splitext(file_path)[1]
                    
                    print(f"  [{i}/{len(file_list)}] [{ext[1:]:4s}] {filename:30s}", end=" ", flush=True)
                    
                    try:
                        result = multi_scanner.scan_file(file_path)
                        all_results[file_path] = self._make_json_serializable(result)
                        total_issues['security'] += result.get('total_issues', 0)
                        print("✓")
                    except Exception as e:
                        print("❌")
            print()
        
        # Project summary
        project_summary = {
            'total_files': len(all_files),
            'files_scanned': len(all_results),
            'file_types': file_counts,
            'total_issues': total_issues,
            'project_score': self._calculate_project_score(all_results),
            'files': all_results
        }
        
        return project_summary
    
    def _get_language_icon(self, language: str) -> str:
        """Get emoji icon for language"""
        icons = {
            'Python': '🐍',
            'JavaScript': '💛',
            'TypeScript': '💙',
            'PHP': '🐘',
            'Java': '☕',
            'C#': '🔷',
            'Go': '🔵',
            'Ruby': '💎',
            'Rust': '🦀',
            'Kotlin': '🟣',
            'HTML': '🌐',
            'JSON': '📄',
            'SQL': '💾',
        }
        return icons.get(language, '📝')
    
    def _calculate_overall_score(self) -> float:
        """Calculate overall code quality score"""
        weights = {
            'security': 0.35,
            'code_smells': 0.25,
            'deep_analysis': 0.20,
            'clones': 0.10,
            'performance': 0.10
        }
        
        scores = {}
        
        # Security score
        if 'security' in self.results:
            scores['security'] = self.results['security'].get('security_score', 0)
        
        # Smell score
        if 'code_smells' in self.results:
            scores['code_smells'] = self.results['code_smells'].get('code_health_score', 0)
        
        # Deep analysis score
        if 'deep_analysis' in self.results:
            scores['deep_analysis'] = self.results['deep_analysis'].get('code_quality_score', 0)
        
        # Clone score (inverse of duplication)
        if 'clone_detection' in self.results:
            clones = self.results['clone_detection'].get('total_clones', 0)
            scores['clones'] = max(0, 100 - (clones * 5))
        
        # Performance score
        if 'performance' in self.results:
            perf_issues = self.results['performance'].get('total_issues', 0)
            scores['performance'] = max(0, 100 - (perf_issues * 10))
        
        # Weighted average
        total_score = 0
        total_weight = 0
        for key, weight in weights.items():
            if key in scores:
                total_score += scores[key] * weight
                total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0, 1)
    
    def _calculate_project_score(self, all_results: Dict) -> float:
        """Calculate project-wide score"""
        if not all_results:
            return 0.0
        
        scores = [r.get('overall_score', 0) for r in all_results.values()]
        return round(sum(scores) / len(scores), 1)
    
    def print_summary(self):
        """Print beautiful summary report"""
        print(f"\n{'='*70}")
        print("📊 ANALYSIS SUMMARY")
        print(f"{'='*70}\n")
        
        # Overall Score
        score = self.results.get('overall_score', 0)
        grade = self._get_grade(score)
        
        # Color-coded score
        if score >= 80:
            score_icon = "🟢"
        elif score >= 60:
            score_icon = "🟡"
        else:
            score_icon = "🔴"
        
        print(f"{score_icon} Overall Score: {score}/100 ({grade})")
        print(f"⏱️  Scan Time: {self.results.get('scan_time', 0)}s\n")
        
        # Quick Stats
        security = self.results.get('security', {})
        smells = self.results.get('code_smells', {})
        clones = self.results.get('clone_detection', {})
        perf = self.results.get('performance', {})
        
        print(f"{'─'*70}")
        print("🎯 ISSUES FOUND")
        print(f"{'─'*70}")
        
        sec_count = security.get('total_issues', 0)
        smell_count = smells.get('total_smells', 0)
        clone_count = clones.get('total_clones', 0)
        perf_count = perf.get('total_issues', 0)
        
        print(f"🔒 Security:     {sec_count:3d} issues")
        print(f"👃 Code Smells:  {smell_count:3d} issues")
        print(f"🔍 Clones:       {clone_count:3d} duplicates")
        print(f"⚡ Performance:  {perf_count:3d} issues")
        print()
        
        # Security Details
        if sec_count > 0:
            print(f"{'─'*70}")
            print("🔒 SECURITY BREAKDOWN")
            print(f"{'─'*70}")
            by_sev = security.get('by_severity', {})
            for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                count = by_sev.get(sev, 0)
                if count > 0:
                    icon = '🔴' if sev == 'CRITICAL' else '🟠' if sev == 'HIGH' else '🟡' if sev == 'MEDIUM' else '🟢'
                    print(f"  {icon} {sev:8s}: {count}")
            print()
        
        # Top Issues
        print(f"{'─'*70}")
        print("⚠️  TOP 5 PRIORITY ISSUES")
        print(f"{'─'*70}")
        
        top_issues = []
        
        # Add critical security
        if security.get('issues'):
            for issue in security['issues'][:3]:
                if issue['severity'] in ['CRITICAL', 'HIGH']:
                    top_issues.append({
                        'type': 'SECURITY',
                        'severity': issue['severity'],
                        'desc': f"{issue['type']} (Line {issue['line']})",
                        'fix': issue['recommendation']
                    })
        
        # Add high smells
        if smells.get('smells'):
            for smell in smells['smells'][:2]:
                if smell['severity'] in ['HIGH', 'MEDIUM']:
                    top_issues.append({
                        'type': 'SMELL',
                        'severity': smell['severity'],
                        'desc': f"{smell['name']} (Line {smell['line']})",
                        'fix': smell['refactoring']
                    })
        
        for i, issue in enumerate(top_issues[:5], 1):
            sev_icon = '🔴' if issue['severity'] == 'CRITICAL' else '🟠' if issue['severity'] == 'HIGH' else '🟡'
            print(f"\n{i}. [{issue['type']}] {issue['desc']}")
            print(f"   {sev_icon} {issue['severity']}")
            print(f"   💡 {issue['fix'][:60]}...")
        
        if not top_issues:
            print("\n✅ No critical issues found!")
        
        print(f"\n{'='*70}\n")
        
        # Deep Analysis
        if 'deep_analysis' in self.results:
            deep = self.results['deep_analysis']
            cf = deep.get('control_flow_analysis', {})
            if cf.get('issues'):
                print(f"{'─'*70}")
                print("🧠 CONTROL FLOW WARNINGS")
                print(f"{'─'*70}")
                for issue in cf['issues'][:3]:
                    print(f"  ⚠️  {issue['message']}")
                print()
        
        # Recommendations
        print(f"{'─'*70}")
        print("🎯 RECOMMENDATIONS")
        print(f"{'─'*70}")
        
        recs = self._generate_recommendations()
        for i, rec in enumerate(recs[:5], 1):
            print(f"{i}. {rec}")
        
        print(f"\n{'='*70}\n")
    
    def _get_grade(self, score: float) -> str:
        """Get letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "C+"
        elif score >= 60:
            return "C"
        else:
            return "D"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate priority recommendations"""
        recs = []
        
        # Security
        if 'security' in self.results:
            sec = self.results['security']
            if sec.get('by_severity', {}).get('CRITICAL', 0) > 0:
                recs.append("⚡ URGENT: Fix CRITICAL security vulnerabilities")
            if sec.get('by_severity', {}).get('HIGH', 0) > 0:
                recs.append("🔴 HIGH: Address high-severity security issues")
        
        # Code Smells
        if 'code_smells' in self.results:
            smells = self.results['code_smells']
            if smells.get('total_smells', 0) > 10:
                recs.append("🟡 MEDIUM: Refactor code smells for better maintainability")
        
        # Clones
        if 'clone_detection' in self.results:
            clones = self.results['clone_detection']
            if clones.get('total_duplicated_lines', 0) > 50:
                recs.append("🟡 MEDIUM: Reduce code duplication")
        
        # Performance
        if 'performance' in self.results:
            perf = self.results['performance']
            if perf.get('total_issues', 0) > 5:
                recs.append("🟢 LOW: Optimize performance bottlenecks")
        
        if not recs:
            recs.append("✅ Great! No major issues found.")
        
        return recs
    
    def save_report(self, output_path: str):
        """Save detailed JSON report with safe serialization"""
        try:
            # Make sure everything is serializable
            safe_results = self._make_json_serializable(self.results)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(safe_results, f, indent=2, ensure_ascii=False)
            print(f"💾 Report saved to: {output_path}")
        except Exception as e:
            print(f"⚠️  Warning: Could not save full JSON report: {e}")
            # Save minimal report as fallback
            try:
                minimal_report = {
                    'overall_score': self.results.get('overall_score', 0),
                    'scan_time': self.results.get('scan_time', 0),
                    'summary': 'Full report could not be serialized'
                }
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(minimal_report, f, indent=2)
                print(f"💾 Minimal report saved to: {output_path}")
            except:
                print(f"❌ Could not save report to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_scan.py <file_or_directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = ComprehensiveScanner()
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.getcwd(), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    if os.path.isfile(target):
        # Single file scan
        print(f"\n{'='*70}")
        print(f"🫀 CODEPULSE - FILE ANALYSIS")
        print(f"{'='*70}")
        print(f"\nFile: {target}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print("⚙️  Running comprehensive analysis...", end=" ", flush=True)
        results = scanner.scan_file(target)
        print("✓\n")
        
        scanner.print_summary()
        
        # Save report in reports directory
        report_filename = f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(reports_dir, report_filename)
        scanner.save_report(report_path)
        
    elif os.path.isdir(target):
        # Directory scan
        results = scanner.scan_directory(target)
        
        print(f"\n{'='*70}")
        print("📊 PROJECT SUMMARY")
        print(f"{'='*70}\n")
        
        score = results['project_score']
        grade = scanner._get_grade(score)
        
        # Color-coded score
        if score >= 80:
            score_icon = "🟢"
        elif score >= 60:
            score_icon = "🟡"
        else:
            score_icon = "🔴"
        
        print(f"{score_icon} Project Score: {score}/100 ({grade})")
        print(f"📁 Files: {results['files_scanned']}/{results['total_files']}\n")
        
        print(f"{'─'*70}")
        print("🎯 TOTAL ISSUES ACROSS PROJECT")
        print(f"{'─'*70}")
        for issue_type, count in results['total_issues'].items():
            icon = '🔒' if issue_type == 'security' else '👃' if issue_type == 'smells' else '🔍' if issue_type == 'clones' else '⚡'
            print(f"{icon} {issue_type.title():12s}: {count:4d}")
        
        # Priority files
        print(f"\n{'─'*70}")
        print("⚠️  FILES NEEDING ATTENTION")
        print(f"{'─'*70}")
        
        file_scores = []
        for file_path, file_result in results['files'].items():
            file_score = file_result.get('overall_score', 100)
            file_scores.append((os.path.basename(file_path), file_score, file_path))
        
        file_scores.sort(key=lambda x: x[1])  # Sort by score (lowest first)
        
        for i, (filename, score, path) in enumerate(file_scores[:5], 1):
            icon = "🔴" if score < 60 else "🟡" if score < 80 else "🟢"
            print(f"{i}. {icon} {filename:30s} {score:5.1f}/100")
        
        # Save report in reports directory
        report_filename = f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(reports_dir, report_filename)
        
        try:
            safe_results = scanner._make_json_serializable(results)
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(safe_results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Detailed report: {report_path}")
        except Exception as e:
            print(f"\n⚠️  Warning: Could not save full report: {e}")
            # Save summary only
            try:
                summary = {
                    'total_files': results['total_files'],
                    'files_scanned': results['files_scanned'],
                    'project_score': results['project_score'],
                    'total_issues': results['total_issues']
                }
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, indent=2)
                print(f"💾 Summary report saved: {report_path}")
            except:
                print(f"❌ Could not save report")
        
        print(f"{'='*70}\n")
        
    else:
        print(f"Error: {target} is not a file or directory")
        sys.exit(1)


if __name__ == '__main__':
    main()
