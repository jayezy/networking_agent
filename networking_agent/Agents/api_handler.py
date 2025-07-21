#!/usr/bin/env python3
"""
API Handler for Networking Matchmaking System
Handles JSON input/output for the complete networking flow
"""

import json
from typing import Dict, Any, List, Optional
from orchestrator import NetworkingOrchestratorSync

class NetworkingAPIHandler:
    """
    API handler for processing JSON requests and returning JSON responses
    """
    
    def __init__(self):
        self.orchestrator = NetworkingOrchestratorSync()
    
    def process_user_registration(self, json_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user registration from JSON input
        """
        try:
            # Validate required fields
            required_fields = ["user_id", "name", "linkedin_url", "about", "give", "take"]
            for field in required_fields:
                if field not in json_input:
                    return self._error_response(f"Missing required field: {field}")
            
            # Process user registration
            processed_user = self.orchestrator.process_user_registration(json_input)
            linkedin_response = self.orchestrator.scrape_linkedin_profile(processed_user.get("user_data", {}).get("linkedin_url"))
            
            # Get dashboard data
            dashboard_data = self.orchestrator.get_user_dashboard_data(processed_user)
            
            return {
                "status": "success",
                "message": f"Successfully processed user: {json_input['name']}",
                "data": {
                    "user_id": processed_user.get("user_data", {}).get("user_id"),
                    "linkedin_url": processed_user.get("user_data", {}).get("linkedin_url"),
                    "profile_analysis": dashboard_data.get("profile_analysis", {}),
                    "give_take_evaluation": dashboard_data.get("give_take_evaluation", {}),
                    "linkedin_summary": dashboard_data.get("linkedin_summary", {}),
                    "networking_recommendations": dashboard_data.get("networking_recommendations", {}),
                    "processing_timestamp": self._get_timestamp(),
                    "linkedin_extracted_data": linkedin_response
                }
            }
            
        except Exception as e:
            return self._error_response(f"Error processing user registration: {str(e)}")
    
    def get_user_matches(self, json_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get matches for a user from JSON input
        """
        try:
            # Validate required fields
            if "user" not in json_input:
                return self._error_response("Missing 'user' field in request")
            
            if "attendees" not in json_input:
                return self._error_response("Missing 'attendees' field in request")
            
            user_data = json_input["user"]
            attendees_data = json_input["attendees"]
            
            # Validate user data
            required_user_fields = ["name", "linkedin_url", "about", "give", "take"]
            for field in required_user_fields:
                if field not in user_data:
                    return self._error_response(f"Missing required user field: {field}")
            
            # Process user and get matches
            processed_user = self.orchestrator.process_user_registration(user_data)
            matches_result = self.orchestrator.get_user_matches(processed_user, attendees_data)
            
            # Format matches for JSON response
            formatted_matches = []
            for match in matches_result.get('matches', []):
                formatted_match = {
                    "name": match.get("name", ""),
                    "linkedin_url": match.get("linkedin_url", ""),
                    "title": match.get("title", ""),
                    "summary": match.get("summary", ""),
                    "tags": match.get("tags", []),
                    "match_percentage": match.get("match_percentage", 0),
                    "match_score": match.get("match_score", 0.0),
                    "skills_tags": match.get("skills_tags", []),
                    "industry_tags": match.get("industry_tags", []),
                    "networking_tags": match.get("networking_tags", []),
                    "career_stage": match.get("career_stage", ""),
                    "networking_persona": match.get("networking_persona", ""),
                    "reasoning": match.get("reasoning", "")
                }
                formatted_matches.append(formatted_match)
            
            return {
                "status": "success",
                "message": f"Found {len(formatted_matches)} matches for {user_data['name']}",
                "data": {
                    "user": {
                        "name": user_data["name"],
                        "linkedin_url": user_data["linkedin_url"]
                    },
                    "total_matches": len(formatted_matches),
                    "matches": formatted_matches,
                    "processing_timestamp": self._get_timestamp()
                }
            }
            
        except Exception as e:
            return self._error_response(f"Error getting user matches: {str(e)}")
    
    def process_event_attendees(self, json_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process all event attendees from JSON input
        """
        try:
            # Validate required fields
            if "attendees" not in json_input:
                return self._error_response("Missing 'attendees' field in request")
            
            attendees_data = json_input["attendees"]
            
            if not isinstance(attendees_data, list):
                return self._error_response("'attendees' must be a list")
            
            if len(attendees_data) == 0:
                return self._error_response("'attendees' list cannot be empty")
            
            # Validate each attendee
            required_fields = ["name", "linkedin_url", "about", "give", "take"]
            for i, attendee in enumerate(attendees_data):
                for field in required_fields:
                    if field not in attendee:
                        return self._error_response(f"Attendee {i+1} missing required field: {field}")
            
            # Process all attendees
            all_matches = self.orchestrator.get_all_user_matches(attendees_data)
            
            # Format results for JSON response
            formatted_results = {}
            for user_name, user_matches in all_matches.get('all_matches', {}).items():
                formatted_matches = []
                for match in user_matches.get('matches', []):
                    formatted_match = {
                        "name": match.get("name", ""),
                        "linkedin_url": match.get("linkedin_url", ""),
                        "title": match.get("title", ""),
                        "summary": match.get("summary", ""),
                        "tags": match.get("tags", []),
                        "match_percentage": match.get("match_percentage", 0),
                        "match_score": match.get("match_score", 0.0),
                        "skills_tags": match.get("skills_tags", []),
                        "industry_tags": match.get("industry_tags", []),
                        "networking_tags": match.get("networking_tags", []),
                        "career_stage": match.get("career_stage", ""),
                        "networking_persona": match.get("networking_persona", ""),
                        "reasoning": match.get("reasoning", "")
                    }
                    formatted_matches.append(formatted_match)
                
                formatted_results[user_name] = {
                    "total_matches": len(formatted_matches),
                    "matches": formatted_matches
                }
            
            return {
                "status": "success",
                "message": f"Successfully processed {all_matches.get('total_users', 0)} attendees",
                "data": {
                    "total_users": all_matches.get('total_users', 0),
                    "user_matches": formatted_results,
                    "processing_timestamp": self._get_timestamp()
                }
            }
            
        except Exception as e:
            return self._error_response(f"Error processing event attendees: {str(e)}")
    
    def get_user_dashboard(self, json_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive dashboard data for a user
        """
        try:
            # Validate required fields
            if "user" not in json_input:
                return self._error_response("Missing 'user' field in request")
            
            user_data = json_input["user"]
            
            # Process user if not already processed
            if "processing_results" not in user_data:
                processed_user = self.orchestrator.process_user_registration(user_data)
            else:
                processed_user = user_data
            
            # Get dashboard data
            dashboard_data = self.orchestrator.get_user_dashboard_data(processed_user)
            
            return {
                "status": "success",
                "message": f"Dashboard data retrieved for {user_data.get('name', 'Unknown')}",
                "data": {
                    "user_info": dashboard_data.get("user_info", {}),
                    "profile_analysis": dashboard_data.get("profile_analysis", {}),
                    "give_take_evaluation": dashboard_data.get("give_take_evaluation", {}),
                    "linkedin_summary": dashboard_data.get("linkedin_summary", {}),
                    "networking_recommendations": dashboard_data.get("networking_recommendations", {}),
                    "processing_timestamp": self._get_timestamp()
                }
            }
            
        except Exception as e:
            return self._error_response(f"Error getting user dashboard: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """
        Generate standardized error response
        """
        return {
            "status": "error",
            "message": message,
            "data": None,
            "processing_timestamp": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp for processing tracking
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def process_request(self, json_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main method to process any JSON request
        """
        try:
            # Validate request structure
            if "action" not in json_request:
                return self._error_response("Missing 'action' field in request")
            
            action = json_request["action"]
            
            # Route to appropriate handler
            if action == "register_user":
                return self.process_user_registration(json_request)
            elif action == "get_matches":
                return self.get_user_matches(json_request)
            elif action == "process_event":
                return self.process_event_attendees(json_request)
            elif action == "get_dashboard":
                return self.get_user_dashboard(json_request)
            else:
                return self._error_response(f"Unknown action: {action}")
                
        except Exception as e:
            return self._error_response(f"Error processing request: {str(e)}")

# Example usage and testing
def main():
    """
    Example usage of the API handler
    """
    api_handler = NetworkingAPIHandler()
    
    # Example 1: User Registration
    registration_request = {
        "action": "register_user",
        "name": "John Doe",
        "linkedin_url": "https://www.linkedin.com/in/johndoe",
        "about": "Senior software engineer with 5+ years experience in Python and cloud technologies",
        "give": "Technical mentorship, code review expertise, and cloud architecture guidance",
        "take": "AI/ML project opportunities, startup connections, and speaking opportunities"
    }
    
    print("=== User Registration ===")
    registration_response = api_handler.process_request(registration_request)
    print(json.dumps(registration_response, indent=2))
    
    # Example 2: Get Matches
    matches_request = {
        "action": "get_matches",
        "user": {
            "name": "John Doe",
            "linkedin_url": "https://www.linkedin.com/in/johndoe",
            "about": "Senior software engineer with expertise in Python and cloud technologies",
            "give": "Technical mentorship and cloud architecture guidance",
            "take": "AI/ML project opportunities and startup connections"
        },
        "attendees": [
            {
                "name": "Jane Smith",
                "linkedin_url": "https://www.linkedin.com/in/janesmith",
                "about": "AI Product Manager with expertise in machine learning",
                "give": "Product strategy and AI project scoping",
                "take": "Technical cofounders and cloud expertise"
            }
        ]
    }
    
    print("\n=== Get Matches ===")
    matches_response = api_handler.process_request(matches_request)
    print(json.dumps(matches_response, indent=2))

if __name__ == "__main__":
    main() 