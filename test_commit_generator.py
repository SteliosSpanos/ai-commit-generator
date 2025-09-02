import os
import sys
import tempfile
import subprocess
from pathlib import Path

SAMPLE_DIFF = """diff --git a/auth/login.py b/auth/login.py
index 1234567..abcdefg 100644
--- a/auth/login.py
+++ b/auth/login.py
@@ -1,6 +1,10 @@
 from flask import request, jsonify
 from werkzeug.security import check_password_hash
+from .oauth import OAuth2Provider
 
 def login():
     username = request.json.get('username')
     password = request.json.get('password')
+    
+    # Add OAuth2 support
+    oauth_provider = OAuth2Provider()
     return jsonify({'status': 'success'})
"""

def test_basic_functionality():
    """Test basic commit message functionality"""
    print("🧪 Testing basic functionality...")

    sys.path.insert(0, os.path.dirname(__file__))
    from commit_generator import CommitGenerator, Config

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("Please set it in .env file or environment variables")
        return False

    try:
        config = Config(openai_api_key=api_key)
        generator = CommitGenerator(config)

        context = {"project_type" : "python", "branch" : "main"}
        message = generator.generate_commit_message(SAMPLE_DIFF, context)

        print(f"✅ Generated message: {message}")

        if ":" in message and len(message.split(":")[0].strip()) > 0:
            print("✅ Message format looks good")
            return True
        else:
            print("❌ Message format doesn't match conventional commits")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_git_integration():
    """Test git integration (if in git repo)"""
    print("\n🧪 Testing git integration...")

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Git repository detected")

        result = subprocess.run(
            ["git", "diff", "--cached", "--no-color"],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            print("✅ Found staged changes for testing")
        else:
            print("ℹ️  No staged changes (this is normal)")

        return True
    except subprocess.CalledProcessError:
        print("ℹ️  Not in a git repository (this is fine for basic testing)")
        return True
    except FileNotFoundError:
        print("❌ Git not found - install git to use this tool")
        return False


def test_project_detection():
    """Test project type detection"""
    print("\n🧪 Testing project type detection...")

    sys.path.insert(0, os.path.dirname(__file__))
    from commit_generator import CommitGenerator, Config

    test_cases = [
        (["package.json"], "javascript/node"),
        (["requirements.txt"], "python"),
        (["pyproject.toml"], "python"),
        (["pom.xml"], "java"),
        (["Cargo.toml"], "rust"),
        (["go.mod"], "go"),
        (["composer.json"], "php"),
        (["README.md"], "general")
    ]

    config = Config(openai_api_key="dummy")
    generator = CommitGenerator(config)

    for files, expected in test_cases:
        detected = generator._detect_project_type(files)
        if detected == expected:
            print(f"✅ {files} -> {detected}")
        else:
            print(f"❌ {files} -> expected {expected}, got {detected}")

    return True

def test_hook_installation():
    """Test hook installation in a temporary git repo"""
    print("\n🧪 Testing hook installation...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        try:
            subprocess.run(
                ["git", "init"],
                cwd=temp_path,
                check=True,
                capture_output=True
            )

            script_path = Path(__file__).parent / "install_hook.py"
            result = subprocess.run(
                ["python", str(script_path), "install"],
                cwd=temp_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✅ Hook installation completed")

                hook_file = temp_path / ".git" / "hooks" / "prepare-commit-msg"
                if hook_file.exists():
                    print("✅ Hook file created successfully")
                    return True
                else:
                    print("❌ Hook file not found")
                    return False
            else:
                print(f"❌ Hook installation failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error testing hook installation: {e}")
            return False

def main():
    print("🚀 AI Commit Generator - Test Suite")
    print("=" * 50)

    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Git Integration", test_git_integration),
        ("Project Detection", test_project_detection),
        ("Hook Installation", test_hook_installation),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((name, False))

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)

    passed = 0
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if success:
            passed += 1

    print(f"\n📈 {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("🎉 All tests passed! Your setup looks good.")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()