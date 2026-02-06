"""
Abstract interface for LLM providers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class LLMInterface(ABC):
    """
    Abstract interface for LLM providers.
    Allows switching between Ollama, OpenAI, or other providers.
    """
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        stop_sequences: Optional[List[str]] = None
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            stop_sequences: Optional list of stop sequences
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ):
        """
        Generate text with streaming (yields chunks).
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Yields:
            Text chunks as they are generated
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the LLM service is available.
        
        Returns:
            True if service is reachable, False otherwise
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Get information about the current model.
        
        Returns:
            Dictionary with model details
        """
        pass
