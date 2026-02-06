"""
Jupyter Notebook parser for extracting content and metadata.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

import nbformat
from nbformat.notebooknode import NotebookNode

from src.utils.logger import setup_logger


class NotebookParser:
    """
    Parser for Jupyter notebooks (.ipynb files).
    Extracts code, markdown, outputs, and metadata.
    """
    
    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)
    
    def parse(self, notebook_path: Path) -> Dict[str, Any]:
        """
        Parse a Jupyter notebook.
        
        Args:
            notebook_path: Path to .ipynb file
            
        Returns:
            Dictionary containing parsed notebook content
        """
        self.logger.info(f"Parsing notebook: {notebook_path}")
        
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            result = {
                "metadata": self._extract_metadata(nb),
                "cells": self._extract_cells(nb),
                "code_cells": self._extract_code_cells(nb),
                "markdown_cells": self._extract_markdown_cells(nb),
                "outputs": self._extract_outputs(nb),
                "imports": self._extract_imports(nb),
                "functions": self._extract_functions(nb),
                "statistics": self._compute_statistics(nb)
            }
            
            self.logger.info(f"Parsed {len(result['cells'])} cells from notebook")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to parse notebook: {e}")
            raise
    
    def _extract_metadata(self, nb: NotebookNode) -> Dict[str, Any]:
        """Extract notebook metadata."""
        metadata = nb.get('metadata', {})
        
        return {
            "kernelspec": metadata.get('kernelspec', {}),
            "language_info": metadata.get('language_info', {}),
            "title": metadata.get('title', ''),
            "authors": metadata.get('authors', []),
        }
    
    def _extract_cells(self, nb: NotebookNode) -> List[Dict[str, Any]]:
        """Extract all cells with their content."""
        cells = []
        
        for idx, cell in enumerate(nb.cells):
            cell_data = {
                "index": idx,
                "type": cell.cell_type,
                "source": cell.source,
                "metadata": cell.get('metadata', {})
            }
            
            if cell.cell_type == 'code':
                cell_data["outputs"] = self._parse_cell_outputs(cell)
                cell_data["execution_count"] = cell.get('execution_count')
            
            cells.append(cell_data)
        
        return cells
    
    def _extract_code_cells(self, nb: NotebookNode) -> List[Dict[str, Any]]:
        """Extract only code cells."""
        return [
            {
                "index": idx,
                "source": cell.source,
                "outputs": self._parse_cell_outputs(cell),
                "execution_count": cell.get('execution_count')
            }
            for idx, cell in enumerate(nb.cells)
            if cell.cell_type == 'code'
        ]
    
    def _extract_markdown_cells(self, nb: NotebookNode) -> List[Dict[str, Any]]:
        """Extract only markdown cells."""
        return [
            {
                "index": idx,
                "source": cell.source,
                "heading_level": self._detect_heading_level(cell.source)
            }
            for idx, cell in enumerate(nb.cells)
            if cell.cell_type == 'markdown'
        ]
    
    def _parse_cell_outputs(self, cell) -> List[Dict[str, Any]]:
        """Parse outputs from a code cell."""
        outputs = []
        
        for output in cell.get('outputs', []):
            output_data = {
                "output_type": output.get('output_type'),
            }
            
            if output.get('output_type') == 'stream':
                output_data["text"] = output.get('text', '')
            
            elif output.get('output_type') == 'execute_result':
                output_data["data"] = output.get('data', {})
                output_data["execution_count"] = output.get('execution_count')
            
            elif output.get('output_type') == 'display_data':
                output_data["data"] = output.get('data', {})
            
            elif output.get('output_type') == 'error':
                output_data["ename"] = output.get('ename')
                output_data["evalue"] = output.get('evalue')
                output_data["traceback"] = output.get('traceback', [])
            
            outputs.append(output_data)
        
        return outputs
    
    def _extract_outputs(self, nb: NotebookNode) -> Dict[str, List]:
        """Extract and categorize all outputs."""
        outputs = {
            "text": [],
            "plots": [],
            "tables": [],
            "errors": []
        }
        
        for cell in nb.cells:
            if cell.cell_type != 'code':
                continue
            
            for output in cell.get('outputs', []):
                if output.get('output_type') == 'stream':
                    outputs["text"].append(output.get('text', ''))
                
                elif output.get('output_type') in ['execute_result', 'display_data']:
                    data = output.get('data', {})
                    
                    if 'image/png' in data or 'image/jpeg' in data:
                        outputs["plots"].append(data)
                    elif 'text/html' in data:
                        outputs["tables"].append(data['text/html'])
                    elif 'text/plain' in data:
                        outputs["text"].append(data['text/plain'])
                
                elif output.get('output_type') == 'error':
                    outputs["errors"].append({
                        "name": output.get('ename'),
                        "value": output.get('evalue'),
                        "traceback": output.get('traceback', [])
                    })
        
        return outputs
    
    def _extract_imports(self, nb: NotebookNode) -> List[str]:
        """Extract import statements."""
        imports = []
        
        for cell in nb.cells:
            if cell.cell_type != 'code':
                continue
            
            lines = cell.source.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
        
        return list(set(imports))  # Remove duplicates
    
    def _extract_functions(self, nb: NotebookNode) -> List[Dict[str, Any]]:
        """Extract function definitions."""
        functions = []
        
        for cell in nb.cells:
            if cell.cell_type != 'code':
                continue
            
            lines = cell.source.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    func_name = line.split('def ')[1].split('(')[0].strip()
                    functions.append({
                        "name": func_name,
                        "definition": line.strip()
                    })
        
        return functions
    
    def _detect_heading_level(self, text: str) -> Optional[int]:
        """Detect markdown heading level."""
        text = text.strip()
        if text.startswith('#'):
            return len(text.split()[0])
        return None
    
    def _compute_statistics(self, nb: NotebookNode) -> Dict[str, int]:
        """Compute notebook statistics."""
        code_cells = [c for c in nb.cells if c.cell_type == 'code']
        markdown_cells = [c for c in nb.cells if c.cell_type == 'markdown']
        
        total_code_lines = sum(
            len(cell.source.split('\n'))
            for cell in code_cells
        )
        
        return {
            "total_cells": len(nb.cells),
            "code_cells": len(code_cells),
            "markdown_cells": len(markdown_cells),
            "total_code_lines": total_code_lines,
            "executed_cells": sum(
                1 for cell in code_cells
                if cell.get('execution_count') is not None
            )
        }
