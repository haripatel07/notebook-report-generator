# Quick Start Guide

## Prerequisites

```bash
python3 --version  # Should be 3.9 or higher
git --version      # Should be installed
```

## Installation

```bash
# Clone the repository
git clone https://github.com/haripatel07/report-generator.git
cd report-generator

# Run automated setup
./scripts/setup.sh

# This creates virtual environment and installs dependencies
```

## LLM Setup

### Using Ollama

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in one terminal
ollama serve

# In another terminal, pull a model
ollama pull llama2  # Or: mistral, codellama
```

### Using OpenAI

Edit `.env` file:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

## Generate Report

```bash
# Activate virtual environment
source venv/bin/activate

# Generate from a notebook
python src/main.py \
  --input path/to/your/notebook.ipynb \
  --type academic \
  --format docx

# Or use the example
python src/main.py \
  --input examples/input/ml_classification.ipynb \
  --type academic \
  --format docx \
  --output my_first_report.docx
```

## Process

The system:
1. Parses Jupyter notebook
2. Extracts code, markdown, and results
3. Analyzes project context
4. Generates report sections
5. Creates workflow diagrams
6. Adds citations
7. Formats output

## Common Use Cases

### Academic Lab Report

```bash
python src/main.py \
  --input lab_notebook.ipynb \
  --type academic \
  --format docx \
  --title "Machine Learning Lab Report" \
  --institution "University Name"
```

### Internship Report

```bash
python src/main.py \
  --input project_folder/ \
  --type internship \
  --format pdf \
  --title "ML Internship - Week 4 Report" \
  --include-code-snippets
```

### Industry Documentation

```bash
python src/main.py \
  --input src/ \
  --type industry \
  --format markdown \
  --diagram-style detailed
```

### Generate All Formats

```bash
python src/main.py \
  --input notebook.ipynb \
  --format all
```

## Output Files

Find your generated reports in:
```
output/
├── technical_report.docx
├── technical_report.pdf
└── technical_report.md
```

## Customization

### Configure Settings

Edit `config/default_config.yaml`:

```yaml
report:
  include_abstract: true
  include_table_of_contents: true
  max_code_snippet_lines: 50
  citation_style: ieee

llm:
  model: llama2
  temperature: 0.7
```

### Environment Variables

Edit `.env`:
```
LLM_MODEL=mistral
REPORT_TYPE=academic
DIAGRAM_STYLE=detailed
```

## Troubleshooting

### "Ollama not found"
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x scripts/setup.sh
```

### "LLM timeout"
Increase timeout in config:
```yaml
llm:
  timeout: 300  # 5 minutes
```

## Next Steps

- Read the [full documentation](docs/)
- Customize [configuration](docs/CONFIGURATION.md)
- Explore [examples](examples/)
- [Contribute](CONTRIBUTING.md) to the project

## Getting Help

- Open an [issue](https://github.com/haripatel07/report-generator/issues)
- Check [discussions](https://github.com/haripatel07/report-generator/discussions)
- Read the [documentation](docs/)

## Quick Reference

### Command Options

```bash
--input, -i        Input file or directory
--output, -o       Output file path
--type, -t         Report type (academic|internship|industry|research)
--format, -f       Output format (docx|pdf|markdown|all)
--title            Custom report title
--institution      Institution/organization name
--include-code-snippets    Include code in report
--diagram-style    Diagram detail (minimal|standard|detailed)
--verbose, -v      Verbose logging
```

### Example Commands

```bash
# Minimal
python src/main.py -i notebook.ipynb

# Full options
python src/main.py \
  -i notebook.ipynb \
  -o report.docx \
  -t academic \
  -f docx \
  --title "My Project" \
  --institution "My University" \
  --include-code-snippets \
  --diagram-style detailed \
  -v
```
