"""
Markdown formatter for report generation.
"""

from pathlib import Path
from typing import Dict, Any

from src.formatters.base_formatter import BaseFormatter


class MarkdownFormatter(BaseFormatter):
    """
    Formatter for Markdown output format.
    
    Generates clean, readable Markdown files with:
    - Proper headings
    - Code blocks
    - Tables
    - Links
    """

    def format_report(
        self,
        sections: Dict[str, Any],
        diagrams: Dict[str, Any],
        citations: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """
        Format report as Markdown.
        
        Args:
            sections: Report sections
            diagrams: Generated diagrams
            citations: Citations and references
            output_path: Output file path
            
        Returns:
            Path to generated Markdown file
        """
        self.logger.info(f"Formatting report as Markdown: {output_path}")
        
        output_path = self._validate_output_path(output_path)
        
        # Prepare content
        content = self._prepare_markdown_content(sections, diagrams, citations)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Markdown report saved to: {output_path}")
        return output_path
    
    def _prepare_markdown_content(
        self,
        sections: Dict[str, Any],
        diagrams: Dict[str, Any],
        citations: Dict[str, Any]
    ) -> str:
        """Prepare the complete Markdown content."""
        content_parts = []
        
        # Add title and metadata
        title = self.config.get("title", "Technical Report")
        content_parts.append(f"# {title}\n")
        
        # Add generation info
        content_parts.append("*Generated automatically by Report Generator*\n")
        content_parts.append("---\n")
        
        # Add table of contents
        if self.config.get("include_table_of_contents", True):
            content_parts.append(self._generate_table_of_contents(sections))
            content_parts.append("---\n")
        
        # Add sections
        section_order = ["abstract", "introduction", "methodology", "results", "discussion", "conclusion"]
        
        for section_name in section_order:
            if section_name in sections:
                content_parts.append(f"## {section_name.title()}\n")
                content_parts.append(sections[section_name])
                content_parts.append("\n")
                
                # Add diagrams after relevant sections
                if section_name == "methodology" and diagrams:
                    content_parts.append(self._format_diagrams(diagrams))
                
                content_parts.append("---\n")
        
        # Add references
        if citations.get("references_section"):
            content_parts.append(citations["references_section"])
        
        # Add appendix if configured
        if self.config.get("include_appendix", False):
            content_parts.append(self._generate_appendix(sections, diagrams))
        
        return "\n".join(content_parts)
    
    def _generate_table_of_contents(self, sections: Dict[str, Any]) -> str:
        """Generate table of contents."""
        toc_items = []
        
        section_order = ["abstract", "introduction", "methodology", "results", "discussion", "conclusion"]
        
        for section in section_order:
            if section in sections:
                toc_items.append(f"- [{section.title()}](#{section})")
        
        toc_items.append("- [References](#references)")
        
        return "## Table of Contents\n\n" + "\n".join(toc_items) + "\n"
    
    def _format_diagrams(self, diagrams: Dict[str, Any]) -> str:
        """Format diagrams for Markdown."""
        if not diagrams or "metadata" not in diagrams:
            return ""
        
        diagram_parts = ["## Diagrams\n"]
        
        for diagram_name, diagram_content in diagrams.items():
            if diagram_name != "metadata" and diagram_content:
                diagram_parts.append(f"### {diagram_name.replace('_', ' ').title()}\n")
                # Wrap in mermaid code blocks for proper rendering
                diagram_parts.append("```mermaid")
                diagram_parts.append(diagram_content)
                diagram_parts.append("```\n")
        
        return "\n".join(diagram_parts) + "\n"
    
    def _generate_appendix(self, sections: Dict[str, Any], diagrams: Dict[str, Any]) -> str:
        """Generate appendix section."""
        appendix = ["## Appendix\n"]
        
        # Add metadata
        if "metadata" in sections:
            appendix.append("### Report Metadata\n")
            metadata = sections["metadata"]
            appendix.append(f"- Report Type: {metadata.get('report_type', 'Unknown')}\n")
            appendix.append(f"- Complexity Level: {metadata.get('complexity_level', 'Unknown')}\n")
            appendix.append(f"- Generated Sections: {', '.join(metadata.get('generated_sections', []))}\n")
        
        # Add diagram metadata
        if diagrams and "metadata" in diagrams:
            diagram_meta = diagrams["metadata"]
            appendix.append("### Diagram Information\n")
            appendix.append(f"- Format: {diagram_meta.get('format', 'Unknown')}\n")
            appendix.append(f"- Number of Diagrams: {diagram_meta.get('count', 0)}\n")
            appendix.append(f"- Types: {', '.join(diagram_meta.get('types', []))}\n")
        
        return "\n".join(appendix)