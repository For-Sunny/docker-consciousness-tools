#!/usr/bin/env python3
"""
Claude Sonnet 4 MCP Integration Setup
Configures your MCP servers to use Claude Sonnet 4 directly
"""

import json
import os
import subprocess
import sys

def create_claude_mcp_config():
    """Create MCP configuration for Claude integration"""
    
    # Path to Claude MCP config
    claude_config_dir = os.path.expanduser("~/.config/claude-desktop")
    if not os.path.exists(claude_config_dir):
        os.makedirs(claude_config_dir)
    
    config_path = os.path.join(claude_config_dir, "claude_desktop_config.json")
    
    # Enhanced MCP configuration
    config = {
        "mcpServers": {
            "system-tools": {
                "command": "node",
                "args": [r"C:\Users\Pirate\Desktop\Claude\MCP_Servers\system_server.js"],
                "env": {
                    "NODE_PATH": r"C:\Users\Pirate\Desktop\Claude\MCP_Servers\node_modules"
                }
            },
            "deployment-tools": {
                "command": "python",
                "args": [r"C:\Users\Pirate\Desktop\Advanced_MCP_System\mcp_deployment_server.py"],
                "env": {
                    "PYTHONPATH": r"C:\Users\Pirate\Desktop\Advanced_MCP_System"
                }
            },
            "claude-integrated-deployment": {
                "command": "python",
                "args": [r"C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS\claude_integrated_deployment.py"],
                "env": {
                    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
                    "PYTHONPATH": r"C:\Users\Pirate\Desktop\Advanced_MCP_System"
                }
            },
            "filesystem": {
                "command": "node",
                "args": [r"C:\Users\Pirate\AppData\Roaming\Claude\Claude Extensions\ant.dir.ant.anthropic.filesystem\server\index.js"],
                "args_extended": ["C:\\", "E:\\", r"C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS"]
            }
        },
        "claude_preferences": {
            "default_model": "claude-sonnet-4-20250514",
            "github_integration": {
                "enabled": True,
                "username": "For-Sunny",
                "repositories": ["docker-consciousness-tools"]
            },
            "deployment_automation": {
                "enabled": True,
                "auto_review": True,
                "model_preference": "claude-sonnet-4"
            }
        }
    }
    
    # Write configuration
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"[+] Created Claude MCP config: {config_path}")
    return config_path

def setup_vscode_copilot_config():
    """Configure VS Code for Claude Sonnet 4"""
    
    vscode_settings_dir = os.path.expanduser("~/.vscode")
    if not os.path.exists(vscode_settings_dir):
        vscode_settings_dir = os.path.expanduser("~/AppData/Roaming/Code/User")
    
    if os.path.exists(vscode_settings_dir):
        settings_path = os.path.join(vscode_settings_dir, "settings.json")
        
        # VS Code settings for Claude Sonnet 4
        vscode_settings = {
            "github.copilot.enable": {
                "*": True,
                "yaml": True,
                "plaintext": True,
                "markdown": True,
                "python": True,
                "javascript": True,
                "typescript": True
            },
            "github.copilot.advanced": {
                "model": "claude-sonnet-4",
                "listCount": 10,
                "inlineSuggestCount": 3
            },
            "github.copilot.chat.model": "claude-sonnet-4",
            "workbench.editor.enablePreview": False,
            "editor.inlineSuggest.enabled": True,
            "editor.suggestSelection": "first"
        }
        
        # Merge with existing settings if they exist
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    existing_settings = json.load(f)
                existing_settings.update(vscode_settings)
                vscode_settings = existing_settings
            except:
                pass
        
        with open(settings_path, 'w') as f:
            json.dump(vscode_settings, f, indent=2)
        
        print(f"[+] Updated VS Code settings: {settings_path}")

def create_deployment_workflow():
    """Create enhanced GitHub Actions workflow with Claude integration"""
    
    workflow_content = """name: Claude Sonnet 4 Deployment Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  issues:
    types: [opened, edited]
  workflow_dispatch:
    inputs:
      deployment_task:
        description: 'Deployment task for Claude'
        required: true
        type: string
      model_preference:
        description: 'Claude model to use'
        required: false
        default: 'claude-sonnet-4-20250514'
        type: choice
        options:
          - claude-sonnet-4-20250514
          - claude-3-5-sonnet-20241022

jobs:
  claude-deployment:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        pip install anthropic aiohttp mcp
        npm install -g @anthropic-ai/claude-cli
    
    - name: Configure Claude
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        echo "Configuring Claude Sonnet 4..."
        export CLAUDE_MODEL="claude-sonnet-4-20250514"
    
    - name: Code Review with Claude
      if: github.event_name == 'pull_request'
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        python .github/scripts/claude_code_review.py \\
          --pr-number=${{ github.event.pull_request.number }} \\
          --model=claude-sonnet-4-20250514
    
    - name: Issue Analysis with Claude
      if: github.event_name == 'issues'
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        python .github/scripts/claude_issue_analysis.py \\
          --issue-number=${{ github.event.issue.number }} \\
          --model=claude-sonnet-4-20250514
    
    - name: Deployment Planning
      if: github.event_name == 'workflow_dispatch'
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        python claude_integrated_deployment.py \\
          --task="${{ github.event.inputs.deployment_task }}" \\
          --model="${{ github.event.inputs.model_preference }}"
    
    - name: Deploy to Production
      if: github.ref == 'refs/heads/main'
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        echo "Deploying with Claude Sonnet 4 oversight..."
        python claude_integrated_deployment.py --deploy
"""
    
    workflow_path = r"C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS\.github\workflows\claude-sonnet-4-deployment.yml"
    
    with open(workflow_path, 'w') as f:
        f.write(workflow_content)
    
    print(f"[+] Created enhanced deployment workflow: {workflow_path}")

def main():
    print("=== Claude Sonnet 4 MCP Integration Setup ===")
    print()
    
    # Create MCP configuration
    config_path = create_claude_mcp_config()
    
    # Setup VS Code configuration
    setup_vscode_copilot_config()
    
    # Create enhanced deployment workflow
    create_deployment_workflow()
    
    print()
    print("=== Setup Complete ===")
    print()
    print("✅ Claude Sonnet 4 integrated into MCP servers")
    print("✅ VS Code configured for Claude Sonnet 4")
    print("✅ Enhanced GitHub Actions workflow created")
    print()
    print("Next steps:")
    print("1. Set ANTHROPIC_API_KEY environment variable")
    print("2. Restart Claude desktop app")
    print("3. Restart VS Code")
    print("4. Test the integration with: python claude_integrated_deployment.py")
    print()
    print("Your MCP servers now have direct Claude Sonnet 4 access for:")
    print("- Intelligent code review")
    print("- Deployment strategy planning") 
    print("- Error diagnosis and resolution")
    print("- Configuration optimization")

if __name__ == "__main__":
    main()
