# Installation Guide

## Prerequisites

- **Python 3.9+**
- **8GB+ RAM**
- **Git**
- **Ollama** (for local LLM) OR **OpenAI API key**

## Quick Install

### 1. Clone the Repository

```bash
git clone https://github.com/haripatel07/report-generator.git
cd report-generator
```

### 2. Run Setup Script

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create necessary directories
- Set up configuration files

### 3. Configure Environment

Edit the `.env` file with your settings:

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

### 4. Install LLM Backend

#### Option A: Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull a model (in a new terminal)
ollama pull llama2
# or for better quality:
ollama pull mistral
```

#### Option B: OpenAI API

Update your `.env` file:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

## Manual Installation

If you prefer to install manually:

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create Directories

```bash
mkdir -p output .cache logs
```

### 4. Configure

```bash
cp .env.example .env
# Edit .env with your settings
```

## Verification

Test your installation:

```bash
# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running (if using Ollama)
curl http://localhost:11434/api/tags

# Run a simple test
python src/main.py --help
```

You should see the help message with all available options.

## Troubleshooting

### Issue: "Ollama is not running"

**Solution:**
```bash
ollama serve
```
Keep this terminal open and run your commands in a new terminal.

### Issue: "Module not found"

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Permission denied" on scripts

**Solution:**
```bash
chmod +x scripts/setup.sh
```

### Issue: Python version too old

**Solution:**
Install Python 3.9+ from [python.org](https://www.python.org/downloads/)

## Next Steps

Once installed, see the [Usage Guide](docs/USAGE.md) for how to generate reports.

## Upgrading

To upgrade to the latest version:

```bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove the project directory
cd ..
rm -rf report-generator
```
