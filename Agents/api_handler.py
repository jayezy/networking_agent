#!/usr/bin/env python3
"""
API Handler for the networking agent system
Provides a simple interface for the backend to interact with Python agents
"""

import json
import sys
import os
from typing import Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import NetworkingAgent

def handle_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle API requests from the backend
    """
    try:
        action = request_data.get('action')
        agent = NetworkingAgent()
        
        if action == 'process_user':
            form_data = request_data.get('data', {})
            return agent.process_new_user(form_data)
            
        elif action == 'generate_matches':
            return agent.generate_matches_for_all_users()
            
        elif action == 'get_user_matches':
            user_id = request_data.get('user_id')
            if not user_id:
                return {"error": "No user_id provided"}
            return agent.get_matches_for_user(user_id)
            
        elif action == 'get_all_matches':
            return agent.get_all_matches()
            
        elif action == 'get_sample_data':
            return agent.get_sample_data()
            
        else:
            return {"error": f"Unknown action: {action}"}
            
    except Exception as e:
        return {"error": str(e)}

def main():
    """
    Main function to handle command line requests
    """
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        
        if not input_data:
            print(json.dumps({"error": "No input data provided"}))
            return
        
        # Parse the request
        request_data = json.loads(input_data)
        
        # Handle the request
        result = handle_request(request_data)
        
        # Output the result as JSON
        print(json.dumps(result))
        
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main() 