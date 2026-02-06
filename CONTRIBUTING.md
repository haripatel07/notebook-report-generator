# Contributing

Guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment

## How to Contribute

### Reporting Bugs

Check if the bug has already been reported in [Issues](https://github.com/haripatel07/report-generator/issues). If not, create a new issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, LLM provider)
- Relevant logs or error messages

### Suggesting Features

Check existing feature requests first. Create a new issue with:
- Clear use case
- Expected behavior
- Rationale for the feature

### Contributing Code

#### 1. Fork and Clone

```bash
git clone https://github.com/haripatel07/report-generator.git
cd report-generator
git remote add upstream https://github.com/original/report-generator.git
```

#### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 3. Make Changes

- Follow the existing code style
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed

#### 4. Run Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Check code style
flake8 src tests

# Run type checking
mypy src
```

#### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve bug in parser"
```

Commit message format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test updates
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

#### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues
- Screenshots/examples if applicable

## Development Setup

### Prerequisites

- Python 3.9+
- Virtual environment
- Git

### Setup

```bash
# Clone your fork
git clone https://github.com/haripatel07/report-generator.git
cd report-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pre-commit install
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to all functions/classes

### Example

```python
"""
Module description.
"""

from typing import List, Optional


def process_notebook(
    notebook_path: str,
    output_format: str = "docx"
) -> Optional[List[str]]:
    """
    Process a Jupyter notebook.
    
    Args:
        notebook_path: Path to the notebook file
        output_format: Desired output format
        
    Returns:
        List of generated file paths, or None if failed
        
    Raises:
        FileNotFoundError: If notebook doesn't exist
    """
    # Implementation
    pass
```

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Include both positive and negative cases

### Example Test

```python
import pytest
from src.parsers.notebook_parser import NotebookParser


def test_parse_notebook_success():
    """Test successful notebook parsing."""
    parser = NotebookParser()
    result = parser.parse("tests/fixtures/sample.ipynb")
    
    assert result is not None
    assert "cells" in result
    assert len(result["cells"]) > 0


def test_parse_notebook_invalid_file():
    """Test parsing with invalid file."""
    parser = NotebookParser()
    
    with pytest.raises(FileNotFoundError):
        parser.parse("nonexistent.ipynb")
```

## Documentation

### Updating Documentation

- Keep README.md up to date
- Update relevant docs in `docs/`
- Add docstrings to new code
- Include usage examples

### Documentation Structure

```
docs/
├── INSTALLATION.md   # Installation guide
├── CONFIGURATION.md  # Configuration options
├── API.md           # API documentation
├── ARCHITECTURE.md  # System architecture
└── examples/        # Usage examples
```

## Project Structure

Understanding the codebase:

```
src/
├── agents/          # Multi-agent system
├── parsers/         # Input file parsers
├── generators/      # Content generators
├── formatters/      # Output formatters
├── llm/            # LLM integration
└── utils/          # Utilities
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add entry to CHANGELOG.md
4. Request review from maintainers
5. Address review feedback
6. Wait for appro
5. Address feedback

## Questions

By contributing, you agree that your contributions will be licensed under the MIT License.
