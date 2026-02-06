"""
OpenAI LLM client implementation.
"""

from typing import Optional, Dict, Any, List
import time

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

from src.llm.llm_interface import LLMInterface
from src.utils.logger import setup_logger


class OpenAIClient(LLMInterface):
    """
    OpenAI API client for LLM inference.
    
    Supports GPT models through OpenAI API.
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Initialize OpenAI client.
        
        Args:
            model: Model name (e.g., 'gpt-3.5-turbo', 'gpt-4')
            api_key: OpenAI API key
            base_url: Custom API base URL
            timeout: Request timeout in seconds
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.logger = setup_logger(self.__class__.__name__)
        
        # Initialize client
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout
        )
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        stop_sequences: Optional[List[str]] = None
    ) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop_sequences: Sequences to stop generation
            
        Returns:
            Generated text
        """
        try:
            self.logger.debug(f"Generating with {self.model}, max_tokens={max_tokens}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop_sequences
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI generation failed: {e}")
            raise
    
    def generate_stream(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        stop_sequences: Optional[List[str]] = None
    ):
        """
        Generate text with streaming using OpenAI API.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            stop_sequences: Sequences to stop generation
            
        Yields:
            Text chunks as they are generated
        """
        try:
            self.logger.debug(f"Streaming generation with {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop_sequences,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            self.logger.error(f"OpenAI streaming failed: {e}")
            raise
    
    def is_available(self) -> bool:
        """
        Check if OpenAI service is available.
        
        Returns:
            True if service is accessible
        """
        try:
            # Simple test request
            self.client.models.list()
            return True
        except Exception as e:
            self.logger.warning(f"OpenAI availability check failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Model information dictionary
        """
        return {
            "provider": "openai",
            "model": self.model,
            "api_key_configured": bool(self.api_key),
            "base_url": self.base_url or "https://api.openai.com/v1",
            "timeout": self.timeout
        }