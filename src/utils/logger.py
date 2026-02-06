"""
Logging configuration for the report generator.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Setup logger with rich formatting.
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler with rich formatting
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_path=False
    )
    console_handler.setLevel(getattr(logging, level.upper()))
    
    console_format = logging.Formatter(
        "%(message)s",
        datefmt="[%X]"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


class ProgressLogger:
    """Progress logger for multi-step operations."""
    
    def __init__(self, logger: logging.Logger, total_steps: int):
        self.logger = logger
        self.total_steps = total_steps
        self.current_step = 0
    
    def step(self, message: str):
        """Log a step with progress."""
        self.current_step += 1
        progress = f"[{self.current_step}/{self.total_steps}]"
        self.logger.info(f"{progress} {message}")
    
    def complete(self, message: str = "All steps completed"):
        """Log completion."""
        self.logger.info(f"{message}")
