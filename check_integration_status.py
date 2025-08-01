#!/usr/bin/env python3
import subprocess
import os

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

print("=== Checking Integration Status ===")
print()

# Check Git status
current_dir = r"C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS"
print(f"Working directory: {current_dir}")

stdout, stderr, code = run_command("git status", cwd=current_dir)
if code == 0:
    print("[+] Git repository status:")
    print(stdout)
else:
    print("[X] Git repository issue:")
    print(stderr)

print()

# Check GitHub repository
stdout, stderr, code = run_command("gh repo view", cwd=current_dir)
if code == 0:
    print("[+] GitHub repository found:")
    print(stdout[:200] + "...")
else:
    print("[X] GitHub repository issue:")
    print(stderr)

print()

# Check GitHub Actions
stdout, stderr, code = run_command("gh workflow list", cwd=current_dir)
if code == 0:
    print("[+] GitHub Actions workflows:")
    print(stdout)
else:
    print("[X] GitHub Actions issue:")
    print(stderr)

print()

# Check GitHub secrets
stdout, stderr, code = run_command("gh secret list", cwd=current_dir)
if code == 0:
    print("[+] GitHub secrets:")
    print(stdout)
else:
    print("[X] GitHub secrets issue:")
    print(stderr)

print()
print("=== Next Steps ===")
print("1. Set environment variable permanently:")
print('   setx ANTHROPIC_API_KEY "your-api-key"')
print("2. Test VS Code Copilot with Claude Sonnet 4")
print("3. Trigger GitHub Actions workflow")
