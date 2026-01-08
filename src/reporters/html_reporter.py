"""
Ultra-Modern HTML Reporter with Animations & Full Error Display
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class HTMLReporter:
    """Generate stunning animated HTML reports with complete error display"""
    
    def generate(self, results: Dict[str, Any], output_file: str = 'report.html') -> str:
        """Generate complete HTML report"""
        
        # Process data
        stats = results.get('stats', {})
        scan_results = results.get('results', [])
        
        total_files = stats.get('total_files', 0)
        total_issues = 0
        security_issues = 0
        quality_issues = 0
        
        files_data = []
        issues_list = []
        
        for item in scan_results:
            if item.get('status') == 'success':
                result = item.get('result', {})
                
                # Count issues
                sec_issues = result.get('security_issues', [])
                qual_issues = result.get('quality_issues', [])
                total_issues += len(sec_issues) + len(qual_issues)
                security_issues += len(sec_issues)
                quality_issues += len(qual_issues)
                
                # Store file data
                files_data.append({
                    'path': item.get('file', 'Unknown'),
                    'language': result.get('language', 'Unknown'),
                    'lines': result.get('code_lines', 0),
                    'functions': result.get('functions', 0),
                    'classes': result.get('classes', 0),
                    'issues': len(sec_issues) + len(qual_issues),
                    'sec_issues': sec_issues,
                    'qual_issues': qual_issues
                })
                
                # Store issues with details
                for issue in sec_issues:
                    issues_list.append({
                        'file': item.get('file'),
                        'type': 'Security',
                        'severity': 'high',
                        'description': issue,
                        'language': result.get('language', 'Unknown')
                    })
                for issue in qual_issues:
                    issues_list.append({
                        'file': item.get('file'),
                        'type': 'Quality',
                        'severity': 'medium',
                        'description': issue,
                        'language': result.get('language', 'Unknown')
                    })
        
        # Calculate quality score
        quality_score = int((1 - len([f for f in files_data if f['issues'] > 0]) / max(total_files, 1)) * 100)
        
        # Generate HTML
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        duration = stats.get('duration', 'N/A')
        
        html = self._generate_full_html(
            total_files, total_issues, security_issues, quality_issues,
            quality_score, files_data, issues_list, timestamp, duration
        )
        
        # Save
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(output_path)
    
    def _generate_full_html(self, total_files, total_issues, security_issues, 
                           quality_issues, quality_score, files_data, issues_list, 
                           timestamp, duration):
        """Generate complete HTML with all features"""
        
        issues_html = self._generate_issues_html(issues_list)
        files_html = self._generate_files_html(files_data)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodePulse Analysis Report - {timestamp}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --accent-purple: #8b5cf6;
            --accent-blue: #3b82f6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-primary);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}
        
        /* Animated Stars Background */
        .stars {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }}
        
        .star {{
            position: absolute;
            width: 2px;
            height: 2px;
            background: white;
            border-radius: 50%;
            animation: twinkle 3s ease-in-out infinite;
        }}
        
        @keyframes twinkle {{
            0%, 100% {{ opacity: 0.2; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.5); }}
        }}
        
        /* Floating particles */
        .particle {{
            position: absolute;
            width: 4px;
            height: 4px;
            background: radial-gradient(circle, rgba(139,92,246,0.8), transparent);
            border-radius: 50%;
            animation: float 8s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0) translateX(0); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(-100vh) translateX(50px); opacity: 0; }}
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }}
        
        /* Header with slide-down animation */
        .header {{
            backdrop-filter: blur(20px);
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 50px 40px;
            margin-bottom: 30px;
            text-align: center;
            animation: slideDown 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}
        
        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-50px) scale(0.9);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            animation: glow 2s ease-in-out infinite;
        }}
        
        @keyframes glow {{
            0%, 100% {{ filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }}
            50% {{ filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.8)); }}
        }}
        
        .header p {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            font-weight: 500;
        }}
        
        /* Summary Cards with staggered animation */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            backdrop-filter: blur(20px);
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: fadeInUp 0.6s ease-out backwards;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
            opacity: 0;
            transition: opacity 0.4s ease;
        }}
        
        .stat-card:hover::before {{
            opacity: 0.1;
        }}
        
        .stat-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .stat-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .stat-card:nth-child(3) {{ animation-delay: 0.3s; }}
        .stat-card:nth-child(4) {{ animation-delay: 0.4s; }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(40px) scale(0.95);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}
        
        .stat-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.4);
            border-color: var(--accent-purple);
        }}
        
        .stat-icon {{
            font-size: 2.5rem;
            margin-bottom: 15px;
            display: inline-block;
            animation: bounce 2s ease-in-out infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .stat-value {{
            font-size: 3rem;
            font-weight: 800;
            color: #fff;
            margin: 15px 0;
            position: relative;
            z-index: 1;
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }}
        
        /* Section with fade-in */
        .section {{
            backdrop-filter: blur(20px);
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 35px;
            margin-bottom: 30px;
            animation: fadeIn 1s ease-out;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; filter: blur(10px); }}
            to {{ opacity: 1; filter: blur(0); }}
        }}
        
        .section-title {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 25px;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .section-title::after {{
            content: '';
            flex: 1;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-purple), transparent);
        }}
        
        /* Issue Items with hover effect */
        .issue-item {{
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 12px;
            transition: all 0.3s ease;
            animation: slideInLeft 0.5s ease-out backwards;
        }}
        
        .issue-item:nth-child(odd) {{
            animation-delay: 0.1s;
        }}
        
        .issue-item:nth-child(even) {{
            animation-delay: 0.2s;
        }}
        
        @keyframes slideInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        .issue-item:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--danger);
            transform: translateX(5px);
            box-shadow: -5px 0 20px rgba(239, 68, 68, 0.2);
        }}
        
        .issue-type {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-right: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .issue-security {{
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        
        .issue-quality {{
            background: rgba(245, 158, 11, 0.2);
            color: #fcd34d;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        
        .issue-file {{
            font-family: 'Monaco', 'Consolas', monospace;
            color: var(--accent-blue);
            font-weight: 600;
            font-size: 0.95rem;
        }}
        
        .issue-description {{
            margin-top: 12px;
            color: var(--text-secondary);
            line-height: 1.6;
            padding-left: 20px;
            border-left: 3px solid rgba(139, 92, 246, 0.3);
        }}
        
        /* Table */
        .table-wrapper {{
            overflow-x: auto;
            border-radius: 16px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th {{
            background: rgba(255, 255, 255, 0.05);
            padding: 18px;
            text-align: left;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border-bottom: 2px solid var(--glass-border);
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        td {{
            padding: 18px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        tr {{
            transition: all 0.3s ease;
        }}
        
        tr:hover {{
            background: rgba(255, 255, 255, 0.05);
            transform: scale(1.01);
        }}
        
        .file-path {{
            font-family: 'Monaco', 'Consolas', monospace;
            color: var(--accent-blue);
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        .language-badge {{
            display: inline-block;
            padding: 4px 12px;
            background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(59,130,246,0.2));
            border: 1px solid rgba(139,92,246,0.3);
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 700;
        }}
        
        .badge-success {{
            background: rgba(16, 185, 129, 0.2);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}
        
        .badge-warning {{
            background: rgba(245, 158, 11, 0.2);
            color: #fcd34d;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        
        .badge-danger {{
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: currentColor;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 currentColor; }}
            50% {{ opacity: 0.8; box-shadow: 0 0 0 4px rgba(255,255,255,0.1); }}
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            font-size: 0.95rem;
            animation: fadeIn 1.5s ease-out;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }}
        
        .footer-links a {{
            color: var(--accent-purple);
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 600;
        }}
        
        .footer-links a:hover {{
            color: var(--accent-blue);
            text-shadow: 0 0 10px currentColor;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2rem; }}
            .summary-grid {{ grid-template-columns: 1fr; }}
            .stat-card {{ padding: 20px; }}
        }}
        
        /* Scroll animations */
        .scroll-reveal {{
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease-out;
        }}
        
        .scroll-reveal.active {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <!-- Animated Background -->
    <div class="stars" id="stars"></div>
    <div class="stars" id="particles"></div>
    
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>⚡ CodePulse Analysis Report</h1>
            <p>📅 Generated: {timestamp} • ⏱️ Duration: {duration} • 📌 v0.10.1</p>
        </div>
        
        <!-- Summary Cards -->
        <div class="summary-grid">
            <div class="stat-card">
                <div class="stat-icon">📁</div>
                <div class="stat-value">{total_files}</div>
                <div class="stat-label">Total Files</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🐛</div>
                <div class="stat-value">{total_issues}</div>
                <div class="stat-label">Total Issues</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🔒</div>
                <div class="stat-value">{security_issues}</div>
                <div class="stat-label">Security Issues</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-value">{quality_score}%</div>
                <div class="stat-label">Quality Score</div>
            </div>
        </div>
        
        <!-- Issues Section -->
        {issues_html}
        
        <!-- Files Table -->
        <div class="section scroll-reveal">
            <h2 class="section-title">📂 Files Analysis</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>File</th>
                            <th>Language</th>
                            <th style="text-align: center;">Lines</th>
                            <th style="text-align: center;">Functions</th>
                            <th style="text-align: center;">Classes</th>
                            <th style="text-align: center;">Issues</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {files_html}
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>⚡ CodePulse</strong> - Professional Code Intelligence</p>
            <div class="footer-links">
                <a href="https://github.com/DeftonesL/CodePulse" target="_blank">💻 GitHub</a>
                <a href="https://github.com/DeftonesL/CodePulse/issues" target="_blank">🐛 Report Issue</a>
                <a href="https://github.com/DeftonesL/CodePulse#readme" target="_blank">📚 Documentation</a>
            </div>
            <p style="margin-top: 20px; opacity: 0.8;">Made with ❤️ by <strong>Saleh Almqati</strong></p>
        </div>
    </div>
    
    <script>
        // Generate animated stars
        const starsContainer = document.getElementById('stars');
        for (let i = 0; i < 150; i++) {{
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animationDelay = Math.random() * 3 + 's';
            star.style.animationDuration = (2 + Math.random() * 2) + 's';
            starsContainer.appendChild(star);
        }}
        
        // Generate floating particles
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 20; i++) {{
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 8 + 's';
            particle.style.animationDuration = (6 + Math.random() * 4) + 's';
            particlesContainer.appendChild(particle);
        }}
        
        // Scroll reveal animation
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('active');
                }}
            }});
        }}, observerOptions);
        
        document.querySelectorAll('.scroll-reveal').forEach(el => {{
            observer.observe(el);
        }});
        
        // Add smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});
    </script>
</body>
</html>'''
    
    def _generate_issues_html(self, issues_list):
        """Generate enhanced issues section"""
        if not issues_list:
            return '<div class="section scroll-reveal"><h2 class="section-title">✅ No Issues Found</h2><p style="color: var(--text-secondary); font-size: 1.1rem;">Great job! Your code is clean and secure.</p></div>'
        
        items_html = ''
        display_count = min(len(issues_list), 50)  # Show first 50
        
        for idx, issue in enumerate(issues_list[:display_count]):
            issue_type = issue['type']
            badge_class = 'issue-security' if issue_type == 'Security' else 'issue-quality'
            file_name = Path(issue['file']).name
            
            items_html += f'''
            <div class="issue-item">
                <div>
                    <span class="issue-type {badge_class}">{issue_type}</span>
                    <span class="issue-file">{file_name}</span>
                </div>
                <div class="issue-description">{issue['description']}</div>
            </div>
            '''
        
        more_text = f'<p style="margin-top: 20px; padding: 15px; background: rgba(245,158,11,0.1); border-radius: 12px; text-align: center; color: var(--warning);"><strong>⚠️ {len(issues_list) - 50} more issues not displayed</strong> - Check full report for details</p>' if len(issues_list) > 50 else ''
        
        return f'''
        <div class="section scroll-reveal">
            <h2 class="section-title">🐛 Issues Found ({len(issues_list)})</h2>
            {items_html}
            {more_text}
        </div>
        '''
    
    def _generate_files_html(self, files_data):
        """Generate files table rows"""
        rows = ''
        for f in files_data:
            issues = f['issues']
            if issues == 0:
                status = '<span class="badge badge-success"><span class="status-dot"></span> Clean</span>'
            elif issues <= 2:
                status = f'<span class="badge badge-warning"><span class="status-dot"></span> {issues} Issues</span>'
            else:
                status = f'<span class="badge badge-danger"><span class="status-dot"></span> {issues} Issues</span>'
            
            file_name = Path(f['path']).name
            functions = f.get('functions', 0) or '-'
            classes = f.get('classes', 0) or '-'
            
            rows += f'''
            <tr>
                <td><span class="file-path">{file_name}</span></td>
                <td><span class="language-badge">{f['language']}</span></td>
                <td style="text-align: center;">{f['lines']:,}</td>
                <td style="text-align: center;">{functions}</td>
                <td style="text-align: center;">{classes}</td>
                <td style="text-align: center;">{issues}</td>
                <td>{status}</td>
            </tr>
            '''
        
        return rows
