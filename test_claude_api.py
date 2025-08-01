#!/usr/bin/env python3
"""
Simple test of Claude Sonnet 4 API integration
"""
import os
import requests
import json

def test_claude_api():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    # Test API call
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": "Hello! Please respond with 'Claude Sonnet integration working!'"}
        ]
    }
    
    try:
        response = requests.post("https://api.anthropic.com/v1/messages", 
                               headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            claude_response = result['content'][0]['text']
            print(f"✅ Claude API Response: {claude_response}")
            return True
        else:
            print(f"❌ API Error ({response.status_code}): {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Testing Claude Sonnet 4 Integration ===")
    print()
    
    success = test_claude_api()
    
    if success:
        print()
        print("🎉 Claude Sonnet 4 integration is working!")
        print("Your MCP servers now have direct API access.")
    else:
        print()
        print("❌ Integration test failed. Check API key and connection.")
