# Project Structure

report-generator/
├── .github/
│   ├── workflows/
│   │   ├── tests.yml
│   │   └── release.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── src/
│   ├── __init__.py
│   ├── main.py                      # Entry point
│   ├── cli.py                       # Command-line interface
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py            # Base agent class
│   │   ├── analyzer_agent.py        # Analyzes input files
│   │   ├── writer_agent.py          # Generates report sections
│   │   ├── diagram_agent.py         # Creates visualizations
│   │   ├── citation_agent.py        # Manages references
│   │   └── orchestrator.py          # Coordinates all agents
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── notebook_parser.py       # Jupyter notebook parsing
│   │   ├── code_parser.py           # Python code analysis
│   │   ├── dataset_parser.py        # Dataset metadata extraction
│   │   └── markdown_parser.py       # Markdown file parsing
│   │
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── content_generator.py     # Core content generation
│   │   ├── section_generator.py     # Individual sections
│   │   ├── diagram_generator.py     # Mermaid/Graphviz diagrams
│   │   └── table_generator.py       # Result tables
│   │
│   ├── formatters/
│   │   ├── __init__.py
│   │   ├── docx_formatter.py        # DOCX output
│   │   ├── pdf_formatter.py         # PDF generation
│   │   ├── markdown_formatter.py    # Markdown output
│   │   └── style_templates.py       # Styling templates
│   │
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── context_extractor.py     # Extract context from files
│   │   ├── code_analyzer.py         # Analyze code structure
│   │   ├── result_analyzer.py       # Parse experimental results
│   │   └── workflow_detector.py     # Detect project workflow
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── llm_interface.py         # Abstract LLM interface
│   │   ├── ollama_client.py         # Ollama integration
│   │   ├── openai_client.py         # OpenAI-compatible API
│   │   └── prompt_templates.py      # Prompt engineering
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py                # Configuration management
│       ├── logger.py                # Logging setup
│       ├── validators.py            # Input validation
│       ├── file_utils.py            # File operations
│       └── plagiarism_checker.py    # Originality verification
│
├── config/
│   ├── default_config.yaml          # Default configuration
│   ├── report_templates.yaml        # Report structure templates
│   ├── style_guidelines.yaml        # Writing style rules
│   └── llm_prompts.yaml             # LLM system prompts
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── test_parsers.py
│   ├── test_agents.py
│   ├── test_generators.py
│   ├── test_formatters.py
│   └── fixtures/                    # Test data
│       ├── sample_notebook.ipynb
│       ├── sample_code.py
│       └── sample_dataset.csv
│
├── docs/
│   ├── INSTALLATION.md
│   ├── CONFIGURATION.md
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   └── examples/
│       ├── academic_report.md
│       ├── internship_report.md
│       └── industry_report.md
│
├── examples/
│   ├── input/
│   │   ├── ml_classification.ipynb
│   │   ├── data_analysis.ipynb
│   │   └── deep_learning_project/
│   └── output/
│       ├── academic_lab_report.docx
│       ├── internship_report.pdf
│       └── technical_documentation.md
│
├── scripts/
│   ├── setup.sh                     # Setup script
│   ├── install_ollama.sh            # Ollama installation
│   └── run_tests.sh                 # Test runner
│
├── .gitignore
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── pyproject.toml
├── LICENSE
├── CHANGELOG.md
└── README.md
