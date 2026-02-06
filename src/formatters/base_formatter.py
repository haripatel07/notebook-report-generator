"""
Base formatter class for report output formats.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path

from src.utils.logger import setup_logger


class BaseFormatter(ABC):
    """
    Abstract base class for report formatters.
    
    Each formatter handles a specific output format:
    - DocxFormatter: Microsoft Word documents
    - PdfFormatter: PDF documents
    - MarkdownFormatter: Markdown files
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the formatter.
        
        Args:
            config: Formatter-specific configuration
        """
        self.config = config
        self.logger = setup_logger(self.__class__.__name__)
    
    @abstractmethod
    def format_report(
        self,
        sections: Dict[str, Any],
        diagrams: Dict[str, Any],
        citations: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """
        Format and save the complete report.
        
        Args:
            sections: Generated report sections
            diagrams: Generated diagrams
            citations: Generated citations
            output_path: Path to save the formatted report
            
        Returns:
            Path to the generated file
        """
        pass
    
    def _prepare_content(self, sections: Dict[str, Any]) -> str:
        """Prepare content for formatting."""
        content_parts = []
        
        # Add title
        title = self.config.get("title", "Technical Report")
        content_parts.append(f"# {title}\n")
        
        # Add sections in order
        section_order = ["abstract", "introduction", "methodology", "results", "discussion", "conclusion"]
        
        for section_name in section_order:
            if section_name in sections:
                content_parts.append(f"## {section_name.title()}\n")
                content_parts.append(sections[section_name])
                content_parts.append("\n---\n")
        
        # Add references if available
        if "references_section" in sections.get("citations", {}):
            content_parts.append(sections["citations"]["references_section"])
        
        return "\n".join(content_parts)
    
    def _validate_output_path(self, output_path: Path) -> Path:
        """Validate and prepare output path."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path