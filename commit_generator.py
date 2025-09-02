import subprocess
import sys
import os
import json
from typing import Optional
import argparse
from dataclasses import dataclass
import openai
from dotenv import load_dotenv

@dataclass
class Config:
    """Configuration for the commit generator"""
    openai_api_key: str
    model: str="gpt-4"
    max_diff_length: int=8000
    temperature: float=0.3

class CommitGenerator:
    def __init__(self, config: Config):
        self.config = config
        openai.api_key = config.openai_api_key

    def get_staged_diff(self) -> str:
        """Get the staged changes from git"""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--no-color"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff: {e}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Git not found. Make sure git is installed in your PATH", file=sys.stderr)
            sys.exit(1)

    def get_repo_context(self) -> dict:
        """Get additional repository context"""
        context = {}
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True
            )
            context["branch"] = result.stdout.strip()
        except:
            context["branch"] = "unknown"

        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            repo_root = result.stdout.strip()
            project_files = os.listdir(repo_root)
            context["project_type"] = self._detect_project_type(project_files)
        except:
            context["project_type"] = "unknown"

        return context

    def _detect_project_type(self, files: list) -> str:
        """Detect project type from files in repo root"""
        if "package.json" in files:
            return "javascript/node"
        elif "requirements.txt" in files or "pyproject.toml" in files:
            return "python"
        elif "pom.xml" in files:
            return "java"
        elif "Cargo.toml" in files:
            return "rust"
        elif "go.mod" in files:
            return "go"
        elif "composer.json" in files:
            return "php"
        else:
            return "general"

    def generate_commit_message(self, diff_content: str, context: dict) -> str:
        """Generate commit message using OpenAI API"""
        if not diff_content.strip():
            print("No staged changed found.", file=sys.stderr)
            sys.exit(1)

        if len(diff_content) > self.config.max_diff_length:
            diff_content = diff_content[:self.config.max_diff_length] + "\n... (diff truncated due to length)"

        prompt = self._build_prompt(diff_content, context)

        try:
            response = openai.chat.completions.create(
                model=self.config.model,
                messages=[{"role" : "user", "content" : prompt}],
                max_tokens=100,
                temperature=self.config.temperature
            )

            commit_message = response.choices[0].message.content.strip()
            commit_message = commit_message.strip('"\'')

            return commit_message
        except openai.APIError as e:
            print(f"OpenAI API error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

    def _build_prompt(self, diff_content: str, context: dict) -> str:
        """Build the prompt for the LLM"""
        project_context = ""
        if context.get("project_type") != "unknown":
            project_context = f"This is a {context["project_type"]} project. "

        return f"""
            You are an expert developer who writes perfect git commit messages following the Conventional Commits specification.
            {project_context}Analyze the following git diff and generate a single commit message that:
            
            1. Uses the format: <type>(<scope>): <description>
            2. Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build
            3. Scope is optional but helpful (e.g., auth, ui, api, deps)
            4. Keep description under 50 characters
            5. Be specific and descriptive
            6. Use imperative mood (e.g., "add" not "added")
            7. Don't include "fix typo" for obvious typos, be more specific

            Examples of good commit messages:
            - feat(auth): add OAuth login flow
            - fix(api): handle null user response
            - docs: update installation guide
            - refactor(utils): extract validation logic
            - test(auth): add login component tests

            Git diff:
            '''
            {diff_content}
            '''

            Respond with ONLY the commit message, nothing else. No explanations, no quotes, just the commit message.
        """

def load_config() -> Config:
    """Load configuration from environment variables and config file"""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        print("Please set it in your environment or create a .env file.", file=sys.stderr)
        sys.exit(1)

    return Config(
        openai_api_key=api_key,
        model=os.getenv("AI_COMMIT_MODEL", "gpt-4"),
        max_diff_length=int(os.getenv("AI_COMMIT_MAX_DIFF_LENGTH", "8000")),
        temperature=float(os.getenv("AI_COMMIT_TEMPERATURE", "0.3"))
    )

def main():
    parser = argparse.ArgumentParser(description="Generate AI-powered git commit messages")
    parser.add_argument("--dry-run", action="store_true", help="Print message without committing")
    parser.add_argument("--message-file", help="Write message to file (for git hooks)")
    parser.add_argument("--diff", help="Use provided diff instead of staged changes")
    args = parser.parse_args()

    config = load_config()
    generator = CommitGenerator(config)

    if args.diff:
        diff_content = args.diff
    else:
        diff_content = generator.get_staged_diff()

    context = generator.get_repo_context()
    commit_message = generator.generate_commit_message(diff_content, context)

    if args.dry_run:
        print(f"Generated commit message: {commit_message}")
    elif args.message_file:
        with open(args.message_file, "w") as f:
            f.write(commit_message)
        print(f"Commit message written to {args.message_file}")
    else:
        print(commit_message)

if __name__ == "__main__":
    main()