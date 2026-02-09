# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced DOCX formatter with professional formatting
  - Improved title page with custom typography and colors
  - Proper heading hierarchy (H1 for main sections, H2 for subsections)
  - Markdown table parsing and conversion to styled Word tables
  - Support for bold, italic, and inline code formatting
  - Bullet and numbered list handling
  - Code block formatting with monospace fonts
- Enhanced PDF formatter with professional formatting
  - Professional title page with custom styling and colors
  - Markdown table rendering with styled ReportLab tables
  - Custom style definitions for consistent typography
  - Improved spacing with proper margins and padding
  - Inline markdown parsing (bold, italic, code)
- New DiagramRenderer utility for Mermaid diagram support
  - Support for mermaid-cli (mmdc) rendering
  - Support for playwright-based rendering
  - Automatic fallback to code blocks when renderers unavailable
  - Converts Mermaid diagrams to PNG images for embedding
- Comprehensive formatter test suite
  - 9 automated tests covering all formatters
  - Tests for structure, tables, headings, and diagrams
  - Integration tests and edge case handling
- Expanded AnalyzerAgent capabilities
  - Enhanced markdown outline extraction
  - Improved dataset details capture
  - Structured evaluation metrics extraction
- Enhanced WriterAgent with richer context handling
  - Professional section generation with accurate metric tables
  - Improved narrative quality

### Changed
- Updated requirements.txt to include playwright for diagram rendering
- Modified work_status.md to reflect completed tasks

### Planned
- Advanced diagram customization (themes, colors, custom styles)
- Support for additional diagram types (PlantUML, D2)
- PDF bookmarks and hyperlinks for better navigation
- Custom document templates and branding
- Export to additional formats (HTML, LaTeX)
- Advanced plagiarism detection
- Multi-language support
- Web-based UI

## [0.1.0] - 2024-01-XX

### Added
- Initial project structure
- Core backend architecture
- Multi-agent system framework
- Jupyter notebook parser
- LLM integration (Ollama and OpenAI)
- Configuration management system
- CLI interface with Rich formatting
- Logging and progress tracking
- DOCX, PDF, and Markdown formatters (stubs)
- Comprehensive documentation
- GitHub Actions CI/CD setup
- Installation and setup scripts

### Features
- Parse Jupyter notebooks and extract context
- Generate technical reports using local LLM
- Support for multiple report types (academic, internship, industry, research)
- Configurable output formats
- Plagiarism prevention framework

### Documentation
- Installation guide
- Contributing guidelines
- Project structure documentation
- README with quick start

### Infrastructure
- Git repository structure
- GitHub Actions workflows
- Setup automation scripts
- Development environment configuration

[Unreleased]: https://github.com/haripatel07/report-generator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/haripatel07/report-generator/releases/tag/v0.1.0
