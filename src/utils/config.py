"""
Configuration management for the report generator.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """LLM configuration settings."""
    
    provider: str = Field(default="ollama", description="LLM provider (ollama, openai)")
    model: str = Field(default="llama2", description="Model name")
    base_url: Optional[str] = Field(default="http://localhost:11434", description="API base URL")
    api_key: Optional[str] = Field(default=None, description="API key (if required)")
    temperature: float = Field(default=0.7, description="Generation temperature")
    max_tokens: int = Field(default=2000, description="Maximum tokens per generation")
    timeout: int = Field(default=120, description="Request timeout in seconds")


class ReportConfig(BaseModel):
    """Report generation configuration."""
    
    include_abstract: bool = Field(default=True)
    include_table_of_contents: bool = Field(default=True)
    include_references: bool = Field(default=True)
    include_appendix: bool = Field(default=False)
    max_code_snippet_lines: int = Field(default=50)
    diagram_format: str = Field(default="mermaid", description="mermaid or graphviz")
    citation_style: str = Field(default="ieee", description="ieee or apa")


class PlagiarismConfig(BaseModel):
    """Plagiarism prevention configuration."""
    
    enabled: bool = Field(default=True)
    max_similarity_threshold: float = Field(default=0.3, description="Maximum allowed similarity")
    paraphrase_iterations: int = Field(default=2, description="Number of paraphrasing passes")
    check_against_sources: bool = Field(default=True)


class Config(BaseModel):
    """Main configuration class."""
    
    llm: LLMConfig = Field(default_factory=LLMConfig)
    report: ReportConfig = Field(default_factory=ReportConfig)
    plagiarism: PlagiarismConfig = Field(default_factory=PlagiarismConfig)
    
    log_level: str = Field(default="INFO")
    output_directory: Path = Field(default=Path("./output"))
    cache_directory: Path = Field(default=Path("./.cache"))
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from file."""
        if config_path and config_path.exists():
            with open(config_path, "r") as f:
                config_dict = yaml.safe_load(f)
            return cls(**config_dict)
        return cls()
    
    @classmethod
    def load_default(cls) -> "Config":
        """Load default configuration."""
        default_config_path = Path(__file__).parent.parent.parent / "config" / "default_config.yaml"
        
        if default_config_path.exists():
            return cls.load(default_config_path)
        
        return cls()
    
    def save(self, config_path: Path):
        """Save configuration to file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)
    
    def set_log_level(self, level: str):
        """Set logging level."""
        self.log_level = level.upper()
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration as dictionary."""
        return self.llm.model_dump()
    
    def ensure_directories(self):
        """Ensure output and cache directories exist."""
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.cache_directory.mkdir(parents=True, exist_ok=True)


def load_prompt_templates() -> Dict[str, str]:
    """Load prompt templates from configuration."""
    template_path = Path(__file__).parent.parent.parent / "config" / "llm_prompts.yaml"
    
    if template_path.exists():
        with open(template_path, "r") as f:
            return yaml.safe_load(f)
    
    return get_default_prompts()


def get_default_prompts() -> Dict[str, str]:
    """Get default prompt templates."""
    return {
        "system_prompt": """You are a technical documentation assistant specialized in generating 
high-quality, original technical reports from project artifacts. Your writing must be:
- Clear, professional, and academically appropriate
- Based on actual implementation details, not generic theory
- Original and plagiarism-free
- Well-structured and properly referenced""",
        
        "analyzer_prompt": """Analyze the provided project artifacts and extract:
1. Main objectives and problem statement
2. Datasets used and their characteristics
3. Methods and algorithms implemented
4. Experimental setup and parameters
5. Results and key findings

Focus on what was ACTUALLY done, not what could theoretically be done.""",
        
        "writer_prompt": """Generate the {section_name} section for a {report_type} report.

Context: {context}

Guidelines:
- Use formal, clear language
- Explain WHY decisions were made, not just WHAT was done
- Reference actual implementation details
- Avoid generic textbook definitions
- Keep it concise and relevant

Generate ONLY the content for this section, without headers or formatting.""",
        
        "diagram_prompt": """Generate a {diagram_type} diagram representing the workflow.

Context: {context}

Create a Mermaid diagram that shows:
- Actual project components
- Data flow between stages
- Key processing steps

Output ONLY the Mermaid code, starting with ```mermaid"""
    }
