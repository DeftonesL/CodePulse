import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scanner import PulseScanner
from ai_engine import AIEngine

try:
    from advanced_metrics import AdvancedMetricsCalculator
    from code_patterns import CodePatternsDetector
    from performance_analyzer import PerformanceAnalyzer
    ADVANCED_FEATURES = True
except ImportError:
    ADVANCED_FEATURES = False
    logging.warning("Advanced features not available")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from modules.security import SecurityScanner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ComprehensiveReport:
    pass
    project_path: str
    scan_date: str
    
    total_files: int
    total_lines: int
    languages: Dict[str, int]
    
    avg_quality_score: float
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    
    security_score: float
    security_issues: int
    critical_vulnerabilities: int
    high_vulnerabilities: int
    
    overall_score: float
    grade: str
    
    top_issues: List[Dict]
    top_vulnerabilities: List[Dict]
    recommendations: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)

class ComprehensiveAnalyzer:
    pass
    
    def __init__(self, project_path: str, api_key: Optional[str] = None):
        self.project_path = Path(project_path).resolve()
        self.api_key = api_key
        
        self.scanner = PulseScanner(str(self.project_path))
        self.ai_engine = AIEngine(api_key=api_key) if api_key else None
        self.security_scanner = SecurityScanner()
        
        logger.info(f"Initialized comprehensive analyzer for: {self.project_path}")
    
    def analyze(self, max_files_ai: int = 5) -> ComprehensiveReport:
        logger.info("Starting comprehensive analysis...")
        
        logger.info("Step 1/3: Scanning project structure...")
        structure = self.scanner.scan()
        
        logger.info("Step 2/3: Running security scan...")
        security_results = self._run_security_scan(structure)
        
        logger.info("Step 3/3: Running AI analysis...")
        ai_results = self._run_ai_analysis(structure, max_files_ai)
        
        logger.info("Generating comprehensive report...")
        report = self._generate_report(structure, ai_results, security_results)
        
        logger.info("Analysis complete!")
        return report
    
    def _run_security_scan(self, structure) -> Dict:
        all_issues = []
        
        for file_meta in structure.files:
            if file_meta.language != 'Python':
                continue
            
            file_path = os.path.join(structure.root_path, file_meta.path)
            issues = self.security_scanner.scan_file(file_path)
            all_issues.extend(issues)
        
        return self.security_scanner.generate_report(all_issues)
    
    def _run_ai_analysis(self, structure, max_files: int) -> Dict:
        if not self.ai_engine:
            logger.warning("No API key - skipping AI analysis")
            return {
                'avg_score': 75.0,
                'results': [],
                'total_issues': 0,
                'skipped': True
            }
        
        results = []
        analyzed_count = 0
        total_issues = 0
        
        for file_meta in structure.files:
            if analyzed_count >= max_files:
                break
            
            if file_meta.language != 'Python':
                continue
            
            try:
                file_path = os.path.join(structure.root_path, file_meta.path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                context = {
                    'imports': file_meta.imports,
                    'functions': file_meta.functions,
                    'classes': file_meta.classes,
                    'complexity': file_meta.complexity_score
                }
                
                result = self.ai_engine.analyze_code(code, file_meta.path, context)
                results.append(result)
                total_issues += len(result.issues)
                analyzed_count += 1
                
            except Exception as e:
                logger.error(f"Failed to analyze {file_meta.path}: {e}")
        
        avg_score = sum(r.overall_score for r in results) / len(results) if results else 0
        
        return {
            'avg_score': avg_score,
            'results': results,
            'total_issues': total_issues,
            'skipped': False
        }
    
    def _calculate_grade(self, score: float) -> str:
        if score >= 90:
            return "A+ Excellent"
        elif score >= 85:
            return "A Very Good"
        elif score >= 80:
            return "B+ Good"
        elif score >= 75:
            return "B Fair"
        elif score >= 70:
            return "C+ Needs Improvement"
        elif score >= 60:
            return "C Weak"
        else:
            return "D Needs Serious Work"
    
    def _generate_report(self, structure, ai_results, security_results) -> ComprehensiveReport:
        
        critical_issues = 0
        high_issues = 0
        medium_issues = 0
        low_issues = 0
        
        if not ai_results['skipped']:
            for result in ai_results['results']:
                for issue in result.issues:
                    if issue.severity.value == 'critical':
                        critical_issues += 1
                    elif issue.severity.value == 'high':
                        high_issues += 1
                    elif issue.severity.value == 'medium':
                        medium_issues += 1
                    elif issue.severity.value == 'low':
                        low_issues += 1
        
        top_issues = []
        if not ai_results['skipped']:
            all_issues = []
            for result in ai_results['results']:
                for issue in result.issues:
                    all_issues.append({
                        'file': result.file_path,
                        'line': issue.line_number,
                        'severity': issue.severity.value,
                        'title': issue.title,
                        'description': issue.description[:100] + '...' if len(issue.description) > 100 else issue.description
                    })
            
            severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
            all_issues.sort(key=lambda x: severity_order.get(x['severity'], 4))
            top_issues = all_issues[:5]  # Top 5
        
        top_vulnerabilities = []
        if security_results['issues']:
            for issue_dict in security_results['issues'][:5]:  # Top 5
                top_vulnerabilities.append({
                    'file': issue_dict['file_path'],
                    'line': issue_dict['line_number'],
                    'severity': issue_dict['severity'],
                    'title': issue_dict['title'],
                    'type': issue_dict['vulnerability_type']
                })
        
        recommendations = []
        
        if security_results['security_score'] < 80:
            recommendations.append("Security: Critical vulnerabilities need immediate fixing")
        
        if ai_results['avg_score'] < 75:
            recommendations.append("Code Quality: Consider code review and refactoring")
        
        if critical_issues > 0:
            recommendations.append(f"Critical Issues: {critical_issues} critical problems found")
        
        if structure.total_files > 0:
            avg_lines_per_file = structure.total_lines / structure.total_files
            if avg_lines_per_file > 500:
                recommendations.append("File Size: Some files are too large, consider splitting")
        
        if not recommendations:
            recommendations.append("Excellent! Project is in good shape, keep maintaining quality")
        
        quality_weight = 0.4
        security_weight = 0.6
        
        overall_score = (
            ai_results['avg_score'] * quality_weight +
            security_results['security_score'] * security_weight
        )
        
        grade = self._calculate_grade(overall_score)
        
        report = ComprehensiveReport(
            project_path=str(self.project_path),
            scan_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_files=structure.total_files,
            total_lines=structure.total_lines,
            languages=structure.languages,
            avg_quality_score=ai_results['avg_score'],
            total_issues=ai_results['total_issues'],
            critical_issues=critical_issues,
            high_issues=high_issues,
            medium_issues=medium_issues,
            low_issues=low_issues,
            security_score=security_results['security_score'],
            security_issues=security_results['total_issues'],
            critical_vulnerabilities=security_results['severity_breakdown']['critical'],
            high_vulnerabilities=security_results['severity_breakdown']['high'],
            overall_score=overall_score,
            grade=grade,
            top_issues=top_issues,
            top_vulnerabilities=top_vulnerabilities,
            recommendations=recommendations
        )
        
        return report
    
    def print_report(self, report: ComprehensiveReport):
        print("\n" + "="*70)
        print("🫀 CODEPULSE - COMPREHENSIVE ANALYSIS REPORT")
        print("="*70)
        
        print(f"\nProject: {report.project_path}")
        print(f"Date: {report.scan_date}")
        
        print("\n" + "-"*70)
        print("GENERAL INFORMATION:")
        print("-"*70)
        print(f"  • Files: {report.total_files}")
        print(f"  • Lines: {report.total_lines:,}")
        print(f"  • Languages: {', '.join(report.languages.keys())}")
        
        print("\n" + "-"*70)
        print("FINAL GRADE:")
        print("-"*70)
        
        if report.overall_score >= 85:
            score_emoji = "[EXCELLENT]"
        elif report.overall_score >= 70:
            score_emoji = "[GOOD]"
        else:
            score_emoji = "[NEEDS WORK]"
        
        print(f"  {score_emoji} {report.overall_score:.1f}/100 - {report.grade}")
        
        print("\n" + "-"*70)
        print("DETAILS:")
        print("-"*70)
        print(f"  • Code Quality: {report.avg_quality_score:.1f}/100")
        print(f"  • Security: {report.security_score:.1f}/100")
        
        print(f"\n  • Code Issues: {report.total_issues}")
        if report.critical_issues > 0:
            print(f"    [CRITICAL]: {report.critical_issues}")
        if report.high_issues > 0:
            print(f"    [HIGH]: {report.high_issues}")
        if report.medium_issues > 0:
            print(f"    [MEDIUM]: {report.medium_issues}")
        if report.low_issues > 0:
            print(f"    [LOW]: {report.low_issues}")
        
        print(f"\n  • Security Vulnerabilities: {report.security_issues}")
        if report.critical_vulnerabilities > 0:
            print(f"    [CRITICAL]: {report.critical_vulnerabilities}")
        if report.high_vulnerabilities > 0:
            print(f"    [HIGH]: {report.high_vulnerabilities}")
        
        if report.top_issues:
            print("\n" + "-"*70)
            print("TOP ISSUES:")
            print("-"*70)
            for i, issue in enumerate(report.top_issues[:3], 1):
                print(f"\n  {i}. [{issue['severity'].upper()}] {issue['title']}")
                print(f"     File: {issue['file']}:{issue['line']}")
                print(f"     Details: {issue['description']}")
        
        if report.top_vulnerabilities:
            print("\n" + "-"*70)
            print("TOP SECURITY VULNERABILITIES:")
            print("-"*70)
            for i, vuln in enumerate(report.top_vulnerabilities[:3], 1):
                print(f"\n  {i}. [{vuln['severity'].upper()}] {vuln['title']}")
                print(f"     File: {vuln['file']}:{vuln['line']}")
                print(f"     Type: {vuln['type']}")
        
        print("\n" + "-"*70)
        print("RECOMMENDATIONS:")
        print("-"*70)
        for i, rec in enumerate(report.recommendations, 1):
            print(f"  {i}. {rec}")
        
        print("\n" + "="*70)
        print("END OF REPORT")
        print("="*70 + "\n")
    
    def export_report(self, report: ComprehensiveReport, output_path: str):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report exported to: {output_path}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <project_path> [api_key]")
        print("\nExample:")
        print("  python analyzer.py ./my-project")
        print("  python analyzer.py ./my-project your-api-key")
        sys.exit(1)
    
    project_path = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    analyzer = ComprehensiveAnalyzer(project_path, api_key=api_key)
    
    report = analyzer.analyze(max_files_ai=10)
    
    analyzer.print_report(report)
    
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(reports_dir, f"comprehensive_report_{timestamp}.json")
    
    analyzer.export_report(report, output_file)
    
    print(f"\nFull report saved to: {output_file}")
    print(f"Reports directory: {os.path.abspath(reports_dir)}")

if __name__ == '__main__':
    main()
