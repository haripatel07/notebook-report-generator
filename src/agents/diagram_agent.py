"""
Diagram Agent: Generates visualizations and diagrams for reports.
"""

from typing import Dict, Any, List
from textwrap import dedent

from src.agents.base_agent import BaseAgent
from src.llm.llm_interface import LLMInterface


class DiagramAgent(BaseAgent):
    """
    Agent responsible for generating diagrams and visualizations.
    
    Generates:
    - System architecture diagrams
    - Data flow diagrams
    - Process flowcharts
    - Results visualization
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate diagrams based on analysis context.
        
        Args:
            context: Analysis context from AnalyzerAgent
            
        Returns:
            Dictionary with generated diagrams
        """
        self.logger.info("Starting diagram generation")
        
        report_type = context.get("report_type", "academic")
        diagram_format = self.config.get("report", {}).get("diagram_format", "mermaid")
        
        diagrams = {}
        
        # Generate different types of diagrams
        diagrams["architecture"] = self._generate_architecture_diagram(context)
        diagrams["data_flow"] = self._generate_data_flow_diagram(context)
        diagrams["process_flow"] = self._generate_process_flow_diagram(context)
        
        if context.get("results_summary", {}).get("visualizations", 0) > 0:
            diagrams["results_overview"] = self._generate_results_diagram(context)
        
        # Add metadata
        diagrams["metadata"] = {
            "format": diagram_format,
            "count": len([d for d in diagrams.keys() if d != "metadata"]),
            "types": [k for k in diagrams.keys() if k != "metadata"]
        }
        
        self.logger.info(f"Generated {len(diagrams)-1} diagrams")
        return diagrams
    
    def _generate_architecture_diagram(self, context: Dict[str, Any]) -> str:
        """Generate system architecture diagram."""
        project_info = context.get("project_info", {})
        technical_analysis = context.get("technical_analysis", {})
        
        libraries = project_info.get("libraries_used", [])
        lib_text = ", ".join(libraries[:3])  # Limit to 3 for simplicity
        
        prompt = f"""
        Create a simple Mermaid flowchart (graph LR or TD) showing system architecture.
        
        Components: Data Input -> Processing ({lib_text[:50]}) -> Output
        
        Keep it minimal: 5-7 nodes max. No styling. Use simple arrows (-->).
        Example: graph TD\n    A[Input] --> B[Process]\n    B --> C[Output]
        """
        
        return self._generate_diagram("Architecture Diagram", prompt.strip())
    
    def _generate_data_flow_diagram(self, context: Dict[str, Any]) -> str:
        """Generate data flow diagram."""
        data_analysis = context.get("data_analysis", {})
        sources = data_analysis.get("data_sources", ["Data"])
        
        prompt = f"""
        Create a simple Mermaid flowchart showing data flow.
        
        Flow: {sources[0] if sources else 'Data'} -> Cleaning -> Transform -> Analysis -> Results
        
        Keep minimal: 4-6 nodes. No styling. Simple arrows (-->).
        Example: graph LR\n    A[Input] --> B[Clean] --> C[Transform] --> D[Output]
        """
        
        return self._generate_diagram("Data Flow Diagram", prompt.strip())
    
    def _generate_process_flow_diagram(self, context: Dict[str, Any]) -> str:
        """Generate process flow diagram."""
        technical_analysis = context.get("technical_analysis", {})
        code_cells = technical_analysis.get("code_cells_count", 0)
        
        prompt = f"""
        Create a simple Mermaid flowchart showing process flow.
        
        Steps: Load Data -> Process ({code_cells} steps) -> Evaluate -> Output
        
        Keep minimal: 4-6 nodes. Add one decision diamond if needed. No styling.
        Example: graph TD\n    A[Start] --> B[Process]\n    B --> C{{Valid?}}\n    C -->|Yes| D[Output]\n    C -->|No| B
        """
        
        return self._generate_diagram("Process Flow Diagram", prompt.strip())
    
    def _generate_results_diagram(self, context: Dict[str, Any]) -> str:
        """Generate results overview diagram."""
        results_summary = context.get("results_summary", {})
        visualizations = results_summary.get("visualizations", 0)
        tables = results_summary.get("tables", 0)
        
        prompt = f"""
        Create a simple Mermaid diagram showing results overview.
        
        Results: {visualizations} charts, {tables} tables
        
        Keep minimal: 3-5 nodes. Show outputs branching from main results node.
        Example: graph TD\n    A[Results] --> B[Charts: {visualizations}]\n    A --> C[Tables: {tables}]
        """
        
        return self._generate_diagram("Results Overview", prompt.strip())
    
    def _generate_diagram(self, diagram_name: str, prompt: str) -> str:
        """Generate a diagram using LLM."""
        try:
            full_prompt = f"""
            Generate ONLY valid Mermaid diagram code. No explanations.
            
            {prompt}
            
            Output format: Start with graph type (graph TD/LR), then nodes and connections.
            Use ONLY simple syntax: Node labels in [], arrows -->. NO styling, NO subgraphs.
            Keep it under 10 nodes for clarity.
            """
            
            response = self.llm.generate(
                prompt=full_prompt,
                max_tokens=400,  # Reduced for simpler diagrams
                temperature=0.3
            )
            
            # Clean up response
            response = response.strip()
            if response.startswith("```mermaid"):
                response = response.replace("```mermaid", "").replace("```", "").strip()
            elif response.startswith("```"):
                response = response.replace("```", "").strip()
            
            # Ensure it starts with graph
            if not response.startswith(("graph", "flowchart")):
                response = f"graph TD\n{response}"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to generate {diagram_name}: {e}")
            return f"graph TD\n    A[{diagram_name}]\n    B[Error: {str(e)[:30]}]\n    A --> B"