#!/usr/bin/env python3
"""
Main entry point for the Automated Technical Report Generator.
"""

import sys
from pathlib import Path
from typing import Optional

# Add the parent directory to the path so src modules can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

import click
from rich.console import Console
from rich.panel import Panel

from src.agents.orchestrator import ReportOrchestrator
from src.utils.config import Config
from src.utils.logger import setup_logger

console = Console()
logger = setup_logger(__name__)


@click.command()
@click.option(
    "--input", "-i",
    required=True,
    type=click.Path(exists=True),
    help="Input file or directory (notebook, code, or project folder)"
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output file path (default: auto-generated)"
)
@click.option(
    "--type", "-t",
    type=click.Choice(["academic", "internship", "industry", "research"]),
    default="academic",
    help="Type of report to generate"
)
@click.option(
    "--format", "-f",
    type=click.Choice(["docx", "pdf", "markdown", "all"]),
    default="docx",
    help="Output format"
)
@click.option(
    "--title",
    type=str,
    help="Report title (auto-detected if not provided)"
)
@click.option(
    "--institution",
    type=str,
    help="Institution or organization name"
)
@click.option(
    "--include-code-snippets",
    is_flag=True,
    help="Include code snippets in the report"
)
@click.option(
    "--diagram-style",
    type=click.Choice(["minimal", "standard", "detailed"]),
    default="standard",
    help="Diagram detail level"
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Custom configuration file"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose logging"
)
def main(
    input: str,
    output: Optional[str],
    type: str,
    format: str,
    title: Optional[str],
    institution: Optional[str],
    include_code_snippets: bool,
    diagram_style: str,
    config: Optional[str],
    verbose: bool
):
    """
    Generate technical reports from Jupyter notebooks and project files.
    
    Examples:
    
        # Generate academic report from notebook
        python main.py -i notebook.ipynb -t academic -f docx
        
        # Generate internship report with custom title
        python main.py -i project/ -t internship --title "ML Internship Report"
        
        # Generate all formats
        python main.py -i notebook.ipynb -f all
    """
    
    try:
        # Display banner
        console.print(Panel.fit(
            "[bold blue]Technical Report Generator[/bold blue]\n"
            "Converting projects into documentation",
            border_style="blue"
        ))
        
        # Load configuration
        config_obj = Config.load(config) if config else Config.load_default()
        
        if verbose:
            config_obj.set_log_level("DEBUG")
        
        # Prepare generation parameters
        params = {
            "input_path": Path(input),
            "output_path": Path(output) if output else None,
            "report_type": type,
            "output_format": format,
            "title": title,
            "institution": institution,
            "include_code_snippets": include_code_snippets,
            "diagram_style": diagram_style,
        }
        
        console.print(f"\n[cyan]Input:[/cyan] {input}")
        console.print(f"[cyan]Report Type:[/cyan] {type}")
        console.print(f"[cyan]Output Format:[/cyan] {format}")
        
        # Initialize orchestrator
        with console.status("[bold green]Initializing report generation system..."):
            orchestrator = ReportOrchestrator(config_obj)
        
        # Generate report
        console.print("\n[bold yellow]Starting report generation...[/bold yellow]\n")
        
        result = orchestrator.generate_report(**params)
        
        # Display results
        if result.success:
            console.print(f"\n[bold green]Report generated successfully[/bold green]")
            console.print(f"\n[cyan]Output file(s):[/cyan]")
            for file_path in result.output_files:
                console.print(f"  {file_path}")
            
            if result.warnings:
                console.print(f"\n[yellow]Warnings:[/yellow]")
                for warning in result.warnings:
                    console.print(f"  {warning}")
                    
        else:
            console.print(f"\n[bold red]Report generation failed[/bold red]")
            console.print(f"[red]Error:[/red] {result.error}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(130)
        
    except Exception as e:
        logger.exception("Unexpected error occurred")
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        if verbose:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
