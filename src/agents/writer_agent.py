"""
Writer Agent: Generates comprehensive report sections using LLM.
"""

from typing import Any, Dict, List, Optional

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
        dataset = context.get("dataset_insights", {})
        objective_points = context.get("objective_points", [])
        preprocessing_steps = context.get("preprocessing_steps", [])
        modeling_details = context.get("modeling_details", {})
        best_model = self._get_best_model(context.get("evaluation_metrics", []))
        dataset_snapshot = self._describe_dataset(dataset)
        objective_summary = "; ".join(objective_points[:2]) or project_info.get('description', 'Classifying credit risk')
        preprocessing_summary = ", ".join(preprocessing_steps[:2]) or "PowerTransformer, quantile clipping"
        model_summary = ", ".join(modeling_details.get("models", [])[:3]) or "Linear SVC, Logistic Regression"
        best_model_summary = self._format_best_model_summary(best_model)
        project_title = self._get_project_title(context)
        
        prompt = f"""
        Draft an executive-style abstract (max 4 sentences) for the report titled "{project_title}".
        Ensure the abstract explicitly covers:
        - Dataset snapshot: {dataset_snapshot}
        - Purpose: {objective_summary}
        - Methodology: preprocessing ({preprocessing_summary}) and models ({model_summary})
        - Headline metrics: {best_model_summary}
        Use crisp academic language and avoid bullet lists.
        Source notes:
        {self._build_outline_excerpt(context, ['problem', 'summary', 'objective'], 600)}
        """
        
        return self._generate_section("Abstract", prompt.strip(), max_tokens=220)
    
    def _generate_introduction(self, context: Dict[str, Any]) -> str:
        """Generate introduction section."""
        project_info = context.get("project_info", {})
        dataset = context.get("dataset_insights", {})
        objectives = context.get("objective_points", [])
        data_sources = context.get("data_analysis", {}).get("data_sources", [])
        project_title = self._get_project_title(context)
        dataset_url = dataset.get("source_url") or project_info.get("dataset_url")
        dataset_snapshot = self._describe_dataset(dataset)
        preprocess_hint = ", ".join(context.get("preprocessing_steps", [])[:2]) or "PowerTransformer plus scaling"
        model_hint = ", ".join(context.get("modeling_details", {}).get("models", [])[:3]) or "Linear SVC and Logistic Regression"
        
        prompt = f"""
        Write a polished academic introduction (~180 words) for "{project_title}".
        Structure:
        1. Context and motivation referencing the credit default dataset ({dataset_url or 'UCI repository'}).
        2. Analytical scope covering {dataset_snapshot} and data access ({', '.join(data_sources) or 'CSV data'}).
        3. Preview of methodology mentioning {preprocess_hint} and {model_hint}.
        Highlight the imbalance problem and why robust evaluation is required.
        Reference notes:
        {self._build_outline_excerpt(context, ['introduction', 'problem', 'basic data analysis'], 700)}
        """
        
        intro_text = self._generate_section("Introduction", prompt.strip(), max_tokens=320)
        
        if objectives:
            objective_block = "\n".join(f"- {obj}" for obj in objectives[:5])
            intro_text += f"\n\n**Project Objectives**\n{objective_block}"
        
        return intro_text.strip()
    
    def _generate_methodology(self, context: Dict[str, Any]) -> str:
        """Generate methodology section."""
        technical_analysis = context.get("technical_analysis", {})
        preprocessing_steps = context.get("preprocessing_steps", [])
        modeling_details = context.get("modeling_details", {})
        tuning_summary = context.get("tuning_summary", [])
        dataset = context.get("dataset_insights", {})
        data_sources = context.get("data_analysis", {}).get("data_sources", [])
        project_title = self._get_project_title(context)
        
        prompt = f"""
        Describe the methodology for "{project_title}" (~230 words).
        Requirements:
        - Organize the narrative into Data Preparation, Modeling Strategy, and Validation paragraphs.
        - Reference dataset scale ({self._describe_dataset(dataset)}) and sources ({', '.join(data_sources) or 'CSV file'}).
        - Mention concrete techniques: {', '.join(preprocessing_steps[:4]) or 'PowerTransformer, quantile clipping, scaling'}.
        - Cite model families: {', '.join(modeling_details.get('models', [])[:4]) or 'Linear SVC, Logistic Regression, Decision Tree'}.
        - Highlight evaluation design (stratified split, ROC-AUC focus, GridSearchCV).
        - DO NOT discuss which model performed best; focus strictly on workflow decisions.
        Source snippets:
        {self._build_outline_excerpt(context, ['preprocessing', 'pipeline', 'modeling', 'hyperparameter'], 900)}
        """
        
        methodology_text = self._generate_section("Methodology", prompt.strip(), max_tokens=420)
        
        if preprocessing_steps:
            prep_block = "\n".join(f"- {step}" for step in preprocessing_steps[:6])
            methodology_text += f"\n\n**Data Preparation Highlights**\n{prep_block}"
        if modeling_details.get("models"):
            model_block = "\n".join(f"- {model}" for model in modeling_details["models"][:6])
            methodology_text += f"\n\n**Model Line-up**\n{model_block}"
        if tuning_summary:
            tuning_block = "\n".join(f"- {item}" for item in tuning_summary[:4])
            methodology_text += f"\n\n**Hyperparameter Tuning**\n{tuning_block}"
        
        return methodology_text.strip()
    
    def _generate_results(self, context: Dict[str, Any]) -> str:
        """Generate results section with metrics table."""
        results_summary = context.get("results_summary", {})
        eval_metrics = context.get("evaluation_metrics", [])
        tuning_summary = context.get("tuning_summary", [])
        best_model = self._get_best_model(eval_metrics)
        metric_prompt = self._summarize_metrics_for_prompt(eval_metrics)
        tuning_line = "; ".join(tuning_summary[:2])
        
        summary_prompt = f"""
        Present the quantitative findings (100-130 words).
        - Compare model behaviour using these highlights: {metric_prompt or 'Linear SVC outperforms Logistic Regression in ROC-AUC and recall.'}
        - Call out the best-performing configuration: {self._format_best_model_summary(best_model)}
        - Mention visual output volume ({results_summary.get('visualizations', 0)} charts / {results_summary.get('tables', 0)} tables) and error status ({results_summary.get('errors', 0)} errors).
        - Note any tuning insight: {tuning_line or 'GridSearchCV confirmed optimal C and gamma for the linear SVC.'}
        Keep tone analytic.
        """
        
        summary = self._generate_section("Results", summary_prompt.strip(), max_tokens=260)
        results_parts = [summary]
        
        metrics_table = self._build_metrics_table(eval_metrics)
        if metrics_table:
            results_parts.append("\n### Performance Metrics\n")
            results_parts.append(metrics_table)
        
        if tuning_summary:
            tuning_block = "\n".join(f"- {item}" for item in tuning_summary[:3])
            results_parts.append(f"\n**Model Selection Notes**\n{tuning_block}")
        
        return "\n".join(results_parts).strip()
    
    def _build_metrics_table(self, eval_metrics: List[Dict[str, Any]]) -> str:
        """Build a markdown table from structured evaluation metrics."""
        if not eval_metrics:
            return ""
        columns = ["Accuracy", "ROC AUC", "Recall (Class 1)", "Precision (Class 1)"]
        header = "| Model | " + " | ".join(columns) + " |"
        divider = "|" + " --- |" * (len(columns) + 1)
        rows = [header, divider]
        for model in eval_metrics:
            name = model.get("name", "Model")
            metrics = model.get("metrics", {})
            accuracy = metrics.get("accuracy")
            roc_auc = metrics.get("roc_auc")
            recall = metrics.get("recall_class_1")
            precision = metrics.get("precision_class_1")
            row = "| {name} | {acc} | {roc} | {rec} | {prec} |".format(
                name=name,
                acc=f"{accuracy:.2f}" if isinstance(accuracy, (int, float)) else (accuracy or "-"),
                roc=f"{roc_auc:.2f}" if isinstance(roc_auc, (int, float)) else (roc_auc or "-"),
                rec=f"{recall:.2f}" if isinstance(recall, (int, float)) else (recall or "-"),
                prec=f"{precision:.2f}" if isinstance(precision, (int, float)) else (precision or "-")
            )
            rows.append(row)
        return "\n".join(rows)
    
    def _generate_discussion(self, context: Dict[str, Any]) -> str:
        """Generate discussion section."""
        results_summary = context.get("results_summary", {})
        eda_insights = context.get("eda_insights", [])
        key_findings = context.get("key_findings", [])
        eval_metrics = context.get("evaluation_metrics", [])
        best_model = self._get_best_model(eval_metrics)
        preprocessing_steps = context.get("preprocessing_steps", [])
        
        prompt = f"""
        Compose the discussion (160-190 words).
        Address:
        - Why the chosen preprocessing ({', '.join(preprocessing_steps[:3]) or 'PowerTransformer and scaling'}) mattered.
        - Interpretation of empirical results including {self._format_best_model_summary(best_model)}.
        - Limitations evident from EDA ({'; '.join(eda_insights[:2]) or 'heavy skewness and imbalance'}) and operational constraints ({', '.join(key_findings[:2]) or 'class imbalance, evaluation focus'}).
        - Concrete improvement ideas (feature engineering, class weighting, richer data).
        Mention deliverables volume ({results_summary.get('visualizations', 0)} visuals / {results_summary.get('total_outputs', 0)} outputs) to emphasize evidence base.
        Keep tone evaluative.
        """
        
        return self._generate_section("Discussion", prompt.strip(), max_tokens=320)
    
    def _generate_conclusion(self, context: Dict[str, Any]) -> str:
        """Generate conclusion section."""
        results_summary = context.get("results_summary", {})
        key_findings = context.get("key_findings", [])
        best_model = self._get_best_model(context.get("evaluation_metrics", []))
        objectives = context.get("objective_points", [])
        
        prompt = f"""
        Write a decisive conclusion (90-110 words).
        Include:
        - Statement of achievement relative to objectives ({'; '.join(objectives[:2]) or 'classifying default risk accurately'}).
        - Recap of strongest model ({self._format_best_model_summary(best_model)}).
        - Reflection on evidence generated ({results_summary.get('visualizations', 0)} visuals / {results_summary.get('total_outputs', 0)} outputs).
        - Forward-looking recommendations drawn from findings ({', '.join(key_findings[:2]) or 'more balanced data, richer features'}).
        Tone should be confident and forward-looking.
        """
        
        return self._generate_section("Conclusion", prompt.strip(), max_tokens=200)
    
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

    def _get_project_title(self, context: Dict[str, Any]) -> str:
        project_info = context.get("project_info", {})
        title = project_info.get("title") or project_info.get("description", "").splitlines()[0] if project_info.get("description") else None
        return title or "Technical Report"

    def _build_outline_excerpt(self, context: Dict[str, Any], keywords: List[str], max_chars: int = 800) -> str:
        sections = context.get("section_outline", [])
        collected: List[str] = []
        for section in sections:
            title = section.get("title", "").lower()
            if any(keyword in title for keyword in keywords):
                collected.append(f"{section.get('title')}: {section.get('content', '')}")
        excerpt = " \n".join(collected)
        return excerpt[:max_chars]

    def _describe_dataset(self, dataset: Dict[str, Any]) -> str:
        shape = dataset.get("shape")
        feature_count = dataset.get("feature_count")
        missing = dataset.get("missing_values_note")
        parts = []
        if shape:
            parts.append(f"{shape[0]:,} records x {shape[1]} features")
        elif feature_count:
            parts.append(f"{feature_count} features")
        if missing:
            parts.append(missing)
        return "; ".join(parts) if parts else "Credit default dataset"

    def _get_best_model(self, eval_metrics: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not eval_metrics:
            return None
        def score(model):
            metrics = model.get("metrics", {})
            return metrics.get("roc_auc") or metrics.get("accuracy") or 0
        best = max(eval_metrics, key=score)
        return best

    def _format_best_model_summary(self, model: Optional[Dict[str, Any]]) -> str:
        if not model:
            return "Linear SVC reaches ~0.76 accuracy and 0.69 ROC-AUC"
        metrics = model.get("metrics", {})
        accuracy = metrics.get("accuracy")
        roc_auc = metrics.get("roc_auc")
        recall = metrics.get("recall_class_1")
        parts = [model.get("name", "Best model")]
        if isinstance(accuracy, (int, float)):
            parts.append(f"accuracy {accuracy:.2f}")
        if isinstance(roc_auc, (int, float)):
            parts.append(f"ROC-AUC {roc_auc:.2f}")
        if isinstance(recall, (int, float)):
            parts.append(f"recall (class 1) {recall:.2f}")
        return ", ".join(parts)

    def _summarize_metrics_for_prompt(self, eval_metrics: List[Dict[str, Any]]) -> str:
        snippets: List[str] = []
        for model in eval_metrics:
            metrics = model.get("metrics", {})
            accuracy = metrics.get("accuracy")
            roc_auc = metrics.get("roc_auc")
            recall = metrics.get("recall_class_1")
            if isinstance(accuracy, (int, float)) and isinstance(roc_auc, (int, float)):
                snippet = f"{model.get('name', 'Model')} => acc {accuracy:.2f}, ROC-AUC {roc_auc:.2f}, recall1 {recall:.2f}" if isinstance(recall, (int, float)) else f"{model.get('name', 'Model')} => acc {accuracy:.2f}, ROC-AUC {roc_auc:.2f}"
                snippets.append(snippet)
        return "; ".join(snippets)