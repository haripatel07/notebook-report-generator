# Deployment Guide

## Project Structure

```
report-generator/
├── src/                    # Source code
│   ├── agents/            # Multi-agent system
│   ├── parsers/           # Input file parsers
│   ├── formatters/        # Output formatters
│   ├── llm/              # LLM integration
│   └── utils/            # Utilities
├── config/                # Configuration files
├── tests/                 # Test suite
├── docs/                  # Documentation
└── scripts/               # Setup scripts
```

## Development Workflow

### Local Development

```bash
cd report-generator
source venv/bin/activate
# Make changes
pytest tests/
git add .
git commit -m "description"
git push
```

### Adding Features

```bash
git checkout -b feature/feature-name
# Implement and test
git commit -m "feat: description"
git push origin feature/feature-name
```

## Testing

```bash
pytest tests/ -v
```

## Configuration

### Report Templates

```yaml
# config/report_templates.yaml
academic:
  sections:
    - title
    - abstract
    - introduction
    - methodology
    - results
    - conclusion
    - references
```

### LLM Prompts

```yaml
# config/llm_prompts.yaml
writer_prompts:
  methodology: |
    Generate the Methodology section.
    Context: {context}
    Guidelines:
    - Explain methods and rationale
    - Reference implementation
    - Be concise
```

## Resources

- [Quick Start](docs/QUICKSTART.md)
- [Installation](docs/INSTALLATION.md)
- [Contributing](CONTRIBUTING.md)
