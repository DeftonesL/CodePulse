import click
import sys
import os
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.scanner import PulseScanner
from core.ai_engine import AIEngine
from core.analyzer import ComprehensiveAnalyzer
from modules.security import SecurityScanner

console = Console()

logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s'
)

@click.group()
@click.version_option(version='0.1.0')
def cli():
    pass

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--depth', default=10, help='Maximum directory depth to scan')
@click.option('--output', '-o', type=click.Path(), help='Output file for results (JSON)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def scan(project_path, depth, output, verbose):
    if verbose:
        logging.getLogger().setLevel(logging.INFO)
    
    console.print(Panel.fit(
        "[bold cyan]🔍 Starting Project Scan[/bold cyan]\n"
        f"Target: {project_path}\n"
        f"Max Depth: {depth}",
        border_style="cyan"
    ))
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning project...", total=None)
            
            scanner = PulseScanner(project_path, max_depth=depth)
            structure = scanner.scan()
            
            progress.update(task, completed=True)
        
        console.print("\n[bold green]✅ Scan Complete![/bold green]\n")
        
        table = Table(title="📊 Project Summary", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Files", str(structure.total_files))
        table.add_row("Total Lines", f"{structure.total_lines:,}")
        table.add_row("Languages", ", ".join(structure.languages.keys()))
        table.add_row("Dependencies", str(len(structure.dependency_graph)))
        
        console.print(table)
        
        if structure.languages:
            console.print("\n[bold]Language Distribution:[/bold]")
            for lang, count in sorted(structure.languages.items(), key=lambda x: x[1], reverse=True):
                console.print(f"  • {lang}: [green]{count}[/green] files")
        
        if output:
            scanner.export_json(output)
            console.print(f"\n[green]📁 Results saved to:[/green] {output}")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--api-key', envvar='ANTHROPIC_API_KEY', help='Anthropic API key')
@click.option('--model', default='claude-sonnet-4', help='AI model to use')
@click.option('--max-files', default=10, help='Maximum files to analyze')
@click.option('--output', '-o', type=click.Path(), help='Output directory for reports')
def analyze(project_path, api_key, model, max_files, output):
    console.print(Panel.fit(
        "[bold cyan]🤖 Starting AI Analysis[/bold cyan]\n"
        f"Target: {project_path}\n"
        f"Model: {model}\n"
        f"Max Files: {max_files}",
        border_style="cyan"
    ))
    
    if not api_key:
        console.print("[yellow]⚠️  No API key provided. Using mock analysis.[/yellow]")
    
    try:
        with console.status("[bold green]Scanning project structure..."):
            scanner = PulseScanner(project_path)
            structure = scanner.scan()
        
        console.print("[green]✓[/green] Scan complete\n")
        
        ai_engine = AIEngine(api_key=api_key, model=model)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Analyzing files (0/{max_files})...", total=max_files)
            
            results = []
            analyzed = 0
            
            for file_meta in structure.files:
                if analyzed >= max_files:
                    break
                
                if file_meta.language != 'Python':
                    continue
                
                file_path = os.path.join(structure.root_path, file_meta.path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                context = {
                    'imports': file_meta.imports,
                    'functions': file_meta.functions,
                    'classes': file_meta.classes,
                    'complexity': file_meta.complexity_score
                }
                
                result = ai_engine.analyze_code(code, file_meta.path, context)
                results.append(result)
                
                analyzed += 1
                progress.update(task, completed=analyzed, description=f"Analyzing files ({analyzed}/{max_files})...")
        
        console.print("\n[bold green]✅ Analysis Complete![/bold green]\n")
        
        total_issues = sum(len(r.issues) for r in results)
        avg_score = sum(r.overall_score for r in results) / len(results) if results else 0
        
        table = Table(title="📊 Analysis Summary", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Files Analyzed", str(len(results)))
        table.add_row("Average Score", f"{avg_score:.1f}/100")
        table.add_row("Total Issues", str(total_issues))
        table.add_row("Critical Issues", str(sum(1 for r in results for i in r.issues if i.severity.value == 'critical')))
        
        console.print(table)
        
        console.print("\n[bold]🔴 Top Issues:[/bold]")
        issue_count = 0
        for result in results:
            for issue in result.issues:
                if issue_count >= 5:
                    break
                console.print(f"\n  [{issue.severity.value.upper()}] {issue.title}")
                console.print(f"  📁 {result.file_path}:{issue.line_number}")
                console.print(f"  {issue.description[:100]}...")
                issue_count += 1
        
        if output:
            os.makedirs(output, exist_ok=True)
            output_file = os.path.join(output, 'analysis_results.json')
            with open(output_file, 'w') as f:
                json.dump([r.to_dict() for r in results], f, indent=2)
            console.print(f"\n[green]📁 Full results saved to:[/green] {output_file}")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for security report')
@click.option('--level', default='enterprise', type=click.Choice(['basic', 'standard', 'enterprise']))
def security(project_path, output, level):
    console.print(Panel.fit(
        "[bold red]🔒 Starting Security Audit[/bold red]\n"
        f"Target: {project_path}\n"
        f"Level: {level.upper()}",
        border_style="red"
    ))
    
    try:
        scanner = SecurityScanner()
        all_issues = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning for vulnerabilities...", total=None)
            
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        issues = scanner.scan_file(file_path)
                        all_issues.extend(issues)
            
            progress.update(task, completed=True)
        
        report = scanner.generate_report(all_issues)
        
        console.print("\n[bold green]✅ Security Scan Complete![/bold green]\n")
        
        score = report['security_score']
        if score >= 90:
            score_color = "green"
            grade = "A"
        elif score >= 80:
            score_color = "yellow"
            grade = "B"
        elif score >= 70:
            score_color = "yellow"
            grade = "C"
        else:
            score_color = "red"
            grade = "D"
        
        console.print(f"[bold]Security Score:[/bold] [{score_color}]{score}/100 (Grade: {grade})[/{score_color}]\n")
        
        table = Table(title="🚨 Security Issues", show_header=True, header_style="bold red")
        table.add_column("Severity", style="cyan")
        table.add_column("Count", style="yellow")
        
        for severity, count in report['severity_breakdown'].items():
            if count > 0:
                table.add_row(severity.upper(), str(count))
        
        console.print(table)
        
        if report['severity_breakdown']['critical'] > 0:
            console.print("\n[bold red]🔴 CRITICAL ISSUES:[/bold red]")
            for issue_dict in report['issues'][:5]:  # Show first 5
                if issue_dict['severity'] == 'critical':
                    console.print(f"\n  {issue_dict['title']}")
                    console.print(f"  📁 {issue_dict['file_path']}:{issue_dict['line_number']}")
                    console.print(f"  {issue_dict['description'][:100]}...")
        
        if output:
            with open(output, 'w') as f:
                json.dump(report, f, indent=2)
            console.print(f"\n[green]📁 Security report saved to:[/green] {output}")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--api-key', envvar='ANTHROPIC_API_KEY', help='Anthropic API key')
@click.option('--max-files', default=10, help='Maximum files to analyze with AI')
@click.option('--output', '-o', type=click.Path(), help='Output file for report (JSON)')
def comprehensive(project_path, api_key, max_files, output):
    console.print(Panel.fit(
        "[bold cyan]COMPREHENSIVE ANALYSIS[/bold cyan]\n"
        f"Target: {project_path}\n"
        f"Max AI Files: {max_files}",
        border_style="cyan"
    ))
    
    try:
        with console.status("[bold green]Initializing analyzer..."):
            analyzer = ComprehensiveAnalyzer(project_path, api_key=api_key)
        
        with console.status("[bold green]Running comprehensive analysis..."):
            report = analyzer.analyze(max_files_ai=max_files)
        
        console.print("\n[bold green]✅ Analysis Complete![/bold green]\n")
        analyzer.print_report(report)
        
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        if output:
            analyzer.export_report(report, output)
            console.print(f"\n[green]📁 Full report saved to:[/green] {output}")
        else:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(reports_dir, f"comprehensive_report_{timestamp}.json")
            analyzer.export_report(report, output_file)
            console.print(f"\n[green]📁 Full report saved to:[/green] {output_file}")
            console.print(f"[dim]Reports directory: {os.path.abspath(reports_dir)}[/dim]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--format', '-f', default='html', type=click.Choice(['html', 'pdf', 'json']))
@click.option('--output', '-o', type=click.Path(), required=True, help='Output file path')
def report(project_path, format, output):
    console.print(Panel.fit(
        "[bold cyan]📊 Generating Report[/bold cyan]\n"
        f"Target: {project_path}\n"
        f"Format: {format.upper()}",
        border_style="cyan"
    ))
    
    console.print("[yellow]⚠️  Report generation coming soon![/yellow]")
    console.print("This feature will generate beautiful HTML/PDF reports with:")
    console.print("  • Code quality metrics")
    console.print("  • Security assessment")
    console.print("  • AI recommendations")
    console.print("  • Trend analysis")

def main():
    cli()

if __name__ == '__main__':
    main()
