"""
Base agent class for the multi-agent system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.llm.llm_interface import LLMInterface
from src.utils.logger import setup_logger


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.
    
    Each agent is responsible for a specific aspect of report generation:
    - Analyzer: Extracts context from input files
    - Writer: Generates report sections
    - Diagram: Creates visualizations
    - Citation: Manages references
    """
    
    def __init__(self, llm: LLMInterface, config: Dict[str, Any]):
        """
        Initialize the agent.
        
        Args:
            llm: LLM interface for text generation
            config: Agent-specific configuration
        """
        self.llm = llm
        self.config = config
        self.logger = setup_logger(self.__class__.__name__)
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main task.
        
        Args:
            context: Input context containing necessary information
            
        Returns:
            Dictionary containing the agent's output
        """
        pass
    
    def _validate_input(self, context: Dict[str, Any], required_keys: list) -> bool:
        """
        Validate that context contains required keys.
        
        Args:
            context: Input context
            required_keys: List of required key names
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        missing = [key for key in required_keys if key not in context]
        
        if missing:
            raise ValueError(f"Missing required context keys: {missing}")
        
        return True
    
    def _build_prompt(self, template: str, **kwargs) -> str:
        """
        Build a prompt from template and variables.
        
        Args:
            template: Prompt template string
            **kwargs: Variables to inject into template
            
        Returns:
            Formatted prompt string
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            self.logger.error(f"Missing template variable: {e}")
            raise
    
    def _generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate text using the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Generation temperature
            
        Returns:
            Generated text
        """
        return self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens or self.config.get("max_tokens", 2000),
            temperature=temperature or self.config.get("temperature", 0.7)
        )
    
    def _post_process(self, text: str) -> str:
        """
        Post-process generated text.
        
        Args:
            text: Raw generated text
            
        Returns:
            Cleaned and processed text
        """
        # Remove excessive whitespace
        text = "\n".join(line.strip() for line in text.split("\n"))
        
        # Remove multiple blank lines
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")
        
        return text.strip()
