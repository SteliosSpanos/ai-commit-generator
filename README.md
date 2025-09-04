# AI Commit Generator 🤖

Generate intelligent, conventional commit messages using AI. This tool analyzes your staged changes and creates meaningful commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## ✨ Features

- 🤖 **AI-Powered**: Uses OpenAI's GPT models to analyze your code changes
- 📝 **Conventional Commits**: Follows the standard format (`type(scope): description`)
- 🔍 **Smart Analysis**: Detects project type and provides contextual commit messages
- ⚡ **Fast & Reliable**: Simple command-line interface that always works
- 🛡️ **Safe**: Interactive confirmation before committing
- 🚀 **Flexible**: Supports dry-run mode and auto-push options

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/SteliosSpanos/ai-commit-generator.git
cd ai-commit-generator

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Configure OpenAI API Key

Get your API key from [OpenAI](https://platform.openai.com/api-keys) and add it to `.env`:

```bash
OPENAI_API_KEY=your_api_key_here
AI_COMMIT_MODEL=gpt-4
```

### 3. Basic Usage

```bash
# Stage your changes
git add .

# Generate and commit with AI
python3 ai_commit.py

# Just see the generated message (no commit)
python3 ai_commit.py --dry-run

# Commit and push automatically
python3 ai_commit.py --push
```

## 📋 Usage Examples

### Basic Workflow
```bash
# Make some changes to your code
echo "console.log('Hello World');" >> app.js

# Stage the changes
git add app.js

# Generate AI commit message and commit
python3 ai_commit.py
```

**Output:**
```
📝 Staged files: app.js
🤖 Generated message: feat(app): add hello world console log
Commit with this message? [Y/n]: y
✅ Commit successful!
```

### Advanced Usage

```bash
# Dry run - see message without committing
python3 ai_commit.py --dry-run

# Commit and push in one command
python3 ai_commit.py --push

# Use with different models (in .env)
AI_COMMIT_MODEL=gpt-3.5-turbo
```

## ⚙️ Configuration Options

Create a `.env` file in your project root:

```env
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional configurations
AI_COMMIT_MODEL=gpt-4     
AI_COMMIT_MAX_DIFF_LENGTH=8000   # Maximum diff length to analyze
AI_COMMIT_TEMPERATURE            # Creativity (0.0 - 1.0)
```

## 🛠️ Installation Methods

### Method 1: Direct Usage (Recommended)
```bash
# From any git repository
python3 /path/to/ai-commit-generator/ai_commit.py
```

### Method 2: Git Alias
```bash
# Set up a global git alias
git config --global alias.aic '!python3 /path/to/ai-commit-generator/ai_commit.py'

# Now use anywhere
git aic
git aic --dry-run
git aic --push
```

### Method 3: System Alias
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
alias aic="python3 /path/to/ai-commit-generator/ai_commit.py"
```

## 📝 Commit Message Examples

The AI generates messages following conventional commits:

| Change Type | Generated Message |
|-------------|-------------------|
| New feature | `feat(auth): add OAuth login flow` |
| Bug fix | `fix(api): handle null user response` |
| Documentation | `docs: update installation guide` |
| Refactoring | `refactor(utils): extract validation logic` |
| Tests | `test(auth): add login component tests` |
| Dependencies | `chore(deps): update axios to v1.5.0` |

## 🎯 Supported Project Types

The AI automatically detects your project type for better context:

- **JavaScript/Node.js**: `package.json`
- **Python**: `requirements.txt`, `pyproject.toml`
- **Java**: `pom.xml`
- **Rust**: `Cargo.toml`
- **Go**: `go.mod`
- **PHP**: `composer.json`

## 🔧 Troubleshooting

### Common Issues

**"No staged changes found"**
```bash
# Make sure you've staged your changes
git add .
git status  # Should show "Changes to be committed"
```

**"OpenAI API error"**
```bash
# Check your API key in .env
cat .env | grep OPENAI_API_KEY

# Test your API key
python3 -c "import openai; openai.api_key='your-key'; print('API key works!')"
```

**"Permission denied"**
```bash
# Make the script executable
chmod +x ai_commit.py
```

### Debug Mode

For troubleshooting, you can add debug output:
```python
# Temporarily add to ai_commit.py
import os
print(f"Working dir: {os.getcwd()}")
print(f"API Key set: {bool(os.getenv('OPENAI_API_KEY'))}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit using the AI tool: `python3 ai_commit.py`
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for developers who want better commit messages!!**