"""
Analyzer Agent: Extracts and analyzes context from parsed input files.
"""

from typing import Dict, Any, List
from collections import defaultdict

from src.agents.base_agent import BaseAgent
from src.llm.llm_interface import LLMInterface


class AnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing parsed input data and extracting
    relevant context for report generation.
    
    Analyzes:
    - Project structure and purpose
    - Key algorithms and methodologies
    - Data sources and processing
    - Results and findings
    - Technical complexity
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze parsed data and extract report context.
        
        Args:
            context: Contains 'parsed_data' and 'report_type'
            
        Returns:
            Dictionary with analysis results
        """
        parsed_data = context.get("parsed_data", {})
        report_type = context.get("report_type", "academic")
        
        self.logger.info("Starting analysis of parsed data")
        
        # Extract different types of information
        project_info = self._analyze_project_structure(parsed_data)
        technical_analysis = self._analyze_technical_content(parsed_data)
        data_analysis = self._analyze_data_processing(parsed_data)
        results_summary = self._summarize_results(parsed_data)
        
        # Generate comprehensive context
        analysis_context = {
            "project_info": project_info,
            "technical_analysis": technical_analysis,
            "data_analysis": data_analysis,
            "results_summary": results_summary,
            "report_type": report_type,
            "complexity_level": self._assess_complexity(technical_analysis),
            "key_findings": self._extract_key_findings(results_summary)
        }
        
        self.logger.info("Analysis complete")
        return analysis_context
    
    def _analyze_project_structure(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the overall project structure and purpose."""
        cells = parsed_data.get("cells", [])
        markdown_cells = parsed_data.get("markdown_cells", [])
        
        # Look for project description in markdown
        project_description = ""
        objectives = []
        
        for cell in markdown_cells:
            content = cell.get("source", "").lower()
            if any(keyword in content for keyword in ["project", "overview", "description", "goal"]):
                project_description = cell.get("source", "")
            if any(keyword in content for keyword in ["objective", "aim", "purpose"]):
                objectives.append(cell.get("source", ""))
        
        # Extract imports to understand libraries used
        imports = parsed_data.get("imports", [])
        libraries = list(set(imports))
        
        return {
            "description": project_description,
            "objectives": objectives,
            "libraries_used": libraries,
            "notebook_metadata": parsed_data.get("metadata", {})
        }
    
    def _analyze_technical_content(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical aspects of the code."""
        code_cells = parsed_data.get("code_cells", [])
        functions = parsed_data.get("functions", [])
        
        # Analyze code complexity
        total_lines = sum(len(cell.get("source", "").split("\n")) for cell in code_cells)
        function_count = len(functions)
        
        # Identify key algorithms (simple heuristic)
        algorithms = []
        for cell in code_cells:
            code = cell.get("source", "").lower()
            if any(keyword in code for keyword in ["algorithm", "model", "train", "predict", "classify"]):
                algorithms.append(cell.get("source", "")[:200] + "...")
        
        # Identify data processing steps
        data_processing = []
        for cell in code_cells:
            code = cell.get("source", "").lower()
            if any(keyword in code for keyword in ["load", "read", "process", "transform", "clean"]):
                data_processing.append("Data loading/processing operation")
        
        return {
            "total_code_lines": total_lines,
            "function_count": function_count,
            "algorithms_identified": algorithms,
            "data_processing_steps": len(data_processing),
            "code_cells_count": len(code_cells)
        }
    
    def _analyze_data_processing(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data sources and processing."""
        code_cells = parsed_data.get("code_cells", [])
        
        # Look for data loading patterns
        data_sources = []
        for cell in code_cells:
            code = cell.get("source", "").lower()
            if "pd.read_csv" in code or "pd.read_excel" in code:
                data_sources.append("CSV/Excel file")
            if "pd.read_sql" in code or "sql" in code:
                data_sources.append("Database")
            if "requests.get" in code or "urllib" in code:
                data_sources.append("Web API")
        
        # Look for data transformations
        transformations = []
        if any("sklearn" in str(parsed_data.get("imports", [])) for _ in code_cells):
            transformations.append("Machine Learning preprocessing")
        if any("pandas" in str(parsed_data.get("imports", [])) for _ in code_cells):
            transformations.append("Data manipulation")
        
        return {
            "data_sources": list(set(data_sources)),
            "transformations": transformations,
            "estimated_dataset_size": "Unknown"  # Could be enhanced with actual data inspection
        }
    
    def _summarize_results(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize results and outputs."""
        outputs = parsed_data.get("outputs", {})
        
        # Get categorized outputs from parser
        text_outputs = outputs.get("text", [])
        plot_outputs = outputs.get("plots", [])
        table_outputs = outputs.get("tables", [])
        error_outputs = outputs.get("errors", [])
        
        # Extract key metrics from text outputs
        metrics = []
        for output in text_outputs:
            content = str(output).lower()
            if any(keyword in content for keyword in ["accuracy", "precision", "recall", "f1", "score", "mse", "mae", "r2"]):
                metrics.append(str(output))
        
        return {
            "total_outputs": len(text_outputs) + len(plot_outputs) + len(table_outputs),
            "text_outputs": text_outputs,  # Keep full text for LLM context
            "visualizations": len(plot_outputs),
            "tables": len(table_outputs),
            "errors": len(error_outputs),
            "key_metrics": metrics  # Include actual metric text
        }
    
    def _assess_complexity(self, technical_analysis: Dict[str, Any]) -> str:
        """Assess technical complexity level."""
        lines = technical_analysis.get("total_code_lines", 0)
        functions = technical_analysis.get("function_count", 0)
        
        if lines > 500 or functions > 10:
            return "High"
        elif lines > 200 or functions > 5:
            return "Medium"
        else:
            return "Low"
    
    def _extract_key_findings(self, results_summary: Dict[str, Any]) -> List[str]:
        """Extract key findings from results."""
        findings = []
        
        if results_summary.get("visualizations", 0) > 0:
            findings.append(f"Generated {results_summary['visualizations']} visualizations")
        
        if results_summary.get("key_metrics"):
            findings.append("Performance metrics calculated")
        
        if results_summary.get("errors", 0) > 0:
            findings.append(f"Encountered {results_summary['errors']} errors during execution")
        
        return findings