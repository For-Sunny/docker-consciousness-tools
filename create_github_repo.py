#!/usr/bin/env python3
import subprocess
import os

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

# Navigate to project directory
project_dir = r"C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS"
os.chdir(project_dir)

print("=== GitHub Repository Setup ===")
print(f"Working in: {project_dir}")
print()

# Check if we're in a git repo
stdout, stderr, code = run_command("git status")
if code != 0:
    print("Initializing Git repository...")
    run_command("git init")
    run_command("git add .")
    run_command('git commit -m "Initial commit with Claude Code integration"')
    print("[+] Git repository initialized and committed")

# Create GitHub repository
print("Creating GitHub repository...")
stdout, stderr, code = run_command("gh repo create docker-consciousness-tools --public --source=. --push")
if code == 0:
    print("[+] Repository created successfully")
    print(stdout)
else:
    print(f"Repository creation result: {stderr}")
    if "already exists" in stderr.lower():
        print("[+] Repository already exists, pushing changes...")
        run_command("git remote add origin https://github.com/For-Sunny/docker-consciousness-tools.git")
        run_command("git push -u origin main")

print()
print("=== Next: Set up API key ===")
print("Run: gh secret set ANTHROPIC_API_KEY")
print("Then paste your API key from: https://console.anthropic.com/settings/keys")
