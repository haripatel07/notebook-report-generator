# GitHub Setup Guide

## Prerequisites

- GitHub account
- Git installed
- Project files

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to [https://github.com/new](https://github.com/new)
2. Fill in repository details:
   - **Repository name**: `report-generator` (or your preferred name)
   - **Description**: "Automated Local AI Agent for Technical Report Generation"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

### Option B: Using GitHub CLI

```bash
# Install GitHub CLI if not already installed
# Visit: https://cli.github.com/

# Authenticate
gh auth login

# Create repository
gh repo create report-generator --public --source=. --remote=origin

# Or for private:
gh repo create report-generator --private --source=. --remote=origin
```

## Step 2: Initialize Local Git Repository

Run the initialization script:

```bash
cd report-generator
./scripts/init_git.sh
```

This will:
- Initialize git repository
- Configure your name and email
- Create initial commit
- Set up main branch

Or do it manually:

```bash
# Initialize repository
git init

# Configure git
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Project structure and core backend"

# Rename branch to main
git branch -M main
```

## Step 3: Connect to GitHub

After creating your GitHub repository, connect it:

```bash
# Add remote (replace with your repository URL)
git remote add origin https://github.com/haripatel07/report-generator.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

## Step 4: Verify Upload

1. Go to your GitHub repository
2. Refresh the page
3. You should see all your files!

## Step 5: Set Up GitHub Features

### Enable GitHub Actions

1. Go to "Actions" tab in your repository
2. GitHub Actions should be automatically enabled
3. The tests workflow will run on every push

### Add Repository Description

1. Go to repository main page
2. Click settings icon next to "About"
3. Add:
   - **Description**: "Technical report generator from Jupyter notebooks"
   - **Website**: Your documentation site (if any)
   - **Topics**: `machine-learning`, `report-generation`, `jupyter-notebook`, `technical-writing`

### Create Repository Labels

```bash
# Using GitHub CLI
gh label create "enhancement" --description "New feature" --color "0E8A16"
gh label create "bug" --description "Bug fix" --color "D73A4A"
gh label create "documentation" --description "Documentation" --color "0075CA"
gh label create "good first issue" --description "Good for newcomers" --color "7057FF"
```

### Enable Issue Templates

Already included in `.github/ISSUE_TEMPLATE/`

### Enable Discussions (Optional)

1. Go to Settings → Features
2. Check "Discussions"

## Step 6: Add README Badges

Update your README.md with badges:

```markdown
# Technical Report Generator

[![Tests](https://github.com/haripatel07/report-generator/workflows/Tests/badge.svg)](https://github.com/haripatel07/report-generator/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

## Step 7: Protect Main Branch

1. Go to Settings → Branches
2. Add branch protection rule:
   - **Branch name pattern**: `main`
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging

## Ongoing Workflow

### Making Changes

```bash
# Create a new branch
git checkout -b feature/your-feature

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/your-feature

# Create Pull Request on GitHub
```

### Syncing with Remote

```bash
# Pull latest changes
git pull origin main

# Push your changes
git push origin main
```

### Tagging Releases

```bash
# Create a tag
git tag -a v0.1.0 -m "Initial release"

# Push tag
git push origin v0.1.0

# Or push all tags
git push origin --tags
```

## Common Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# View branches
git branch -a

# Switch branch
git checkout branch-name

# Delete branch
git branch -d branch-name

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View changes
git diff
```

## Troubleshooting

### "Permission denied (publickey)"

Set up SSH keys:
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add this to GitHub → Settings → SSH Keys
```

### "Repository not found"

Check remote URL:
```bash
git remote -v
git remote set-url origin https://github.com/haripatel07/report-generator.git
```

### "refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

## Next Steps

After pushing to GitHub:

1. Star your own repository
2. Create first issue or enhancement
3. Customize README with screenshots
4. Add example notebooks
5. Share with community

## GitHub Best Practices

- Write clear commit messages
- Use meaningful branch names
- Keep commits small and focused
- Review your own PRs before requesting reviews
- Respond to issues promptly
- Keep documentation updated
- Use GitHub Projects for task management

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI](https://cli.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
