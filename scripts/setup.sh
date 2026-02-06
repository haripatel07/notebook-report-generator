#!/bin/bash

# Setup script for Report Generator

set -e

echo "==================================="
echo "Report Generator Setup"
echo "==================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "Error: Python 3.9 or higher is required (found $python_version)"
    exit 1
fi
echo "[OK] Python $python_version found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "[OK] Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "[OK] Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "[OK] pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "[OK] Dependencies installed"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p output
mkdir -p .cache
mkdir -p logs
echo "[OK] Directories created"
echo ""

# Copy environment template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "[OK] .env file created (please configure it)"
else
    echo "[INFO] .env file already exists (skipping)"
fi
echo ""

# Check Ollama installation
echo "Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "[OK] Ollama is installed"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "[OK] Ollama service is running"
    else
        echo "[INFO] Ollama is installed but not running"
        echo "  Start it with: ollama serve"
    fi
else
    echo "[INFO] Ollama is not installed"
    echo "  Install it with: ./scripts/install_ollama.sh"
fi
echo ""

echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Configure .env file with your settings"
echo "2. If using Ollama, install a model:"
echo "   ollama pull llama2"
echo "3. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "4. Run the generator:"
echo "   python src/main.py --input notebook.ipynb"
echo ""
