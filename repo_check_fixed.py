#!/usr/bin/env python3
import subprocess
import os

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

# Check current directory
current_dir = r"C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS"
print(f"Checking directory: {current_dir}")
print()

# Check if this is a Git repository
stdout, stderr, code = run_command("git status", cwd=current_dir)
if code == 0:
    print("[+] This is a Git repository")
    print("Git Status:")
    print(stdout)
    print()
    
    # Get remote info
    stdout, stderr, code = run_command("git remote -v", cwd=current_dir)
    if code == 0 and stdout:
        print("Remote repositories:")
        print(stdout)
    else:
        print("No remote repositories configured")
    print()
    
    # Get branch info
    stdout, stderr, code = run_command("git branch -a", cwd=current_dir)
    if code == 0:
        print("Branches:")
        print(stdout)
else:
    print("[-] Not a Git repository (or Git not found)")
    print(f"Error: {stderr}")
    
    # Check if .git exists
    git_dir = os.path.join(current_dir, '.git')
    if os.path.exists(git_dir):
        print("[+] .git directory found")
    else:
        print("[-] No .git directory")

print()
print("=== GitHub CLI Setup Check ===")
stdout, stderr, code = run_command("where gh")
if code == 0:
    print(f"GitHub CLI found at: {stdout}")
else:
    print("GitHub CLI not found - need to install it")
    print("Download from: https://cli.github.com/")

print()
print("=== Copilot CLI Check ===")
stdout, stderr, code = run_command("where github-copilot-cli")
if code != 0:
    stdout, stderr, code = run_command("npm list -g github-copilot-cli")
    
if code == 0:
    print("Copilot CLI found")
else:
    print("Copilot CLI not found")
