#!/bin/bash

# Git Repository Initialization Script

set -e

echo "==================================="
echo "Initializing Git Repository"
echo "==================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed"
    echo "Install git from: https://git-scm.com/downloads"
    exit 1
fi

# Initialize git repository
if [ -d .git ]; then
    echo "[INFO] Git repository already initialized"
else
    echo "Initializing git repository..."
    git init
    echo "[OK] Git repository initialized"
fi
echo ""

# Configure git (optional)
echo "Configuring git..."
read -p "Enter your name (for git commits): " git_name
read -p "Enter your email (for git commits): " git_email

git config user.name "$git_name"
git config user.email "$git_email"
echo "[OK] Git configured"
echo ""

# Add all files
echo "Adding files to git..."
git add .
echo "[OK] Files added"
echo ""

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: Project structure and core backend"
echo "[OK] Initial commit created"
echo ""

# Create main branch (if needed)
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "Renaming branch to main..."
    git branch -M main
    echo "[OK] Branch renamed to main"
fi
echo ""

echo "==================================="
echo "Git Repository Ready!"
echo "==================================="
echo ""
echo "Next steps to push to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Add remote and push:"
echo "   git remote add origin https://github.com/yourusername/report-generator.git"
echo "   git push -u origin main"
echo ""
echo "Or if you already have a repo:"
echo "   git remote add origin YOUR_REPO_URL"
echo "   git push -u origin main"
echo ""
