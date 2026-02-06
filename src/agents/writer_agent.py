"""
Writer Agent: Generates comprehensive report sections using LLM.
"""

from typing import Dict, Any, List
from textwrap import dedent

from src.agents.base_agent import BaseAgent
from src.llm.llm_interface import LLMInterface


class WriterAgent(BaseAgent):
    """
    Agent responsible for generating report sections using LLM.
    
    Generates:
    - Abstract/Summary
    - Introduction
    - Methodology
    - Results
    - Discussion
    - Conclusion
    """

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate report sections based on analysis context.
        
        Args:
            context: Analysis context from AnalyzerAgent
            
        Returns:
            Dictionary with generated sections
        """
        self.logger.info("Starting report section generation")
        
        report_type = context.get("report_type", "academic")
        
        # Generate each section
        sections = {}
        
        sections["abstract"] = self._generate_abstract(context)
        sections["introduction"] = self._generate_introduction(context)
        sections["methodology"] = self._generate_methodology(context)
        sections["results"] = self._generate_results(context)
        sections["discussion"] = self._generate_discussion(context)
        sections["conclusion"] = self._generate_conclusion(context)
        
        # Add metadata
        sections["metadata"] = {
            "report_type": report_type,
            "generated_sections": list(sections.keys()),
            "complexity_level": context.get("complexity_level", "Medium")
        }
        
        self.logger.info(f"Generated {len(sections)} report sections")
        return sections
    
    def _generate_abstract(self, context: Dict[str, Any]) -> str:
        """Generate abstract/summary section."""
        project_info = context.get("project_info", {})
        technical_analysis = context.get("technical_analysis", {})
        results_summary = context.get("results_summary", {})
        
        prompt = f"""
        Write a concise abstract (100-120 words max) for a technical report.
        
        Project: {project_info.get('description', 'Data analysis project')[:100]}
        
        Key Details:
        - {technical_analysis.get('total_code_lines', 0)} lines of code, {technical_analysis.get('function_count', 0)} functions
        - {len(project_info.get('libraries_used', []))} libraries: {', '.join(project_info.get('libraries_used', [])[:5])}
        - {results_summary.get('visualizations', 0)} visualizations
        
        Be concise and focus only on: objective, methods, and main results.
        """
        
        return self._generate_section("Abstract", prompt.strip(), max_tokens=200)
    
    def _generate_introduction(self, context: Dict[str, Any]) -> str:
        """Generate introduction section."""
        project_info = context.get("project_info", {})
        data_analysis = context.get("data_analysis", {})
        
        prompt = f"""
        Write a brief introduction (150-200 words).
        
        Project: {project_info.get('description', 'Data analysis project')[:150]}
        Data: {', '.join(data_analysis.get('data_sources', ['CSV/Excel'])[:3])}
        Tech: {len(project_info.get('libraries_used', []))} libraries, {context.get('technical_analysis', {}).get('function_count', 0)} functions
        
        Include: context, objectives, scope. Be concise.
        """
        
        return self._generate_section("Introduction", prompt.strip(), max_tokens=300)
    
    def _generate_methodology(self, context: Dict[str, Any]) -> str:
        """Generate methodology section."""
        technical_analysis = context.get("technical_analysis", {})
        data_analysis = context.get("data_analysis", {})
        
        algorithms = technical_analysis.get('algorithms_identified', [])
        
        prompt = f"""
        Write a concise methodology (200-250 words).
        
        Implementation:
        - {technical_analysis.get('total_code_lines', 0)} LOC, {technical_analysis.get('code_cells_count', 0)} cells
        - {technical_analysis.get('function_count', 0)} functions
        - Key algorithms: {', '.join(alg.split('(')[0] for alg in algorithms[:5])}
        
        Data: {', '.join(data_analysis.get('data_sources', [])[:3])}
        Tools: {', '.join(context.get('project_info', {}).get('libraries_used', [])[:8])}
        
        Focus on: approach, tools, key steps. Be direct and technical.
        """
        
        return self._generate_section("Methodology", prompt.strip(), max_tokens=400)
    
    def _generate_results(self, context: Dict[str, Any]) -> str:
        """Generate results section with metrics table."""
        results_summary = context.get("results_summary", {})
        text_outputs = results_summary.get('text_outputs', [])
        
        # Create metrics table
        results_parts = []
        
        # Add summary
        summary_prompt = f"""
        Write a brief results summary (80-100 words).
        
        Outputs: {results_summary.get('total_outputs', 0)} total, {results_summary.get('visualizations', 0)} visualizations, {results_summary.get('tables', 0)} tables
        Errors: {results_summary.get('errors', 0)}
        
        Be concise. Present key findings objectively.
        """
        
        summary = self._generate_section("Results Summary", summary_prompt.strip(), max_tokens=150)
        results_parts.append(summary)
        
        # Parse and add metrics table from outputs
        metrics_table = self._parse_metrics_from_outputs(text_outputs)
        if metrics_table:
            results_parts.append("\n### Performance Metrics\n")
            results_parts.append(metrics_table)
        
        return "\n".join(results_parts)
    
    def _parse_metrics_from_outputs(self, text_outputs: List) -> str:
        """Parse model performance metrics from text outputs."""
        import re
        
        models = {}
        current_model = None
        
        # Combine all text outputs into one string for parsing
        full_text = "\n".join(str(output) for output in text_outputs)
        
        # Look for model names and their metrics
        lines = full_text.split('\n')
        for line in lines:
            # Check for model names
            if 'Model:' in line or 'Regressor' in line or 'Classifier' in line:
                # Extract model name
                model_match = re.search(r'(?:Model:\s*)?([A-Za-z\s]+(?:Regressor|Classifier|Forest|Boost|XGB|LGBM|Linear))', line)
                if model_match:
                    current_model = model_match.group(1).strip()
                    if current_model not in models:
                        models[current_model] = {}
            
            # Extract metrics
            if current_model:
                # MSE
                mse_match = re.search(r'MSE[:\s]+([0-9.]+)', line, re.IGNORECASE)
                if mse_match:
                    models[current_model]['MSE'] = f"{float(mse_match.group(1)):.2f}"
                
                # MAE
                mae_match = re.search(r'MAE[:\s]+([0-9.]+)', line, re.IGNORECASE)
                if mae_match:
                    models[current_model]['MAE'] = f"{float(mae_match.group(1)):.2f}"
                
                # R2 Score
                r2_match = re.search(r'R2[\s_]Score[:\s]+([0-9.\-]+)', line, re.IGNORECASE)
                if r2_match:
                    models[current_model]['R2'] = f"{float(r2_match.group(1)):.4f}"
                
                # Accuracy
                acc_match = re.search(r'Accuracy[:\s]+([0-9.]+)', line, re.IGNORECASE)
                if acc_match:
                    models[current_model]['Accuracy'] = f"{float(acc_match.group(1)):.4f}"
        
        # Build table if we found models
        if not models:
            return ""
        
        # Determine which metrics are present
        all_metrics = set()
        for model_metrics in models.values():
            all_metrics.update(model_metrics.keys())
        
        if not all_metrics:
            return ""
        
        # Build table header
        metric_cols = sorted(all_metrics)
        table_lines = []
        table_lines.append("| Model | " + " | ".join(metric_cols) + " |")
        table_lines.append("|-------" + "|-------" * len(metric_cols) + "|")
        
        # Build table rows
        for model_name, metrics in models.items():
            row = f"| {model_name} |"  
            for metric in metric_cols:
                row += f" {metrics.get(metric, '-')} |"  
            table_lines.append(row)
        
        return "\n".join(table_lines)
    
    def _generate_discussion(self, context: Dict[str, Any]) -> str:
        """Generate discussion section."""
        technical_analysis = context.get("technical_analysis", {})
        results_summary = context.get("results_summary", {})
        
        prompt = f"""
        Write a concise discussion (150-180 words).
        
        Results: {results_summary.get('visualizations', 0)} visualizations, {results_summary.get('total_outputs', 0)} outputs
        Findings: {', '.join(context.get('key_findings', [])[:3])}
        
        Cover: significance, limitations, improvements. Be analytical but brief.
        """
        
        return self._generate_section("Discussion", prompt.strip(), max_tokens=300)
    
    def _generate_conclusion(self, context: Dict[str, Any]) -> str:
        """Generate conclusion section."""
        results_summary = context.get("results_summary", {})
        
        prompt = f"""
        Write a brief conclusion (80-100 words).
        
        Outcomes: {results_summary.get('visualizations', 0)} visualizations, {results_summary.get('total_outputs', 0)} outputs
        Key Points: {', '.join(context.get('key_findings', [])[:2])}
        
        Summarize: achievements and significance. Be concise.
        """
        
        return self._generate_section("Conclusion", prompt.strip(), max_tokens=150)
    
    def _generate_section(self, section_name: str, prompt: str, max_tokens: int = None) -> str:
        """Generate a report section using LLM."""
        try:
            full_prompt = f"""
            Write technical report content. Be concise, clear, and professional.
            
            {prompt}
            
            IMPORTANT: Write ONLY the content text. Do NOT include section headers (##, ###), 
            do NOT include the word "{section_name}" as a header. Just write the paragraph content.
            Use clear language, stay on topic, avoid repetition.
            """
            
            if max_tokens is None:
                max_tokens = self.config.get("llm", {}).get("max_tokens", 400)
            
            response = self.llm.generate(
                prompt=full_prompt,
                max_tokens=max_tokens,
                temperature=self.config.get("llm", {}).get("temperature", 0.7)
            )
            
            # Clean up response - remove any section headers that might have been generated
            response = response.strip()
            lines = response.split('\n')
            cleaned_lines = []
            for line in lines:
                # Skip lines that are section headers
                if line.strip().startswith('#') or (line.strip().startswith(section_name) and len(line.strip()) < 50):
                    continue
                cleaned_lines.append(line)
            
            return '\n'.join(cleaned_lines).strip()
            
        except Exception as e:
            self.logger.error(f"Failed to generate {section_name} section: {e}")
            return f"[Content generation failed: {str(e)}]"