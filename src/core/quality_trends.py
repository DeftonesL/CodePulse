"""
Quality Trends Analyzer
========================

Tracks code quality changes over time.
Compares current state with historical data.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class QualitySnapshot:
    """Single point-in-time quality measurement"""
    timestamp: str
    commit_hash: Optional[str]
    metrics: Dict[str, float]
    issues_count: Dict[str, int]
    files_analyzed: int
    total_lines: int
    overall_score: float


class QualityTrendsAnalyzer:
    """
    Analyzes quality trends over time.
    Stores snapshots and detects improvements/regressions.
    """
    
    def __init__(self, history_file: str = '.codepulse_history.json'):
        self.history_file = history_file
        self.history = self._load_history()
        
    def _load_history(self) -> List[QualitySnapshot]:
        """Load historical quality data"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                return [QualitySnapshot(**item) for item in data]
            except (IOError, json.JSONDecodeError, KeyError) as e:
                # Failed to load history file
                return []
        return []
    
    def _save_history(self):
        """Save quality history"""
        with open(self.history_file, 'w') as f:
            json.dump([asdict(s) for s in self.history], f, indent=2)
    
    def add_snapshot(self, 
                    metrics: Dict[str, float],
                    issues: Dict[str, int],
                    files: int,
                    lines: int,
                    score: float,
                    commit: Optional[str] = None):
        """Add new quality snapshot"""
        snapshot = QualitySnapshot(
            timestamp=datetime.now().isoformat(),
            commit_hash=commit,
            metrics=metrics,
            issues_count=issues,
            files_analyzed=files,
            total_lines=lines,
            overall_score=score
        )
        
        self.history.append(snapshot)
        self._save_history()
        
        return self.analyze_trend()
    
    def analyze_trend(self) -> Dict[str, Any]:
        """Analyze quality trends"""
        if len(self.history) < 2:
            return {
                'trend': 'insufficient_data',
                'message': 'Need at least 2 measurements to show trends'
            }
        
        current = self.history[-1]
        previous = self.history[-2]
        
        # Calculate changes
        score_change = current.overall_score - previous.overall_score
        lines_change = current.total_lines - previous.total_lines
        
        # Metric changes
        metric_changes = {}
        for key in current.metrics:
            if key in previous.metrics:
                metric_changes[key] = current.metrics[key] - previous.metrics[key]
        
        # Issue changes
        issue_changes = {}
        for severity in current.issues_count:
            if severity in previous.issues_count:
                issue_changes[severity] = current.issues_count[severity] - previous.issues_count[severity]
        
        # Determine trend
        if score_change > 5:
            trend = 'improving'
        elif score_change < -5:
            trend = 'degrading'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'score_change': round(score_change, 2),
            'lines_change': lines_change,
            'metric_changes': metric_changes,
            'issue_changes': issue_changes,
            'current_score': current.overall_score,
            'previous_score': previous.overall_score,
            'measurement_count': len(self.history)
        }
    
    def get_long_term_trend(self, periods: int = 10) -> Dict[str, Any]:
        """Get trend over multiple measurements"""
        if len(self.history) < periods:
            periods = len(self.history)
        
        if periods < 2:
            return {'trend': 'insufficient_data'}
        
        recent = self.history[-periods:]
        
        scores = [s.overall_score for s in recent]
        avg_score = sum(scores) / len(scores)
        
        # Calculate linear regression slope
        x_values = list(range(len(scores)))
        x_mean = sum(x_values) / len(x_values)
        y_mean = avg_score
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, scores))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        slope = numerator / denominator if denominator != 0 else 0
        
        # Determine trend
        if slope > 0.5:
            trend = 'improving'
        elif slope < -0.5:
            trend = 'degrading'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'slope': round(slope, 3),
            'average_score': round(avg_score, 2),
            'min_score': min(scores),
            'max_score': max(scores),
            'periods_analyzed': periods,
            'volatility': round(self._calculate_volatility(scores), 2)
        }
    
    def _calculate_volatility(self, scores: List[float]) -> float:
        """Calculate score volatility (standard deviation)"""
        if len(scores) < 2:
            return 0.0
        
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        return variance ** 0.5
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive quality summary"""
        if not self.history:
            return {'status': 'no_data'}
        
        current = self.history[-1]
        
        # Best and worst scores
        all_scores = [s.overall_score for s in self.history]
        best_idx = all_scores.index(max(all_scores))
        worst_idx = all_scores.index(min(all_scores))
        
        return {
            'current_score': current.overall_score,
            'best_score': all_scores[best_idx],
            'best_date': self.history[best_idx].timestamp,
            'worst_score': all_scores[worst_idx],
            'worst_date': self.history[worst_idx].timestamp,
            'total_measurements': len(self.history),
            'average_score': round(sum(all_scores) / len(all_scores), 2),
            'recent_trend': self.analyze_trend(),
            'long_term_trend': self.get_long_term_trend()
        }


class CodebaseGrowthAnalyzer:
    """
    Analyzes codebase growth patterns.
    Detects rapid growth, code churn, etc.
    """
    
    def __init__(self):
        self.snapshots = []
        
    def add_snapshot(self, 
                    files: int,
                    lines: int,
                    functions: int,
                    classes: int):
        """Add growth snapshot"""
        self.snapshots.append({
            'timestamp': datetime.now().isoformat(),
            'files': files,
            'lines': lines,
            'functions': functions,
            'classes': classes
        })
    
    def analyze_growth(self) -> Dict[str, Any]:
        """Analyze growth patterns"""
        if len(self.snapshots) < 2:
            return {'status': 'insufficient_data'}
        
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        # Growth rates
        files_growth = ((last['files'] - first['files']) / max(first['files'], 1)) * 100
        lines_growth = ((last['lines'] - first['lines']) / max(first['lines'], 1)) * 100
        
        # Average sizes
        avg_file_size = last['lines'] / max(last['files'], 1)
        avg_functions_per_file = last['functions'] / max(last['files'], 1)
        
        # Detect issues
        issues = []
        
        if lines_growth > 100:
            issues.append({
                'type': 'rapid_growth',
                'message': f'Codebase doubled in size ({lines_growth:.1f}% growth)',
                'recommendation': 'Review if all code is necessary. Consider refactoring.'
            })
        
        if avg_file_size > 500:
            issues.append({
                'type': 'large_files',
                'message': f'Average file size is {avg_file_size:.0f} lines',
                'recommendation': 'Split large files into smaller modules.'
            })
        
        return {
            'growth_metrics': {
                'files_growth': round(files_growth, 2),
                'lines_growth': round(lines_growth, 2),
                'current_size': last['lines'],
                'avg_file_size': round(avg_file_size, 0),
                'avg_functions_per_file': round(avg_functions_per_file, 1)
            },
            'issues': issues,
            'health_status': 'healthy' if not issues else 'needs_attention'
        }


if __name__ == '__main__':
    import sys
    
    # Example usage
    analyzer = QualityTrendsAnalyzer()
    
    # Simulate adding snapshot
    if len(sys.argv) > 1 and sys.argv[1] == 'add':
        analyzer.add_snapshot(
            metrics={'complexity': 45.2, 'maintainability': 78.5},
            issues={'HIGH': 3, 'MEDIUM': 12, 'LOW': 25},
            files=42,
            lines=5234,
            score=82.5
        )
        print("Snapshot added!")
    
    # Show summary
    summary = analyzer.get_summary()
    print(json.dumps(summary, indent=2))
