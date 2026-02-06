"""
Citation Agent: Generates references and citations for reports.
"""

from typing import Dict, Any, List
from datetime import datetime
from textwrap import dedent

from src.agents.base_agent import BaseAgent
from src.llm.llm_interface import LLMInterface


class CitationAgent(BaseAgent):
    """
    Agent responsible for generating citations and references.
    
    Generates:
    - Library citations
    - Methodology references
    - Tool citations
    - Academic references
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate citations and references based on context.
        
        Args:
            context: Analysis context with libraries and methods used
            
        Returns:
            Dictionary with citations and references
        """
        self.logger.info("Starting citation generation")
        
        project_info = context.get("project_info", {})
        technical_analysis = context.get("technical_analysis", {})
        report_type = context.get("report_type", "academic")
        
        citations = {}
        
        # Generate different types of citations
        citations["libraries"] = self._generate_library_citations(project_info.get("libraries_used", []))
        citations["methodology"] = self._generate_methodology_citations(technical_analysis)
        citations["tools"] = self._generate_tool_citations()
        
        # Generate references section
        citations["references_section"] = self._generate_references_section(citations)
        
        # Add inline citations for sections
        citations["inline_citations"] = self._generate_inline_citations(context)
        
        # Add metadata
        citations["metadata"] = {
            "citation_style": self.config.get("report", {}).get("citation_style", "ieee"),
            "total_references": len(citations.get("libraries", [])) + len(citations.get("methodology", [])) + len(citations.get("tools", [])),
            "report_type": report_type
        }
        
        self.logger.info(f"Generated {citations['metadata']['total_references']} references")
        return citations
    
    def _generate_library_citations(self, libraries: List[str]) -> List[Dict[str, str]]:
        """Generate citations for libraries used."""
        citations = []
        
        # Filter to only major libraries (no individual imports like "from sklearn.model_selection import train_test_split")
        major_libs = set()
        for lib in libraries:
            # Extract base library name
            if lib.startswith('from '):
                parts = lib.split()
                if len(parts) >= 2:
                    base_lib = parts[1].split('.')[0]  # Get sklearn from sklearn.metrics
                    major_libs.add(base_lib)
            elif lib.startswith('import '):
                base_lib = lib.replace('import ', '').split('.')[0].split(' as ')[0].strip()
                major_libs.add(base_lib)
            else:
                major_libs.add(lib.split('.')[0])
        
        # Map common names
        lib_mapping = {
            'sklearn': 'scikit-learn',
            'pd': 'pandas',
            'np': 'numpy',
            'plt': 'matplotlib',
            'sns': 'seaborn'
        }
        
        # Filter out built-in/trivial libraries
        exclude_libs = {'warnings', 'os', 'sys', 'json', 'csv', 're', 'time', 'datetime', 'collections'}
        
        major_libs = {lib_mapping.get(lib, lib) for lib in major_libs if lib not in exclude_libs}
        
        library_info = {
            "pandas": {
                "authors": "The pandas development team",
                "title": "pandas-dev/pandas: Powerful data structures for data analysis, time series, and statistics",
                "year": "2023",
                "url": "https://github.com/pandas-dev/pandas"
            },
            "numpy": {
                "authors": "Harris, C. R., Millman, K. J., van der Walt, S. J., et al.",
                "title": "Array programming with NumPy",
                "year": "2020",
                "journal": "Nature",
                "volume": "585",
                "pages": "357-362"
            },
            "matplotlib": {
                "authors": "Hunter, J. D.",
                "title": "Matplotlib: A 2D graphics environment",
                "year": "2007",
                "journal": "Computing in Science & Engineering",
                "volume": "9",
                "pages": "90-95"
            },
            "seaborn": {
                "authors": "Waskom, M. L.",
                "title": "seaborn: statistical data visualization",
                "year": "2021",
                "journal": "Journal of Open Research Software",
                "volume": "6",
                "pages": "1-3"
            },
            "scikit-learn": {
                "authors": "Pedregosa, F., Varoquaux, G., Gramfort, A., et al.",
                "title": "Scikit-learn: Machine Learning in Python",
                "year": "2011",
                "journal": "Journal of Machine Learning Research",
                "volume": "12",
                "pages": "2825-2830"
            },
            "tensorflow": {
                "authors": "Abadi, M., Agarwal, A., Barham, P., et al.",
                "title": "TensorFlow: Large-scale machine learning on heterogeneous systems",
                "year": "2015",
                "url": "https://www.tensorflow.org/"
            },
            "pytorch": {
                "authors": "Paszke, A., Gross, S., Massa, F., et al.",
                "title": "PyTorch: An Imperative Style, High-Performance Deep Learning Library",
                "year": "2019",
                "journal": "Advances in Neural Information Processing Systems",
                "volume": "32"
            },
            "jupyter": {
                "authors": "Kluyver, T., Ragan-Kelley, B., Pérez, F., et al.",
                "title": "Jupyter Notebooks - a publishing format for reproducible computational workflows",
                "year": "2016",
                "journal": "Positioning and Power in Academic Publishing: Players, Agents and Agendas",
                "pages": "87-90"
            },
            "xgboost": {
                "authors": "Chen, T., & Guestrin, C.",
                "title": "XGBoost: A Scalable Tree Boosting System",
                "year": "2016",
                "journal": "Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining",
                "pages": "785-794"
            },
            "lightgbm": {
                "authors": "Ke, G., Meng, Q., Finley, T., et al.",
                "title": "LightGBM: A Highly Efficient Gradient Boosting Decision Tree",
                "year": "2017",
                "journal": "Advances in Neural Information Processing Systems",
                "volume": "30"
            }
        }
        
        for lib in sorted(major_libs):
            lib_lower = lib.lower()
            if lib_lower in library_info:
                info = library_info[lib_lower]
                citation = {
                    "library": lib,
                    "citation": self._format_citation(info),
                    "bibtex": self._generate_bibtex(lib, info)
                }
                citations.append(citation)
            else:
                # Generic citation for unknown libraries
                citation = {
                    "library": lib,
                    "citation": f"{lib} development team. ({datetime.now().year}). {lib}: Python library. Retrieved from library documentation.",
                    "bibtex": f"@misc{{{lib.lower()},\n  title={{{lib}}},\n  author={{{lib} development team}},\n  year={{{datetime.now().year}}}\n}}"
                }
                citations.append(citation)
        
        return citations
    
    def _generate_methodology_citations(self, technical_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate citations for methodologies used."""
        citations = []
        
        # Add general methodology citations
        if technical_analysis.get("function_count", 0) > 0:
            citations.append({
                "method": "Custom Algorithm Implementation",
                "citation": "Project-specific algorithms implemented in Python",
                "bibtex": "@misc{custom_algorithms,\n  title={Custom Algorithm Implementation},\n  author={Project Author},\n  year={2024},\n  note={Project-specific implementation}\n}"
            })
        
        if technical_analysis.get("data_processing_steps", 0) > 0:
            citations.append({
                "method": "Data Processing Pipeline",
                "citation": "Standard data preprocessing and cleaning techniques applied",
                "bibtex": "@misc{data_processing,\n  title={Data Processing Pipeline},\n  author={Project Author},\n  year={2024},\n  note={Custom data processing implementation}\n}"
            })
        
        return citations
    
    def _generate_tool_citations(self) -> List[Dict[str, str]]:
        """Generate citations for tools and frameworks."""
        tools = [
            {
                "name": "Python",
                "citation": "Van Rossum, G. & Drake, F. L. (2009). Python 3 Reference Manual. CreateSpace.",
                "bibtex": "@book{python,\n  title={Python 3 Reference Manual},\n  author={Van Rossum, G. and Drake, F. L.},\n  year={2009},\n  publisher={CreateSpace}\n}"
            },
            {
                "name": "Jupyter Notebook",
                "citation": "Kluyver, T., Ragan-Kelley, B., Pérez, F., Granger, B., Bussonnier, M., Frederic, J., ... & IPython development team. (2016). Jupyter Notebooks—a publishing format for reproducible computational workflows. In Positioning and Power in Academic Publishing: Players, Agents and Agendas (pp. 87-90).",
                "bibtex": "@inproceedings{jupyter,\n  title={Jupyter Notebooks---a publishing format for reproducible computational workflows},\n  author={Kluyver, T and Ragan-Kelley, B and P{\'e}rez, F and Granger, B and Bussonnier, M and Frederic, J and Kelley, K and Hamrick, J and Grout, J and Corlay, S and others},\n  booktitle={Positioning and Power in Academic Publishing: Players, Agents and Agendas},\n  pages={87--90},\n  year={2016}\n}"
            }
        ]
        
        return tools
    
    def _generate_references_section(self, citations: Dict[str, Any]) -> str:
        """Generate formatted references section."""
        style = self.config.get("report", {}).get("citation_style", "ieee")
        
        references = []
        
        # Collect all citations
        for category in ["libraries", "methodology", "tools"]:
            for item in citations.get(category, []):
                if style.lower() == "ieee":
                    references.append(item.get("citation", ""))
                else:  # APA style
                    references.append(item.get("citation", ""))
        
        # Format as numbered list
        formatted_refs = "\n".join(f"{i+1}. {ref}" for i, ref in enumerate(references))
        
        return f"""# References

{formatted_refs}

---
*Citation Style: {style.upper()}*
"""
    
    def _generate_inline_citations(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Generate inline citations for different sections."""
        return {
            "methodology": "[1]-[3]",  # Libraries used
            "results": "[4]-[5]",     # Methodology citations
            "tools": "[6]-[7]"       # Tool citations
        }
    
    def _format_citation(self, info: Dict[str, str]) -> str:
        """Format citation based on available information."""
        authors = info.get("authors", "")
        title = info.get("title", "")
        year = info.get("year", "")
        
        citation = f"{authors} ({year}). {title}."
        
        if "journal" in info:
            citation += f" {info['journal']}"
            if "volume" in info:
                citation += f", {info['volume']}"
            if "pages" in info:
                citation += f", {info['pages']}"
            citation += "."
        
        if "url" in info:
            citation += f" Retrieved from {info['url']}"
        
        return citation
    
    def _generate_bibtex(self, key: str, info: Dict[str, str]) -> str:
        """Generate BibTeX entry."""
        bibtex = f"@article{{{key.lower()},\n"
        bibtex += f"  title={{{info.get('title', '')}}},\n"
        bibtex += f"  author={{{info.get('authors', '')}}},\n"
        bibtex += f"  year={{{info.get('year', '')}}}"
        
        if "journal" in info:
            bibtex += f",\n  journal={{{info['journal']}}}"
        if "volume" in info:
            bibtex += f",\n  volume={{{info['volume']}}}"
        if "pages" in info:
            bibtex += f",\n  pages={{{info['pages']}}}"
        if "url" in info:
            bibtex += f",\n  url={{{info['url']}}}"
        
        bibtex += "\n}"
        return bibtex