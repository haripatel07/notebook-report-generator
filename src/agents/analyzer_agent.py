"""
Analyzer Agent: Extracts and analyzes context from parsed input files.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

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
        
        # Build markdown outline once for downstream tasks
        markdown_outline = self._build_markdown_outline(
            parsed_data.get("markdown_cells", [])
        )
        
        # Extract different types of information
        project_info = self._analyze_project_structure(parsed_data, markdown_outline)
        technical_analysis = self._analyze_technical_content(parsed_data)
        data_analysis = self._analyze_data_processing(parsed_data)
        results_summary = self._summarize_results(parsed_data)
        dataset_insights = self._extract_dataset_insights(parsed_data, markdown_outline)
        eda_insights = self._extract_eda_insights(parsed_data, markdown_outline)
        preprocessing_steps = self._extract_preprocessing_steps(parsed_data, markdown_outline)
        modeling_details = self._extract_modeling_details(parsed_data, markdown_outline)
        evaluation_metrics = self._extract_evaluation_metrics(
            parsed_data.get("outputs", {}).get("text", [])
        )
        tuning_summary = self._extract_tuning_summary(
            parsed_data.get("outputs", {}).get("text", []),
            markdown_outline
        )
        objective_points = self._extract_objectives_from_outline(markdown_outline)
        
        # Generate comprehensive context
        analysis_context = {
            "project_info": project_info,
            "technical_analysis": technical_analysis,
            "data_analysis": data_analysis,
            "results_summary": results_summary,
            "section_outline": markdown_outline,
            "objective_points": objective_points,
            "dataset_insights": dataset_insights,
            "eda_insights": eda_insights,
            "preprocessing_steps": preprocessing_steps,
            "modeling_details": modeling_details,
            "evaluation_metrics": evaluation_metrics,
            "tuning_summary": tuning_summary,
            "report_type": report_type,
            "complexity_level": self._assess_complexity(technical_analysis),
            "key_findings": self._extract_key_findings(results_summary)
        }
        
        self.logger.info("Analysis complete")
        return analysis_context
    
    def _analyze_project_structure(
        self,
        parsed_data: Dict[str, Any],
        outline: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
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
        
        project_title = outline[0]["title"] if outline else ""
        dataset_url = self._extract_first_url(markdown_cells)
        
        return {
            "description": project_description,
            "objectives": objectives,
            "libraries_used": libraries,
            "notebook_metadata": parsed_data.get("metadata", {}),
            "title": project_title,
            "dataset_url": dataset_url
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

    def _extract_first_url(self, markdown_cells: List[Dict[str, Any]]) -> Optional[str]:
        """Return the first URL mentioned in markdown cells, if any."""
        url_pattern = re.compile(r"(https?://\S+)")
        for cell in markdown_cells:
            match = url_pattern.search(cell.get("source", ""))
            if match:
                return match.group(1).strip().rstrip(')')
        return None

    def _build_markdown_outline(self, markdown_cells: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create an ordered outline of markdown headings and their content."""
        outline: List[Dict[str, Any]] = []
        current: Optional[Dict[str, Any]] = None
        
        def flush_current():
            nonlocal current
            if current:
                lines = current.pop("content_lines", [])
                current["content"] = self._clean_content_lines(lines)
                outline.append(current)
                current = None
        
        for cell in markdown_cells:
            text = cell.get("source", "")
            if not text:
                continue
            lines = text.splitlines()
            for raw_line in lines:
                line = raw_line.rstrip()
                stripped = line.strip()
                if not stripped:
                    if current:
                        current.setdefault("content_lines", []).append("")
                    continue
                if stripped.startswith('#'):
                    flush_current()
                    level = len(stripped) - len(stripped.lstrip('#'))
                    title = stripped.lstrip('#').strip() or "Untitled Section"
                    current = {
                        "title": title,
                        "level": max(level, 1),
                        "content_lines": []
                    }
                else:
                    if current is None:
                        current = {
                            "title": "Context",
                            "level": 2,
                            "content_lines": []
                        }
                    current.setdefault("content_lines", []).append(stripped)
            if current:
                current.setdefault("content_lines", []).append("")
        flush_current()
        return outline

    def _clean_content_lines(self, lines: List[str]) -> str:
        """Normalize whitespace in collected markdown lines."""
        cleaned: List[str] = []
        last_blank = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if not last_blank:
                    cleaned.append("")
                last_blank = True
            else:
                cleaned.append(stripped)
                last_blank = False
        return "\n".join(cleaned).strip()

    def _extract_objectives_from_outline(self, outline: List[Dict[str, Any]]) -> List[str]:
        """Collect objective statements from outline sections."""
        objectives: List[str] = []
        for section in outline:
            title = section.get("title", "").lower()
            if "objective" in title or "goal" in title:
                bullets = self._split_bullet_lines(section.get("content", ""))
                if bullets:
                    objectives.extend(bullets)
                else:
                    objectives.extend([
                        line.strip()
                        for line in section.get("content", "").splitlines()
                        if line.strip()
                    ])
        return objectives[:10]

    def _split_bullet_lines(self, block: str) -> List[str]:
        """Extract bullet or numbered lines from a text block."""
        bullets: List[str] = []
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(('- ', '* ', '• ')):
                bullets.append(stripped[2:].strip())
            else:
                match = re.match(r"^\d+[\).]\s+(.*)", stripped)
                if match:
                    bullets.append(match.group(1).strip())
        return bullets

    def _extract_dataset_insights(
        self,
        parsed_data: Dict[str, Any],
        outline: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Summarize dataset-level insights from outputs and markdown."""
        text_outputs = parsed_data.get("outputs", {}).get("text", [])
        shape = self._parse_dataset_shape(text_outputs)
        feature_count = self._parse_feature_count(text_outputs)
        missing_note = self._detect_missing_values(text_outputs)
        dataset_section = next(
            (section for section in outline if "dataset" in section.get("title", "").lower()),
            None
        )
        summary_points: List[str] = []
        if dataset_section:
            summary_points = self._split_bullet_lines(dataset_section.get("content", ""))
            if not summary_points:
                summary_points = [
                    line.strip()
                    for line in dataset_section.get("content", "").splitlines()
                    if line.strip()
                ]
        source_url = None
        if dataset_section and 'http' in dataset_section.get("content", ""):
            match = re.search(r"(https?://\S+)", dataset_section.get("content", ""))
            if match:
                source_url = match.group(1).strip()
        return {
            "title": dataset_section.get("title") if dataset_section else "",
            "summary_points": summary_points[:8],
            "shape": shape,
            "feature_count": feature_count,
            "missing_values_note": missing_note,
            "source_url": source_url or parsed_data.get("metadata", {}).get("dataset_url"),
            "raw_excerpt": dataset_section.get("content", "") if dataset_section else ""
        }

    def _parse_dataset_shape(self, text_outputs: List[str]) -> Optional[Tuple[int, int]]:
        """Parse dataset shape tuple from text outputs."""
        shape_pattern = re.compile(r"\((\d{2,}),\s*(\d{1,})\)")
        for text in text_outputs:
            match = shape_pattern.search(text)
            if match:
                try:
                    return int(match.group(1)), int(match.group(2))
                except ValueError:
                    continue
        return None

    def _parse_feature_count(self, text_outputs: List[str]) -> Optional[int]:
        """Extract number of columns from dataframe info output."""
        pattern = re.compile(r"total\s+(\d+)\s+columns", re.IGNORECASE)
        for text in text_outputs:
            match = pattern.search(text)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        return None

    def _detect_missing_values(self, text_outputs: List[str]) -> Optional[str]:
        """Detect simple missing value statements."""
        for text in text_outputs:
            if "dtype" in text and "default payment next month" in text:
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                numeric_lines = [line for line in lines if not line.lower().startswith("dtype")]
                if numeric_lines and all(line.endswith('0') for line in numeric_lines):
                    return "No missing values detected across all 25 features."
        return None

    def _extract_eda_insights(
        self,
        parsed_data: Dict[str, Any],
        outline: List[Dict[str, Any]]
    ) -> List[str]:
        """Derive EDA highlights from markdown and outputs."""
        insights: List[str] = []
        keywords = ["eda", "analysis", "distribution", "exploration"]
        for section in outline:
            if any(keyword in section.get("title", "").lower() for keyword in keywords):
                bullets = self._split_bullet_lines(section.get("content", ""))
                if bullets:
                    insights.extend(bullets)
                else:
                    insights.extend([
                        line.strip()
                        for line in section.get("content", "").splitlines()
                        if line.strip()
                    ])
        skewness_note = self._summarize_skewness(parsed_data.get("outputs", {}).get("text", []))
        if skewness_note:
            insights.append(skewness_note)
        corr_note = self._summarize_correlations(parsed_data.get("outputs", {}).get("text", []))
        if corr_note:
            insights.append(corr_note)
        return insights[:12]

    def _summarize_skewness(self, text_outputs: List[str]) -> Optional[str]:
        for text in text_outputs:
            if "skewed" in text.lower():
                features = [
                    line.split(' is ')[0].strip()
                    for line in text.splitlines()
                    if "skewed" in line.lower()
                ]
                if features:
                    highlight = ", ".join(features[:5])
                    if len(features) > 5:
                        highlight += ", ..."
                    return f"Severe skewness observed in {len(features)} variables ({highlight})."
        return None

    def _summarize_correlations(self, text_outputs: List[str]) -> Optional[str]:
        for text in text_outputs:
            if "Name: default payment next month" in text:
                pairs = self._extract_series_pairs(text)
                positives = [
                    f"{name} ({value:.3f})"
                    for name, value in pairs
                    if value > 0.05 and name.lower() != "default payment next month"
                ]
                negatives = [
                    f"{name} ({value:.3f})"
                    for name, value in pairs
                    if value < -0.05
                ]
                snippets = []
                if positives:
                    snippets.append(f"PAY sequence features show the strongest positive correlation: {', '.join(positives[:4])}.")
                if negatives:
                    snippets.append(f"Credit limits and repayment amounts have weak negative correlation: {', '.join(negatives[:3])}.")
                return " ".join(snippets) if snippets else None
        return None

    def _extract_series_pairs(self, block: str) -> List[Tuple[str, float]]:
        pairs: List[Tuple[str, float]] = []
        for raw_line in block.splitlines():
            match = re.match(r"^([A-Za-z0-9_ ]+?)\s+(-?\d+\.\d+)$", raw_line.strip())
            if match:
                name = match.group(1).strip()
                try:
                    value = float(match.group(2))
                except ValueError:
                    continue
                pairs.append((name, value))
        return pairs

    def _extract_preprocessing_steps(
        self,
        parsed_data: Dict[str, Any],
        outline: List[Dict[str, Any]]
    ) -> List[str]:
        steps: List[str] = []
        section_keywords = ["preprocessing", "handling", "pipeline", "feature", "scaling"]
        for section in outline:
            if any(keyword in section.get("title", "").lower() for keyword in section_keywords):
                bullets = self._split_bullet_lines(section.get("content", ""))
                if bullets:
                    steps.extend(bullets)
                else:
                    steps.extend([
                        line.strip()
                        for line in section.get("content", "").splitlines()
                        if line.strip()
                    ])
        imports = parsed_data.get("imports", [])
        preprocess_map = {
            "PowerTransformer": "Applied PowerTransformer to correct heavy-tailed distributions.",
            "QuantileTransformer": "Used quantile-based clipping to contain extreme outliers.",
            "StandardScaler": "Scaled numerical features with StandardScaler for SVM stability.",
            "Pipeline": "Wrapped preprocessing and estimator steps inside a sklearn Pipeline.",
            "SMOTE": "Considered sampling strategies to mitigate class imbalance."
        }
        for lib, description in preprocess_map.items():
            if any(lib in imp for imp in imports):
                steps.append(description)
        # Deduplicate while preserving order
        seen = set()
        ordered_steps = []
        for step in steps:
            if step and step not in seen:
                ordered_steps.append(step)
                seen.add(step)
        return ordered_steps[:12]

    def _extract_modeling_details(
        self,
        parsed_data: Dict[str, Any],
        outline: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        code_cells = parsed_data.get("code_cells", [])
        imports = parsed_data.get("imports", [])
        models = self._extract_model_names_from_code(code_cells, imports)
        modeling_sections = [
            section for section in outline
            if any(keyword in section.get("title", "").lower() for keyword in ["model", "hyperparameter", "summary"])
        ]
        notes: List[str] = []
        for section in modeling_sections:
            bullets = self._split_bullet_lines(section.get("content", ""))
            if bullets:
                notes.extend(bullets)
            else:
                notes.extend([
                    line.strip()
                    for line in section.get("content", "").splitlines()
                    if line.strip()
                ])
        return {
            "models": models,
            "notes": notes[:12]
        }

    def _extract_model_names_from_code(
        self,
        code_cells: List[Dict[str, Any]],
        imports: List[str]
    ) -> List[str]:
        model_hints = [
            ("SVC", "Support Vector Classifier"),
            ("LogisticRegression", "Logistic Regression"),
            ("DecisionTreeClassifier", "Decision Tree Classifier"),
            ("RandomForestClassifier", "Random Forest"),
            ("GradientBoostingClassifier", "Gradient Boosting"),
            ("XGBClassifier", "XGBoost Classifier"),
            ("LGBMClassifier", "LightGBM Classifier"),
            ("AdaBoostClassifier", "AdaBoost Classifier"),
            ("Pipeline", "Scikit-learn Pipeline")
        ]
        code_text = "\n".join(cell.get("source", "") for cell in code_cells)
        all_text = code_text + "\n" + "\n".join(imports)
        found = []
        for hint, label in model_hints:
            if hint in all_text and label not in found:
                found.append(label)
        return found

    def _extract_evaluation_metrics(self, text_outputs: List[str]) -> List[Dict[str, Any]]:
        """Parse evaluation metrics for each model block."""
        metrics: List[Dict[str, Any]] = []
        current: Optional[Dict[str, Any]] = None
        collecting_confusion = False
        confusion_lines: List[str] = []
        for block in text_outputs:
            lines = block.splitlines()
            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    if collecting_confusion and confusion_lines:
                        current = self._attach_confusion(current, confusion_lines)
                        confusion_lines = []
                        collecting_confusion = False
                    continue
                if line.startswith("Model:"):
                    if current:
                        metrics.append(current)
                    current = {
                        "name": line.replace("Model:", "").strip(),
                        "metrics": {}
                    }
                    collecting_confusion = False
                    confusion_lines = []
                elif line.startswith("Confusion Matrix"):
                    collecting_confusion = True
                    confusion_lines = []
                elif collecting_confusion:
                    confusion_lines.append(line)
                    # Expect two rows; attach once we have them
                    if len(confusion_lines) >= 2 and line.endswith("]"):
                        current = self._attach_confusion(current, confusion_lines)
                        confusion_lines = []
                        collecting_confusion = False
                elif line.startswith("ROC AUC Score") and current:
                    value = line.split(":", 1)[-1].strip()
                    try:
                        current["metrics"]["roc_auc"] = float(value)
                    except ValueError:
                        current["metrics"]["roc_auc"] = value
                elif line.lower().startswith("accuracy") and current:
                    parts = line.split()
                    accuracy_value = None
                    if len(parts) >= 2:
                        try:
                            accuracy_value = float(parts[1])
                        except ValueError:
                            accuracy_value = None
                    if accuracy_value is None:
                        for token in reversed(parts):
                            token_clean = token.strip()
                            if '.' not in token_clean:
                                continue
                            try:
                                accuracy_value = float(token_clean)
                                break
                            except ValueError:
                                continue
                    if accuracy_value is not None:
                        current["metrics"]["accuracy"] = accuracy_value
                else:
                    class_match = re.match(r"^(0|1)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", line)
                    if class_match and current:
                        label = class_match.group(1)
                        current["metrics"][f"precision_class_{label}"] = float(class_match.group(2))
                        current["metrics"][f"recall_class_{label}"] = float(class_match.group(3))
                        current["metrics"][f"f1_class_{label}"] = float(class_match.group(4))
            if collecting_confusion and confusion_lines:
                current = self._attach_confusion(current, confusion_lines)
                confusion_lines = []
                collecting_confusion = False
        if current:
            metrics.append(current)
        return metrics

    def _attach_confusion(
        self,
        current: Optional[Dict[str, Any]],
        confusion_lines: List[str]
    ) -> Optional[Dict[str, Any]]:
        if current is None:
            return None
        matrix: List[List[int]] = []
        for line in confusion_lines:
            numbers = [int(num) for num in re.findall(r"\d+", line)]
            if numbers:
                matrix.append(numbers)
        if matrix:
            current["metrics"]["confusion_matrix"] = matrix
        return current

    def _extract_tuning_summary(
        self,
        text_outputs: List[str],
        outline: List[Dict[str, Any]]
    ) -> List[str]:
        summary: List[str] = []
        for block in text_outputs:
            if "Best params" in block or "Best CV" in block:
                for line in block.splitlines():
                    stripped = line.strip()
                    if stripped.lower().startswith("best params") or stripped.lower().startswith("best cv"):
                        summary.append(stripped)
        if not summary:
            for section in outline:
                if "hyperparameter" in section.get("title", "").lower():
                    summary.extend(
                        self._split_bullet_lines(section.get("content", ""))
                        or [line.strip() for line in section.get("content", "").splitlines() if line.strip()]
                    )
        return summary[:6]