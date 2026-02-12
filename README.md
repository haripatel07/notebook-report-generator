# Notebook Report Generator

Converts Jupyter notebooks, source code, and experimental results into technical reports in multiple formats.

## Purpose

Automates technical report creation for:
- Lab reports and semester projects
- Internship documentation
- Technical documentation
- Research summaries

## Features

- Local LLM support (Ollama) and cloud API compatibility
- Multiple output formats: DOCX, PDF, Markdown
- Diagram generation from code structure
- Citation management
- Configurable report templates

## Architecture

```
Input (Notebooks, Code, Data)
    ↓
Document Parser & Analyzer
    ↓
Context Extraction Engine
    ↓
Multi-Agent Report Generator
    ↓
Diagram Generator
    ↓
Output Formatter (DOCX/PDF)
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/haripatel07/report-generator.git
cd report-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the system
python src/main.py --input path/to/notebook.ipynb --type academic --format docx
```

## Requirements

- Python 3.9+
- Local LLM (Ollama) or OpenAI-compatible API
- 8GB+ RAM
- Storage for model weights

## Installation

See [INSTALLATION.md](docs/INSTALLATION.md) for detailed setup instructions.

## Usage

### Basic Usage

```bash
python src/main.py \
  --input project/notebook.ipynb \
  --type academic \
  --format docx \
  --output report.docx
```

### Advanced Options

```bash
python src/main.py \
  --input project/ \
  --type internship \
  --format pdf \
  --title "Machine Learning Internship Report" \
  --institution "XYZ University" \
  --include-code-snippets \
  --diagram-style detailed
```

## Report Types

- `academic`: University lab reports, course projects
- `internship`: Weekly and final internship reports
- `industry`: Professional technical documentation
- `research`: Research paper drafts and summaries

## Project Structure

```
report-generator/
├── src/
│   ├── agents/          # Multi-agent system
│   ├── parsers/         # Input file parsers
│   ├── generators/      # Content generators
│   ├── formatters/      # Output formatters
│   └── utils/           # Utilities
├── config/              # Configuration files
├── tests/               # Unit and integration tests
├── docs/                # Documentation
└── examples/            # Example inputs/outputs
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
