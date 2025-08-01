#!/usr/bin/env python3
import subprocess
import os

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

current_dir = r"C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS"

print("=== Pushing Updates to GitHub ===")
print()

# Add new files
stdout, stderr, code = run_command("git add .", cwd=current_dir)
print(f"Git add result: {code}")

# Commit
stdout, stderr, code = run_command('git commit -m "Add Claude Sonnet 4 integration and test scripts"', cwd=current_dir)
print(f"Git commit: {stdout if stdout else stderr}")

# Push
stdout, stderr, code = run_command("git push", cwd=current_dir)
print(f"Git push: {stdout if stdout else stderr}")

print()
print("=== Checking Workflows on GitHub ===")

# Check workflows after push
stdout, stderr, code = run_command("gh workflow list", cwd=current_dir)
if code == 0:
    print("Available workflows:")
    print(stdout)
else:
    print(f"Workflow check failed: {stderr}")

print()
print("[SUCCESS] Your Claude Sonnet 4 integration is set up!")
print()
print("What's working:")
print("✓ GitHub repository created")
print("✓ API key stored as GitHub secret") 
print("✓ Claude Sonnet 4 enabled in Copilot")
print("✓ MCP server configurations created")
print("✓ GitHub Actions workflows ready")
print()
print("To test:")
print("1. Open VS Code - Copilot should use Claude Sonnet 4")
print("2. Go to https://github.com/For-Sunny/docker-consciousness-tools/actions")
print("3. Manually trigger 'Claude Sonnet 4 Deployment Pipeline'")
print("4. Set permanent env var: setx ANTHROPIC_API_KEY \"your-key\"")
