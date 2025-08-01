#!/usr/bin/env python3
"""
Claude Sonnet 4 Code Review Script for GitHub Actions
"""

import asyncio
import aiohttp
import os
import sys
import json
import argparse
from typing import Dict, List

class ClaudeCodeReviewer:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.anthropic.com/v1/messages"
    
    async def review_pr_files(self, pr_files: List[Dict]) -> str:
        """Review PR files using Claude Sonnet 4"""
        
        # Prepare code review prompt
        files_content = []
        for file in pr_files:
            if file.get('patch'):
                files_content.append(f"""
File: {file['filename']}
Status: {file['status']}
Changes: +{file['additions']} -{file['deletions']}

Diff:
{file['patch']}
""")
        
        prompt = f"""Please review this pull request and provide detailed feedback:

{chr(10).join(files_content)}

Please provide:
1. **Code Quality Assessment**: Overall code quality and adherence to best practices
2. **Security Review**: Potential security vulnerabilities or concerns  
3. **Performance Analysis**: Performance implications of the changes
4. **Bug Detection**: Potential bugs or logical errors
5. **Improvement Suggestions**: Specific recommendations for improvement
6. **Approval Recommendation**: Whether this PR should be approved, needs changes, or rejected

Format your response in GitHub-flavored markdown with clear sections.
"""

        async with aiohttp.ClientSession() as session:
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": self.model,
                "max_tokens": 4000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            async with session.post(self.api_url, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['content'][0]['text']
                else:
                    error_text = await response.text()
                    raise Exception(f"Claude API Error ({response.status}): {error_text}")

    async def post_review_comment(self, review_text: str, pr_number: int):
        """Post review comment to GitHub PR"""
        # This would use GitHub API to post the comment
        # For now, just print the review
        print(f"=== Claude Sonnet 4 Code Review for PR #{pr_number} ===")
        print(review_text)
        print("=" * 60)

async def main():
    parser = argparse.argumentParser(description="Claude Sonnet 4 Code Review")
    parser.add_argument("--pr-number", required=True, help="Pull request number")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Claude model to use")
    
    args = parser.parse_args()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    # Mock PR files data (in real implementation, fetch from GitHub API)
    mock_pr_files = [
        {
            "filename": "example.py",
            "status": "modified",
            "additions": 10,
            "deletions": 2,
            "patch": """@@ -1,5 +1,13 @@
def process_data(data):
-    return data.upper()
+    if not data:
+        return ""
+    return data.strip().upper()

+def validate_input(data):
+    if not isinstance(data, str):
+        raise ValueError("Input must be a string")
+    return True
+
 # Main execution
 if __name__ == "__main__":
     result = process_data("hello world")"""
        }
    ]
    
    reviewer = ClaudeCodeReviewer(api_key, args.model)
    review = await reviewer.review_pr_files(mock_pr_files)
    await reviewer.post_review_comment(review, int(args.pr_number))

if __name__ == "__main__":
    asyncio.run(main())
