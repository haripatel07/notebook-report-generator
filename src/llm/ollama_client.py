"""
Ollama LLM client implementation.
"""

import requests
from typing import List, Optional

from src.llm.llm_interface import LLMInterface
from src.utils.logger import setup_logger


class OllamaClient(LLMInterface):
    """
    Ollama LLM client for local model inference.
    """
    
    def __init__(
        self,
        model: str = "llama2",
        base_url: str = "http://localhost:11434",
        timeout: int = 120
    ):
        """
        Initialize Ollama client.
        
        Args:
            model: Model name (e.g., "llama2", "mistral", "codellama")
            base_url: Ollama API base URL
            timeout: Request timeout in seconds
        """
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = setup_logger(self.__class__.__name__)
        
        self.api_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        stop_sequences: Optional[List[str]] = None
    ) -> str:
        """Generate text using Ollama."""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        if stop_sequences:
            payload["options"]["stop"] = stop_sequences
        
        try:
            self.logger.debug(f"Sending request to Ollama: {self.model}")
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timed out after {self.timeout}s")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ):
        """Generate text with streaming."""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    import json
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
                        
        except Exception as e:
            self.logger.error(f"Streaming failed: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def get_model_info(self) -> dict:
        """Get model information."""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": self.model},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except:
            return {"model": self.model, "status": "unknown"}
    
    def pull_model(self, model: Optional[str] = None):
        """
        Pull/download a model.
        
        Args:
            model: Model name to pull (uses self.model if not specified)
        """
        model_name = model or self.model
        
        self.logger.info(f"Pulling model: {model_name}")
        
        payload = {"name": model_name, "stream": False}
        
        response = requests.post(
            f"{self.base_url}/api/pull",
            json=payload,
            timeout=600  # 10 minutes for large models
        )
        
        if response.status_code == 200:
            self.logger.info(f"Model {model_name} pulled successfully")
        else:
            self.logger.error(f"Failed to pull model: {response.text}")
            raise RuntimeError(f"Model pull failed: {response.text}")
