#!/usr/bin/env python3
"""
Networking Matchmaking System
Main entry point with JSON-based API interface
"""

import sys
import json
from typing import Dict, Any, List
from api_handler import NetworkingAPIHandler
from orchestrator import NetworkingOrchestratorSync
import os

class NetworkingMatchmakingSystem:
    """
    Main system that provides JSON-based API for networking matchmaking
    """
    
    def __init__(self):
        self.api_handler = NetworkingAPIHandler()
        self.orchestrator = NetworkingOrchestratorSync()
    
    def process_json_request(self, json_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process any JSON request and return JSON response
        """
        return self.api_handler.process_request(json_request)
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a new user
        """
        request = {
            "action": "register_user", 
            **user_data
        }
        return self.process_json_request(request)
    
    def get_matches(self, user_data: Dict[str, Any], attendees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get matches for a user
        """
        request = {
            "action": "get_matches",
            "user": user_data,
            "attendees": attendees
        }
        return self.process_json_request(request)
    
    def process_event(self, attendees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process all event attendees
        """
        request = {
            "action": "process_event",
            "attendees": attendees
        }
        return self.process_json_request(request)
    
    def get_dashboard(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get user dashboard data
        """
        request = {
            "action": "get_dashboard",
            "user": user_data
        }
        return self.process_json_request(request)
    
    def run_demo(self):
        """
        Run a demo with sample JSON data
        """
        print("=== Networking Matchmaking System Demo ===\n")
        
        # Sample user data
        sample_user = {
            "user_id": "user_id_123456789",
            "name": "Jay Agrawal",
            "about": "Senior software engineer with 5+ years experience in Python, cloud technologies, and machine learning. Passionate about mentoring junior developers and contributing to open-source projects.",
            "give": "Technical mentorship, code review expertise, cloud architecture guidance, and open-source project collaboration",
            "take": "AI/ML project opportunities, startup connections, speaking opportunities at tech conferences, and collaboration on innovative projects",
            "linkedin_url": "https://www.linkedin.com/in/agrawalrinkal/"
        }

        # sample_data_path = os.path.join(os.path.dirname(__file__), '../Database/' + 'sample_data5' + '.json')
        # with open(sample_data_path, 'r') as f:
        #     data = json.load(f)
        # sample_user = data[0]
        
        # Sample attendees
        sample_attendees = [
            {
                "name": "Jane Smith",
                "linkedin_url": "https://www.linkedin.com/in/janesmith",
                "about": "AI Product Manager at TechCorp with expertise in machine learning product development. Love building products that scale and mentoring aspiring PMs.",
                "give": "Product strategy, AI project scoping, mentorship for aspiring PMs, and connections in the AI/ML space",
                "take": "Technical cofounders, cloud scaling expertise, and collaboration on AI projects"
            },
            {
                "name": "Mike Johnson",
                "linkedin_url": "https://www.linkedin.com/in/mikejohnson",
                "about": "DevOps engineer and cloud architect with 6+ years experience. Conference speaker and community leader in the DevOps space.",
                "give": "DevOps automation, cloud infrastructure guidance, SRE best practices, and conference speaking opportunities",
                "take": "AI integration expertise, mentorship opportunities, and collaboration on cloud-native projects"
            }
        ]
        
        # Demo 1: User Registration
        print("1. User Registration")
        print("Input JSON:")
        print(json.dumps(sample_user, indent=2))
        
        registration_result = self.register_user(sample_user)
        self.orchestrator.merge_registration_with_sample_data(registration_result, 'sample_data4')
        print("\nOutput JSON:")
        print(json.dumps(registration_result, indent=2))
        
        # Demo 2: Get Matches
        print("\n" + "="*50)
        print("2. Get User Matches")
        print("Input JSON:")
        matches_input = {
            "user": sample_user,
            "attendees": sample_attendees
        }
        print(json.dumps(matches_input, indent=2))
        
        matches_result = self.get_matches(sample_user, sample_attendees)
        print("\nOutput JSON:")
        print(json.dumps(matches_result, indent=2))
        
        # Demo 3: Process Event
        print("\n" + "="*50)
        print("3. Process Event Attendees")
        print("Input JSON:")
        event_input = {
            "attendees": sample_attendees + [sample_user]
        }
        print(json.dumps(event_input, indent=2))
        
        event_result = self.process_event(sample_attendees + [sample_user])
        print("\nOutput JSON:")
        print(json.dumps(event_result, indent=2))
        
        print("\n=== Demo Completed ===")
    
    def process_from_file(self, input_file: str, output_file: str = None):
        """
        Process JSON request from file
        """
        try:
            # Read input JSON
            with open(input_file, 'r') as f:
                json_request = json.load(f)
            
            # Process request
            result = self.process_json_request(json_request)
            
            # Write output
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"✅ Result written to {output_file}")
            else:
                print(json.dumps(result, indent=2))
                
        except FileNotFoundError:
            print(f"❌ Input file not found: {input_file}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in input file: {input_file}")
        except Exception as e:
            print(f"❌ Error processing file: {str(e)}")

def main():
    """
    Main entry point
    """
    system = NetworkingMatchmakingSystem()
    print("hi", sys.argv)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "demo":
            # Run demo
            system.run_demo()
        
        elif command == "file":
            # Process from file
            if len(sys.argv) < 3:
                print("Usage: python main.py file <input_file> [output_file]")
                return
            
            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            system.process_from_file(input_file, output_file)
        
        elif command == "register":
            # Example user registration
            sample_user = {
                "name": "John Doe",
                "linkedin_url": "https://www.linkedin.com/in/johndoe",
                "about": "Senior software engineer with expertise in Python and cloud technologies",
                "give": "Technical mentorship and cloud architecture guidance",
                "take": "AI/ML project opportunities and startup connections"
            }
            result = system.register_user(sample_user)
            system.orchestrator.merge_registration_with_sample_data(result)
            print(json.dumps(result, indent=2))
        
        elif command == "matches":
            # Example getting matches
            user = {
                "name": "John Doe",
                "linkedin_url": "https://www.linkedin.com/in/johndoe",
                "about": "Senior software engineer with expertise in Python and cloud technologies",
                "give": "Technical mentorship and cloud architecture guidance",
                "take": "AI/ML project opportunities and startup connections"
            }
            attendees = [
                {
                    "name": "Jane Smith",
                    "linkedin_url": "https://www.linkedin.com/in/janesmith",
                    "about": "AI Product Manager with expertise in machine learning",
                    "give": "Product strategy and AI project scoping",
                    "take": "Technical cofounders and cloud expertise"
                }
            ]
            result = system.get_matches(user, attendees)
            print(json.dumps(result, indent=2))
        
        else:
            print("Usage:")
            print("  python main.py demo      - Run full demo")
            print("  python main.py file <input> [output] - Process JSON from file")
            print("  python main.py register  - Example user registration")
            print("  python main.py matches   - Example getting matches")
            print("  python main.py           - Run demo (default)")
    
    else:
        # Default: run demo
        system.run_demo()

if __name__ == "__main__":
    main() 