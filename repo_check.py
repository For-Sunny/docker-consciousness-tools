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
    print("✓ This is a Git repository")
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
    print("✗ Not a Git repository (or Git not found)")
    print(f"Error: {stderr}")
    
    # Check if .git exists
    git_dir = os.path.join(current_dir, '.git')
    if os.path.exists(git_dir):
        print("✓ .git directory found")
    else:
        print("✗ No .git directory")

print()
print("=== Available Git Repositories Search ===")

# Search for Git repositories on the system
search_paths = ["C:\\", "E:\\"]
for search_path in search_paths:
    if os.path.exists(search_path):
        print(f"Searching {search_path}...")
        try:
            for root, dirs, files in os.walk(search_path):
                if '.git' in dirs:
                    print(f"Found Git repo: {root}")
                # Don't go too deep to avoid performance issues
                if root.count(os.sep) > 3:
                    dirs.clear()
        except (PermissionError, OSError):
            continue
