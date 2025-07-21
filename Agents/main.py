#!/usr/bin/env python3
"""
Main networking agent system - consolidated and simplified
Handles the complete workflow from user input to match generation
"""

import asyncio
import json
import os
import sys
import argparse
from typing import Dict, List, Any
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager
from linkedin_connector import LinkedInConnector
from linkedin_processor_agent import LinkedInProcessorAgent
from matchmaking_agent import MatchmakingAgent

class NetworkingAgent:
    """
    Consolidated networking agent that handles the complete workflow
    """
    
    def __init__(self):
        self.data_manager = DataManager()
        self.linkedin_connector = LinkedInConnector()
        self.linkedin_processor = LinkedInProcessorAgent()
        self.matchmaking_agent = MatchmakingAgent()
    
    def process_new_user(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a new user registration from frontend form data
        """
        print(f"Processing new user registration...")
        
        # Convert form data to user data format
        user_data = self.data_manager.convert_form_data_to_user_data(form_data)
        
        if not user_data:
            return {"error": "Failed to convert form data"}
        
        # Add user to sample data
        success = self.data_manager.add_user_data(user_data)
        if not success:
            return {"error": "Failed to save user data"}
        
        # Process LinkedIn data
        linkedin_result = self._process_linkedin_data(user_data)
        
        # Update user with LinkedIn data
        if linkedin_result.get('success'):
            self.data_manager.update_user_with_linkedin_data(
                user_data['user_id'], 
                linkedin_result['linkedin_data']
            )
        
        return {
            "success": True,
            "user_id": user_data['user_id'],
            "linkedin_processed": linkedin_result.get('success', False),
            "message": "User registered successfully"
        }
    
    def _process_linkedin_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process LinkedIn data for a user
        """
        try:
            linkedin_url = user_data.get('linkedin_url')
            if not linkedin_url:
                return {"success": False, "error": "No LinkedIn URL provided"}
            
            print(f"Processing LinkedIn data for: {linkedin_url}")
            
            # Scrape LinkedIn profile
            linkedin_raw_data = self.linkedin_connector.scrape_profile(linkedin_url)
            
            if not linkedin_raw_data:
                return {"success": False, "error": "Failed to scrape LinkedIn profile"}
            
            # Process LinkedIn data with the processor agent
            processed_data = self.linkedin_processor.generate_profile_summary_and_tags(linkedin_raw_data)
            
            return {
                "success": True,
                "linkedin_data": {
                    "raw_data": linkedin_raw_data,
                    "processed_data": processed_data
                }
            }
        except Exception as e:
            print(f"Error processing LinkedIn data: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_matches_for_all_users(self) -> Dict[str, Any]:
        """
        Generate matches for all users in the system
        """
        print("Generating matches for all users...")
        
        # Load all users with LinkedIn data
        users = self.data_manager.get_all_users_with_linkedin_data()
        
        if len(users) < 2:
            return {
                "success": False,
                "error": "Need at least 2 users with LinkedIn data to generate matches"
            }
        
        # Prepare users for matchmaking
        prepared_users = []
        for user in users:
            prepared_user = {
                "name": user.get('name', 'Unknown'),
                "linkedin_url": user.get('linkedin_url', ''),
                "give": user.get('give', ''),
                "take": user.get('take', ''),
                "interests": user.get('interests', ''),
                "linkedin_data": user.get('linkedin_data', {}),
                "user_id": user.get('user_id', '')
            }
            
            # Add LinkedIn summary and tags if available
            if user.get('linkedin_data'):
                linkedin_data = user['linkedin_data']
                if 'processed_data' in linkedin_data:
                    processed = linkedin_data['processed_data']
                    prepared_user.update({
                        'summary': processed.get('summary', ''),
                        'tags': processed.get('tags', []),
                        'title': linkedin_data.get('raw_data', {}).get('title', '')
                    })
            
            prepared_users.append(prepared_user)
        
        # Generate matches using the matchmaking agent
        try:
            matches_result = self.matchmaking_agent.find_matches_for_all_users(prepared_users)
            
            # Save matches data
            self.data_manager.save_matches_data(matches_result)
            
            return {
                "success": True,
                "matches": matches_result,
                "total_users": len(prepared_users),
                "message": f"Generated matches for {len(prepared_users)} users"
            }
        except Exception as e:
            print(f"Error generating matches: {e}")
            return {"success": False, "error": str(e)}
    
    def get_matches_for_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get matches for a specific user
        """
        print(f"Getting matches for user: {user_id}")
        
        # Get user data
        user = self.data_manager.get_user_by_id(user_id)
        if not user:
            return {"error": "User not found"}
        
        # Load all users
        all_users = self.data_manager.get_all_users_with_linkedin_data()
        
        # Prepare user for matchmaking
        prepared_user = {
            "name": user.get('name', 'Unknown'),
            "linkedin_url": user.get('linkedin_url', ''),
            "give": user.get('give', ''),
            "take": user.get('take', ''),
            "interests": user.get('interests', ''),
            "linkedin_data": user.get('linkedin_data', {}),
            "user_id": user.get('user_id', '')
        }
        
        # Add LinkedIn summary and tags if available
        if user.get('linkedin_data'):
            linkedin_data = user['linkedin_data']
            if 'processed_data' in linkedin_data:
                processed = linkedin_data['processed_data']
                prepared_user.update({
                    'summary': processed.get('summary', ''),
                    'tags': processed.get('tags', []),
                    'title': linkedin_data.get('raw_data', {}).get('title', '')
                })
        
        # Prepare all other users as candidates
        candidates = []
        for other_user in all_users:
            if other_user.get('user_id') != user_id:
                candidate = {
                    "name": other_user.get('name', 'Unknown'),
                    "linkedin_url": other_user.get('linkedin_url', ''),
                    "give": other_user.get('give', ''),
                    "take": other_user.get('take', ''),
                    "interests": other_user.get('interests', ''),
                    "linkedin_data": other_user.get('linkedin_data', {}),
                    "user_id": other_user.get('user_id', '')
                }
                
                # Add LinkedIn summary and tags if available
                if other_user.get('linkedin_data'):
                    linkedin_data = other_user['linkedin_data']
                    if 'processed_data' in linkedin_data:
                        processed = linkedin_data['processed_data']
                        candidate.update({
                            'summary': processed.get('summary', ''),
                            'tags': processed.get('tags', []),
                            'title': linkedin_data.get('raw_data', {}).get('title', '')
                        })
                
                candidates.append(candidate)
        
        # Get matches
        try:
            matches_result = self.matchmaking_agent.find_matches_for_user(prepared_user, candidates)
            
            return {
                "success": True,
                "user": prepared_user,
                "matches": matches_result.get('matches', []),
                "total_matches": len(matches_result.get('matches', []))
            }
        except Exception as e:
            print(f"Error getting matches for user: {e}")
            return {"success": False, "error": str(e)}
    
    def get_all_matches(self) -> Dict[str, Any]:
        """
        Get all matches data
        """
        matches_data = self.data_manager.load_matches_data()
        return matches_data
    
    def get_sample_data(self) -> Dict[str, Any]:
        """
        Get sample data
        """
        sample_data = self.data_manager.load_sample_data()
        return {
            "success": True,
            "sample_data": sample_data,
            "total_users": len(sample_data)
        }

def main():
    """
    Main function for handling command line arguments and testing
    """
    parser = argparse.ArgumentParser(description='Networking Agent System')
    parser.add_argument('--action', type=str, help='Action to perform')
    parser.add_argument('--data', type=str, help='JSON data for processing')
    parser.add_argument('--user_id', type=str, help='User ID for specific actions')
    
    args = parser.parse_args()
    
    agent = NetworkingAgent()
    
    try:
        if args.action == 'process_user':
            if not args.data:
                print(json.dumps({"error": "No data provided"}))
                return
            
            form_data = json.loads(args.data)
            result = agent.process_new_user(form_data)
            print(json.dumps(result))
            
        elif args.action == 'generate_matches':
            result = agent.generate_matches_for_all_users()
            print(json.dumps(result))
            
        elif args.action == 'get_user_matches':
            if not args.user_id:
                print(json.dumps({"error": "No user_id provided"}))
                return
            
            result = agent.get_matches_for_user(args.user_id)
            print(json.dumps(result))
            
        elif args.action == 'get_all_matches':
            result = agent.get_all_matches()
            print(json.dumps(result))
            
        elif args.action == 'get_sample_data':
            result = agent.get_sample_data()
            print(json.dumps(result))
            
        else:
            # Default test mode
            print("Testing networking agent system...")
            
            # Load current sample data
            sample_data = agent.data_manager.load_sample_data()
            print(f"Loaded {len(sample_data)} users from sample data")
            
            # Generate matches for all users
            if len(sample_data) >= 2:
                print("Generating matches...")
                matches_result = agent.generate_matches_for_all_users()
                print(f"Matches result: {matches_result.get('success', False)}")
                
                if matches_result.get('success'):
                    print(f"Generated matches for {matches_result.get('total_users', 0)} users")
                else:
                    print(f"Error: {matches_result.get('error', 'Unknown error')}")
            else:
                print("Need at least 2 users to generate matches")
                
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main() 