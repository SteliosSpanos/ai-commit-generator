# AI Git Commit Message Generator

An intelligent git hook that automatically generates conventional commit messages using AI by analyzing your staged changes.

## Features

- 🤖 **AI-Powered**: Uses OpenAI GPT-4 to understand your code changes
- 📝 **Conventional Commits**: Generates properly formatted conventional commit messages
- 🔧 **Easy Setup**: Simple installation and configuration
- 🧠 **Context Aware**: Understands different project types (Python, Node.js, etc.)
- ⚡ **Fast**: Quick generation with smart diff truncation
- 🛠️ **Flexible**: Can be used as a git hook or standalone tool

## Installation

### Prerequisites

- Python 3.8+
- Git
- OpenAI API key

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-commit-generator.git
   cd ai-commit-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Install the git hook in your project**
   ```bash
   cd /path/to/your/project
   python /path/to/ai-commit-generator/install_hook.py install
   ```

## Usage

### As a Git Hook (Automatic)

Once installed, the hook will automatically generate commit messages:

```bash
git add .
git commit  # Message will be auto-generated!
```

### As a Standalone Tool

```bash
# Generate message for staged changes
python commit_generator.py

# Dry run (just show the message)
python commit_generator.py --dry-run

# Use custom diff
python commit_generator.py --diff "your diff content here"
```

## Configuration

Set these environment variables in your `.env` file:

```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional
AI_COMMIT_MODEL=gpt-4                    # OpenAI model to use
AI_COMMIT_MAX_DIFF_LENGTH=8000          # Max diff length to send to AI
AI_COMMIT_TEMPERATURE=0.3               # AI creativity (0.0-1.0)
```

## Example Output

The tool generates conventional commit messages like:

- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null user response`
- `docs: update installation guide`
- `refactor(utils): extract validation logic`
- `test(auth): add login component tests`

## How It Works

1. **Analyzes** your staged git changes
2. **Detects** project type and context
3. **Sends** diff to OpenAI with carefully crafted prompt
4. **Generates** a conventional commit message
5. **Sets** it as your commit message

## Supported Project Types

The tool automatically detects and optimizes for:

- Python (requirements.txt, pyproject.toml)
- Node.js (package.json)
- Java (pom.xml)
- Rust (Cargo.toml)
- Go (go.mod)
- PHP (composer.json)

## Uninstall

To remove the git hook:

```bash
python install_hook.py uninstall
```

## Development

### Running Tests

```bash
# Test with sample diff
python commit_generator.py --diff "$(git diff HEAD~1)"
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Troubleshooting

### "OpenAI API key not set"
Make sure your `.env` file contains `OPENAI_API_KEY=your_key_here`

### "Git not found"
Ensure git is installed and in your PATH

### "No staged changes found"
Make sure you've staged files with `git add` before committing

### Hook not working
- Verify the hook is executable: `ls -la .git/hooks/prepare-commit-msg`
- Check the hook content references the correct script path
- Ensure Python dependencies are installed

## Roadmap

1. Support for other LLM providers (Anthropic, local models)
2. Configuration file support
3. Better handling of large repositories
4. Integration with popular git GUIs
5. Custom prompt templates