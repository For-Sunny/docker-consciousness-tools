#!/usr/bin/env python3
"""
Enhanced MCP Deployment Server with Claude Sonnet 4 Integration
Adds direct Claude API access to your deployment pipeline
"""

import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional
import aiohttp
import subprocess

# MCP protocol imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Add tools path
sys.path.append(r"C:\Users\Pirate\Desktop\Advanced_MCP_System")
from tools.deployment_tools import DeploymentToolsManager

class ClaudeIntegratedDeploymentServer:
    def __init__(self):
        self.deployment_manager = DeploymentToolsManager()
        self.server = Server("claude-deployment-tools")
        self.claude_api_url = "https://api.anthropic.com/v1/messages"
        self.setup_tools()
    
    def setup_tools(self):
        """Setup all MCP tools including Claude integration"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List all available deployment tools + Claude integration"""
            tools = []
            
            # Original deployment tools
            available_tools = self.deployment_manager.get_available_tools()
            for tool_name, tool_info in available_tools.items():
                tools.append(Tool(
                    name=tool_name,
                    description=tool_info["description"],
                    inputSchema={
                        "type": "object",
                        "properties": tool_info.get("parameters", {}),
                    }
                ))
            
            # Claude integration tools
            claude_tools = [
                Tool(
                    name="claude_code_review",
                    description="Use Claude Sonnet 4 to review code and suggest improvements",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "description": "Code to review"},
                            "language": {"type": "string", "description": "Programming language"},
                            "context": {"type": "string", "description": "Additional context"}
                        },
                        "required": ["code"]
                    }
                ),
                Tool(
                    name="claude_deployment_planning",
                    description="Use Claude Sonnet 4 to create deployment strategies",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_type": {"type": "string", "description": "Type of project to deploy"},
                            "requirements": {"type": "string", "description": "Deployment requirements"},
                            "constraints": {"type": "string", "description": "Any constraints or limitations"}
                        },
                        "required": ["project_type"]
                    }
                ),
                Tool(
                    name="claude_error_diagnosis",
                    description="Use Claude Sonnet 4 to diagnose deployment errors",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "error_log": {"type": "string", "description": "Error log or message"},
                            "system_info": {"type": "string", "description": "System information"},
                            "deployment_context": {"type": "string", "description": "Deployment context"}
                        },
                        "required": ["error_log"]
                    }
                ),
                Tool(
                    name="claude_optimize_config",
                    description="Use Claude Sonnet 4 to optimize configuration files",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "config_content": {"type": "string", "description": "Configuration file content"},
                            "config_type": {"type": "string", "description": "Type of config (docker, yaml, json, etc.)"},
                            "optimization_goals": {"type": "string", "description": "What to optimize for"}
                        },
                        "required": ["config_content", "config_type"]
                    }
                )
            ]
            
            tools.extend(claude_tools)
            return tools

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute deployment tools with Claude integration"""
            
            try:
                # Claude integration tools
                if name.startswith("claude_"):
                    return await self.handle_claude_tool(name, arguments)
                
                # Original deployment tools
                elif hasattr(self.deployment_manager, name):
                    tool_method = getattr(self.deployment_manager, name)
                    result = tool_method(**arguments)
                    result_text = json.dumps(result, indent=2)
                    
                    return [TextContent(
                        type="text",
                        text=result_text
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Tool '{name}' not found"
                    )]
                    
            except Exception as e:
                return [TextContent(
                    type="text", 
                    text=f"Error executing {name}: {str(e)}"
                )]

    async def handle_claude_tool(self, tool_name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle Claude Sonnet 4 API calls"""
        
        # Get API key from environment or prompt
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return [TextContent(
                type="text",
                text="ANTHROPIC_API_KEY not set. Please set your API key."
            )]
        
        # Prepare prompts based on tool
        prompt = self.prepare_claude_prompt(tool_name, arguments)
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01"
                }
                
                payload = {
                    "model": "claude-3-5-sonnet-20241022",  # Latest Sonnet model
                    "max_tokens": 4000,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
                
                async with session.post(self.claude_api_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        claude_response = result['content'][0]['text']
                        
                        return [TextContent(
                            type="text",
                            text=f"Claude Sonnet 4 Response:\n\n{claude_response}"
                        )]
                    else:
                        error_text = await response.text()
                        return [TextContent(
                            type="text",
                            text=f"Claude API Error ({response.status}): {error_text}"
                        )]
                        
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error calling Claude API: {str(e)}"
            )]

    def prepare_claude_prompt(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Prepare specialized prompts for different Claude tools"""
        
        if tool_name == "claude_code_review":
            return f"""Please review this {arguments.get('language', 'code')} code and provide detailed feedback:

Code:
```{arguments.get('language', '')}
{arguments['code']}
```

Context: {arguments.get('context', 'No additional context provided')}

Please provide:
1. Code quality assessment
2. Potential bugs or issues
3. Performance improvements
4. Best practices recommendations
5. Security considerations (if applicable)
"""

        elif tool_name == "claude_deployment_planning":
            return f"""Create a comprehensive deployment strategy for this project:

Project Type: {arguments['project_type']}
Requirements: {arguments.get('requirements', 'Standard deployment')}
Constraints: {arguments.get('constraints', 'None specified')}

Please provide:
1. Deployment architecture recommendation
2. Step-by-step deployment plan
3. Required infrastructure
4. Security considerations
5. Monitoring and maintenance strategy
6. Rollback procedures
"""

        elif tool_name == "claude_error_diagnosis":
            return f"""Diagnose this deployment error and provide solutions:

Error Log:
{arguments['error_log']}

System Info: {arguments.get('system_info', 'Not provided')}
Deployment Context: {arguments.get('deployment_context', 'Not provided')}

Please provide:
1. Root cause analysis
2. Immediate fix recommendations
3. Prevention strategies
4. Related issues to check
5. Step-by-step troubleshooting guide
"""

        elif tool_name == "claude_optimize_config":
            return f"""Optimize this {arguments['config_type']} configuration:

Configuration:
```{arguments['config_type']}
{arguments['config_content']}
```

Optimization Goals: {arguments.get('optimization_goals', 'General optimization')}

Please provide:
1. Optimized configuration
2. Explanation of changes
3. Performance impact
4. Security improvements
5. Best practices applied
"""

        return f"Process this request: {json.dumps(arguments, indent=2)}"

    async def run(self):
        """Run the enhanced MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

async def main():
    """Main entry point"""
    server = ClaudeIntegratedDeploymentServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
