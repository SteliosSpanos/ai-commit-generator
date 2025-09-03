import subprocess
import sys
import os
import argparse
from commit_generator import CommitGenerator, load_config

def run_git_command(command):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="AI-powered git commit")
    parser.add_argument("--push", action="store_true", help="Push after committing")
    parser.add_argument("--dry-run", action="store_true", help="Show message without committing")
    args = parser.parse_args()

    if run_git_command(["git", "rev-parse", "--git-dir"]) is None:
        print("Error: Not in a git repository", file=sys.stderr)
        sys.exit(1)

    staged_files = run_git_command(["git", "diff", "--cached", "--name-only"])
    if not staged_files:
        print("No staged changes found. Use 'git add' to stage changes first")
        sys.exit(1)

    print(f"📝 Staged files: {staged_files.replace(chr(10), ', ')}")

    try:
        config = load_config()
        generator = CommitGenerator(config)

        diff_content = generator.get_staged_diff()
        context = generator.get_repo_context()
        commit_message = generator.generate_commit_message(diff_content, context)

        print(f"🤖 Generated message: {commit_message}")

        if args.dry_run:
            print("Dry run completed. No commit made")
            return

        response = str(input("Commit with this message? [Y/n]: ").strip().lower())
        if response and response not in ["y", "yes"]:
            print("Commit cancelled")
            return

        commit_result = run_git_command(["git", "commit", "-m", commit_message])
        if commit_result is not None:
            print("✅ Commit successful!")

            if args.push:
                print("📤 Pushing to remote...")
                push_result = run_git_command(["git", "push", "origin", "main"])
                if push_result is not None:
                    print("✅ Push successful!")
                else:
                    print("❌ Push failed")
        else:
            print("❌ Commit failed")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
