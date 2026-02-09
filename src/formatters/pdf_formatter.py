"""
PDF formatter for report generation.
"""

from pathlib import Path
from typing import Dict, Any, List
import re
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak,
        Table, TableStyle, Image
    )
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

from src.formatters.base_formatter import BaseFormatter
from src.utils.diagram_renderer import DiagramRenderer


class PdfFormatter(BaseFormatter):
    """
    Formatter for PDF output format.
    
    Generates professional PDF documents with:
    - Proper typography
    - Page formatting
    - Headers and footers
    - Tables
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if not PDF_AVAILABLE:
            self.logger.warning("reportlab not available. PDF formatting will be limited.")
        self.diagram_renderer = DiagramRenderer()
        self._temp_diagram_files = []  # Track temp files for cleanup
    
    def format_report(
        self,
        sections: Dict[str, Any],
        diagrams: Dict[str, Any],
        citations: Dict[str, Any],
        output_path: Path
    ) -> Path:
        """
        Format report as PDF.
        
        Args:
            sections: Report sections
            diagrams: Generated diagrams
            citations: Citations and references
            output_path: Output file path
            
        Returns:
            Path to generated PDF file
        """
        if not PDF_AVAILABLE:
            raise ImportError("reportlab is required for PDF formatting. Install with: pip install reportlab")
        
        self.logger.info(f"Formatting report as PDF: {output_path}")
        
        output_path = self._validate_output_path(output_path)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Define custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            textColor=colors.HexColor('#003366'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=48
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            spaceBefore=18,
            spaceAfter=12,
            textColor=colors.HexColor('#003366'),
            fontName='Helvetica-Bold'
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor('#003366'),
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        )
        
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=9,
            leftIndent=20,
            spaceBefore=6,
            spaceAfter=6,
            backColor=colors.HexColor('#F5F5F5')
        )
        
        custom_styles = {
            'title': title_style,
            'subtitle': subtitle_style,
            'heading1': heading1_style,
            'heading2': heading2_style,
            'body': body_style,
            'code': code_style
        }
        
        # Build document content
        story = []
        
        # Title page
        story.extend(self._build_title_page(styles, custom_styles, sections))
        
        # Table of contents
        if self.config.get("include_table_of_contents", True):
            story.extend(self._build_table_of_contents(styles))
        
        # Sections
        story.extend(self._build_sections(styles, custom_styles, sections))
        
        # Diagrams
        if diagrams:
            story.extend(self._build_diagrams_section(styles, custom_styles, diagrams))
        
        # References
        if citations.get("references_section"):
            story.extend(self._build_references(styles, citations))
        
        # Build PDF
        doc.build(story)
        
        # Clean up temporary diagram files after PDF is built
        for temp_file in self._temp_diagram_files:
            temp_file.unlink(missing_ok=True)
        self._temp_diagram_files.clear()
        
        self.logger.info(f"PDF report saved to: {output_path}")
        return output_path
    
    def _build_title_page(self, styles, custom_styles, sections: Dict[str, Any]):
        """Build professionally formatted title page content."""
        story = []
        
        title = self.config.get("title", "Technical Report")
        
        # Add top spacing
        story.append(Spacer(1, 2*inch))
        
        # Title
        story.append(Paragraph(title, custom_styles['title']))
        story.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        story.append(Paragraph("Automated Technical Report", custom_styles['subtitle']))
        story.append(Spacer(1, 2*inch))
        
        # Generation info
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#808080'),
            alignment=TA_CENTER
        )
        story.append(Paragraph("Generated by Report Generator", info_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), info_style))
        
        story.append(PageBreak())
        
        return story
    
    def _build_table_of_contents(self, styles):
        """Build table of contents."""
        story = []
        
        story.append(Paragraph("Table of Contents", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        toc_items = [
            "Abstract",
            "Introduction",
            "Methodology", 
            "Results",
            "Discussion",
            "Conclusion",
            "References"
        ]
        
        for i, item in enumerate(toc_items, 1):
            story.append(Paragraph(f"{i}. {item}", styles['Normal']))
            story.append(Spacer(1, 6))
        
        story.append(PageBreak())
        
        return story
    
    def _build_sections(self, styles, custom_styles, sections: Dict[str, Any]):
        """Build report sections with proper formatting."""
        story = []
        
        section_order = ["abstract", "introduction", "methodology", "results", "discussion", "conclusion"]
        
        for section_name in section_order:
            if section_name in sections:
                # Section heading
                story.append(Paragraph(section_name.title(), custom_styles['heading1']))
                story.append(Spacer(1, 0.15*inch))
                
                # Section content with markdown parsing
                content = sections[section_name]
                story.extend(self._parse_markdown_content(content, styles, custom_styles))
                
                story.append(Spacer(1, 0.2*inch))
        
        return story
    
    def _build_diagrams_section(self, styles, custom_styles, diagrams: Dict[str, Any]):
        """Build diagrams section with rendered images."""
        story = []
        
        story.append(Paragraph("Diagrams", custom_styles['heading1']))
        story.append(Spacer(1, 0.15*inch))
        
        for diagram_name, diagram_content in diagrams.items():
            if diagram_name != "metadata" and diagram_content:
                # Diagram heading
                story.append(Paragraph(diagram_name.replace('_', ' ').title(), custom_styles['heading2']))
                story.append(Spacer(1, 0.1*inch))
                
                # Try to render Mermaid diagram
                if diagram_content.strip():
                    try:
                        image_path = self.diagram_renderer.render_mermaid_to_png(diagram_content)
                        if image_path and image_path.exists():
                            # Add image to PDF
                            img = Image(str(image_path), width=5*inch, height=3*inch, kind='proportional')
                            story.append(img)
                            # Track temp file for cleanup after PDF is built
                            self._temp_diagram_files.append(image_path)
                        else:
                            # Fallback to code block
                            story.append(Paragraph(diagram_content, custom_styles['code']))
                    except Exception as e:
                        self.logger.warning(f"Failed to render diagram {diagram_name}: {e}")
                        story.append(Paragraph(diagram_content, custom_styles['code']))
                
                story.append(Spacer(1, 0.2*inch))
        
        return story
    
    def _build_references(self, styles, citations: Dict[str, Any]):
        """Build references section."""
        story = []
        
        heading_style = ParagraphStyle(
            'RefHeading',
            parent=styles['Heading1'],
            fontSize=18,
            spaceBefore=18,
            spaceAfter=12,
            textColor=colors.HexColor('#003366'),
            fontName='Helvetica-Bold'
        )
        
        story.append(Paragraph("References", heading_style))
        story.append(Spacer(1, 12))
        
        references_text = citations.get("references_section", "")
        # Remove markdown formatting
        references_text = references_text.replace("# References", "").strip()
        
        # Split into lines and format
        lines = references_text.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('---'):
                story.append(Paragraph(line.strip(), styles['Normal']))
                story.append(Spacer(1, 6))
        
        return story
    
    def _parse_markdown_content(self, content: str, styles, custom_styles) -> List:
        """Parse markdown content and return list of flowables."""
        story = []
        blocks = content.split('\n\n')
        
        for block in blocks:
            if not block.strip():
                continue
            
            # Check for tables
            if '|' in block and block.count('\n') > 0:
                table_flowable = self._create_table(block)
                if table_flowable:
                    story.append(table_flowable)
                    story.append(Spacer(1, 0.15*inch))
            # Check for code blocks
            elif block.strip().startswith('```'):
                code_content = block.strip().strip('```').strip()
                # Remove language identifier
                if '\n' in code_content:
                    parts = code_content.split('\n', 1)
                    if len(parts) > 1 and not ' ' in parts[0]:
                        code_content = parts[1]
                story.append(Paragraph(code_content, custom_styles['code']))
                story.append(Spacer(1, 0.1*inch))
            # Check for headings in content
            elif block.strip().startswith('#'):
                level = len(block) - len(block.lstrip('#'))
                heading_text = block.lstrip('#').strip()
                if level <= 2:
                    story.append(Paragraph(heading_text, custom_styles['heading2']))
                else:
                    story.append(Paragraph(heading_text, styles['Heading3']))
                story.append(Spacer(1, 0.1*inch))
            # Regular paragraph
            else:
                # Process inline formatting
                formatted_text = self._format_inline_markdown(block)
                story.append(Paragraph(formatted_text, custom_styles['body']))
                story.append(Spacer(1, 0.08*inch))
        
        return story
    
    def _format_inline_markdown(self, text: str) -> str:
        """Format inline markdown (bold, italic, code)."""
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Inline code
        text = re.sub(r'`(.*?)`', r'<font name="Courier" size="10">\1</font>', text)
        return text
    
    def _create_table(self, markdown_table: str):
        """Parse markdown table and create ReportLab Table."""
        lines = [line.strip() for line in markdown_table.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return None
        
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|') if cell.strip()]
        
        # Skip separator line and get data
        data_lines = lines[2:] if len(lines) > 2 else []
        
        if not header:
            return None
        
        # Build table data
        table_data = [header]
        
        for line in data_lines:
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            # Pad with empty cells if needed
            while len(cells) < len(header):
                cells.append('')
            table_data.append(cells[:len(header)])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        return table