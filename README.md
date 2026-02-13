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
# Clone and setup
git clone https://github.com/haripatel07/report-generator.git
cd report-generator
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup LLM (pick one)
ollama pull llama3                    # easiest
export OPENAI_API_KEY="your_key"      # or this
export GROQ_API_KEY="your_key"        # or this

# Generate a report
python src/main.py --input notebook.ipynb --type academic --format docx
```

See the LLM Setup section below if you need help with the model setup.

## Requirements

- Python 3.9+
- Local LLM (Ollama) or OpenAI-compatible API
- 8GB+ RAM
- Storage for model weights

## Installation

See [INSTALLATION.md](docs/INSTALLATION.md) for detailed setup instructions.

## LLM Setup

This tool needs an LLM to generate reports. Pick one:

### Using Ollama (easiest option)

If you haven't used LLMs before, start here. It's free and runs locally.

```bash
# Install from https://ollama.com
ollama pull llama3
ollama list  # verify it's installed
```

The tool will use Ollama automatically if you don't set an API key.

### Using OpenAI

You'll need an API key and it costs money per request.

1. Get a key from https://platform.openai.com/api-keys
2. Set it in your environment:

```bash
# Mac/Linux
export OPENAI_API_KEY="your_key_here"

# Windows PowerShell
setx OPENAI_API_KEY "your_key_here"
```

Or just create a `.env` file in the project root:
```
OPENAI_API_KEY=your_key_here
```

**Important:** Restart your terminal after setting the variable.

### Using Groq (free alternative)

Similar to OpenAI but with a generous free tier.

1. Get a key from https://console.groq.com
2. Set it the same way:

```bash
export GROQ_API_KEY="your_key_here"
# or add to .env file
```

### Testing

```bash
# If using Ollama
ollama run llama3 "test"

# Otherwise just try running
python src/main.py --help
```

Common issues:
- Forgot to restart terminal after setting API key
- Ollama not running (check with `ollama list`)
- Wrong API key or typo in .env file

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
