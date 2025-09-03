import os
import sys
import subprocess
from pathlib import Path

def find_git_root():
    """Find the git repository root"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository", file=sys.stderr)
        sys.exit(1)

def install_hook():
    """Install the prepare-commit-msg hook"""
    git_root = find_git_root()
    hooks_dir = git_root / ".git" / "hooks"
    hook_path = hooks_dir / "prepare-commit-msg"

    hooks_dir.mkdir(exist_ok=True)

    script_dir = Path(__file__).parent
    commit_generator_path = script_dir / "commit_generator.py"

    hook_content = f"""#!/bin/bash
# AI Commit Message Generator Hook

# Enable debugging (remove these lines in production)
exec 2> >(tee -a /tmp/git-hook-debug.log)
echo "Hook started at $(date)" >&2
echo "Arguments: $1 $2 $3" >&2

# Only run for regular commits (not merges, rebases, etc.)
if [ "$2" == "" ] || [ "$2" == "message" ]; then
    echo "Running AI commit generator..." >&2
    
    # Check if python3 is available
    if command -v python3 &> /dev/null; then
        echo "Using python3" >&2
        python3 "{commit_generator_path.absolute()}" --message-file "$1" 2>&1
        exit_code=$?
    elif command -v python &> /dev/null; then
        echo "Using python" >&2
        python "{commit_generator_path.absolute()}" --message-file "$1" 2>&1
        exit_code=$?
    else
        echo "Error: Python not found" >&2
        exit 1
    fi
    
    echo "Hook completed with exit code: $exit_code" >&2
    exit $exit_code
else
    echo "Skipping hook (merge/rebase/etc.)" >&2
fi
"""

    with open(hook_path, "w") as f:
        f.write(hook_content)

    os.chmod(hook_path, 0o755)

    print(f"✅ Git hook installed successfully!")
    print(f"Hook location: {hook_path}")
    print("\nThe hook will now automatically generate commit messages for your commits.")
    print("Make sure you have:")
    print("1. Set OPENAI_API_KEY in your environment or .env file")
    print("2. Installed required Python packages: pip install -r requirements.txt")

def uninstall_hook():
    """Uninstall the prepare-commit-msg hook"""
    git_root = find_git_root()
    hook_path = git_root / ".git" / "hooks" / "prepare-commit-msg"

    if hook_path.exists():
        with open(hook_path, "r") as f:
            content = f.read()

        if "AI Commit Message Generator Hook" in content:
            hook_path.unlink()
            print("✅ Git hook uninstalled successfully!")
        else:
            print("⚠️ Found a different prepare-commit-msg hook. Not removing it.")
            print(f"Hook location: {hook_path}")
    else:
        print("No prepare-commit-msg hook found.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python install_hook.py [install|uninstall]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "install":
        install_hook()
    elif command == "uninstall":
        uninstall_hook()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python install_hook.py [install|uninstall]")
        sys.exit(1)

if __name__ == "__main__":
    main()