"""
Report generation orchestrator that coordinates all agents.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from src.agents.analyzer_agent import AnalyzerAgent
from src.agents.writer_agent import WriterAgent
from src.agents.diagram_agent import DiagramAgent
from src.agents.citation_agent import CitationAgent
from src.parsers.notebook_parser import NotebookParser
from src.formatters.docx_formatter import DocxFormatter
from src.formatters.pdf_formatter import PdfFormatter
from src.formatters.markdown_formatter import MarkdownFormatter
from src.llm.ollama_client import OllamaClient
from src.utils.config import Config
from src.utils.logger import setup_logger, ProgressLogger


@dataclass
class GenerationResult:
    """Result of report generation."""
    success: bool
    output_files: List[Path]
    warnings: List[str]
    error: Optional[str] = None


class ReportOrchestrator:
    """
    Orchestrates the entire report generation process.
    
    Workflow:
    1. Parse input files (notebooks, code, data)
    2. Extract context using AnalyzerAgent
    3. Generate sections using WriterAgent
    4. Create diagrams using DiagramAgent
    5. Add citations using CitationAgent
    6. Format output using appropriate formatter
    """
    
    def __init__(self, config: Config):
        """
        Initialize the orchestrator.
        
        Args:
            config: System configuration
        """
        self.config = config
        self.logger = setup_logger(self.__class__.__name__)
        
        # Ensure directories exist
        config.ensure_directories()
        
        # Initialize LLM client
        self.llm = self._initialize_llm()
        
        # Initialize agents
        self.analyzer = AnalyzerAgent(self.llm, config.model_dump())
        self.writer = WriterAgent(self.llm, config.model_dump())
        self.diagram = DiagramAgent(self.llm, config.model_dump())
        self.citation = CitationAgent(self.llm, config.model_dump())
        
        # Initialize parsers
        self.notebook_parser = NotebookParser()
        
        # Initialize formatters
        self.formatters = {
            "docx": DocxFormatter(config.report.model_dump()),
            "pdf": PdfFormatter(config.report.model_dump()),
            "markdown": MarkdownFormatter(config.report.model_dump())
        }
    
    def _initialize_llm(self):
        """Initialize LLM client based on configuration."""
        llm_config = self.config.llm
        
        if llm_config.provider == "ollama":
            llm = OllamaClient(
                model=llm_config.model,
                base_url=llm_config.base_url,
                timeout=llm_config.timeout
            )
        elif llm_config.provider == "openai":
            from src.llm.openai_client import OpenAIClient
            llm = OpenAIClient(
                model=llm_config.model,
                api_key=llm_config.api_key,
                base_url=llm_config.base_url
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_config.provider}")
        
        # Check availability
        if not llm.is_available():
            self.logger.warning(f"LLM service not available: {llm_config.provider}")
        
        return llm
    
    def generate_report(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        report_type: str = "academic",
        output_format: str = "docx",
        **kwargs
    ) -> GenerationResult:
        """
        Generate a complete technical report.
        
        Args:
            input_path: Path to input file or directory
            output_path: Output file path (auto-generated if None)
            report_type: Type of report (academic, internship, industry, research)
            output_format: Output format (docx, pdf, markdown, all)
            **kwargs: Additional generation parameters
            
        Returns:
            GenerationResult with success status and output files
        """
        warnings = []
        
        try:
            # Setup progress tracking
            total_steps = 6
            progress = ProgressLogger(self.logger, total_steps)
            
            # Step 1: Parse input files
            progress.step("Parsing input files...")
            parsed_data = self._parse_inputs(input_path)
            
            # Step 2: Extract context
            progress.step("Extracting project context...")
            # Pass the first notebook's parsed data directly to analyzer
            notebook_data = parsed_data.get("notebooks", [{}])[0]
            context = self.analyzer.execute({
                "parsed_data": notebook_data,  # Pass notebook data, not the wrapper dict
                "report_type": report_type,
                **kwargs
            })
            
            # Step 3: Generate report sections
            progress.step("Generating report sections...")
            sections = self.writer.execute({
                **context,  # Spread analyzer results at top level
                "report_type": report_type,
                **kwargs
            })
            
            # Step 4: Generate diagrams
            progress.step("Creating diagrams...")
            diagrams = self.diagram.execute({
                **context,  # Spread analyzer results at top level
                "diagram_style": kwargs.get("diagram_style", "standard")
            })
            
            # Step 5: Generate citations
            progress.step("Adding citations and references...")
            citations = self.citation.execute({
                **context,  # Spread analyzer results at top level
                "sections": sections
            })
            
            # Step 6: Format output
            progress.step("Formatting final document...")
            output_files = self._format_output(
                sections=sections,
                diagrams=diagrams,
                citations=citations,
                output_path=output_path,
                output_format=output_format,
                report_type=report_type,
                **kwargs
            )
            
            progress.complete("Report generation completed successfully")
            
            return GenerationResult(
                success=True,
                output_files=output_files,
                warnings=warnings
            )
            
        except Exception as e:
            self.logger.exception("Report generation failed")
            return GenerationResult(
                success=False,
                output_files=[],
                warnings=warnings,
                error=str(e)
            )
    
    def _parse_inputs(self, input_path: Path) -> Dict[str, Any]:
        """Parse input files and extract content."""
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input path not found: {input_path}")
        
        parsed_data = {
            "notebooks": [],
            "code_files": [],
            "data_files": [],
            "markdown_files": []
        }
        
        if input_path.is_file():
            # Single file
            if input_path.suffix == ".ipynb":
                parsed_data["notebooks"].append(
                    self.notebook_parser.parse(input_path)
                )
            # Add other file type parsers here
        
        elif input_path.is_dir():
            # Directory - find all relevant files
            for ipynb_file in input_path.glob("**/*.ipynb"):
                parsed_data["notebooks"].append(
                    self.notebook_parser.parse(ipynb_file)
                )
            
            # Add code files, data files, etc.
        
        return parsed_data
    
    def _format_output(
        self,
        sections: Dict[str, str],
        diagrams: List[Dict],
        citations: List[Dict],
        output_path: Optional[Path],
        output_format: str,
        report_type: str,
        **kwargs
    ) -> List[Path]:
        """Format and save the final report."""
        
        output_files = []
        
        # Determine output path
        if output_path is None:
            title = kwargs.get("title", "technical_report")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
            safe_title = safe_title.replace(' ', '_')
            output_path = self.config.output_directory / f"{safe_title}.{output_format}"
        
        # Prepare document data
        doc_data = {
            "sections": sections,
            "diagrams": diagrams,
            "citations": citations,
            "report_type": report_type,
            "metadata": {
                "title": kwargs.get("title", "Technical Report"),
                "institution": kwargs.get("institution", ""),
                "include_code_snippets": kwargs.get("include_code_snippets", False)
            }
        }
        
        # Generate requested formats
        formats_to_generate = ["docx", "pdf", "markdown"] if output_format == "all" else [output_format]
        
        for fmt in formats_to_generate:
            formatter = self.formatters[fmt]
            output_file = output_path.with_suffix(f".{fmt}")
            
            formatter.format_report(sections, diagrams, citations, output_file)
            output_files.append(output_file)
            
            self.logger.info(f"Generated {fmt.upper()} report: {output_file}")
        
        return output_files
