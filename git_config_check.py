#!/usr/bin/env python3
import subprocess
import os

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

print("=== Git Configuration Check ===")
print()

# Check Git version
stdout, stderr, code = run_command("git --version")
if code == 0:
    print(f"Git Version: {stdout}")
else:
    print(f"Git not found: {stderr}")

print()

# Check Git global config
print("=== Global Git Configuration ===")
stdout, stderr, code = run_command("git config --global --list")
if code == 0:
    for line in stdout.split('\n'):
        if line.strip():
            print(line)
else:
    print(f"Error getting config: {stderr}")

print()

# Check GitHub CLI
print("=== GitHub CLI Check ===")
stdout, stderr, code = run_command("gh --version")
if code == 0:
    print(f"GitHub CLI: {stdout.split()[0]} {stdout.split()[2]}")
    
    # Check auth status
    stdout, stderr, code = run_command("gh auth status")
    if code == 0:
        print("GitHub Auth Status:")
        print(stdout)
    else:
        print("Not authenticated with GitHub CLI")
else:
    print("GitHub CLI not installed")

print()

# Check for repositories in common locations
print("=== Repository Scan ===")
common_paths = [
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Projects"), 
    os.path.expanduser("~/Code"),
    "C:\\Users\\{}\\Documents".format(os.getenv('USERNAME', 'user')),
    "C:\\Projects",
    "C:\\Code",
    "E:\\Projects",
    "E:\\Code"
]

for path in common_paths:
    if os.path.exists(path):
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, '.git')):
                    print(f"Git repo found: {item_path}")
        except PermissionError:
            continue

print()
print("=== Environment Variables ===")
relevant_vars = ['GITHUB_TOKEN', 'ANTHROPIC_API_KEY', 'PATH']
for var in relevant_vars:
    value = os.getenv(var)
    if value:
        if var in ['GITHUB_TOKEN', 'ANTHROPIC_API_KEY']:
            print(f"{var}: {'*' * min(8, len(value))}... (hidden)")
        else:
            print(f"{var}: {value[:100]}{'...' if len(value) > 100 else ''}")
    else:
        print(f"{var}: Not set")
