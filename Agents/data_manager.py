import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class DataManager:
    """
    Manages data operations for the networking agent system
    """
    
    def __init__(self, data_dir: str = "Database"):
        self.data_dir = data_dir
        self.sample_data_file = os.path.join(data_dir, "sample_data.json")
        self.processed_data_file = os.path.join(data_dir, "processed_data.json")
        self.matches_data_file = os.path.join(data_dir, "matches_data.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def load_sample_data(self) -> List[Dict[str, Any]]:
        """Load sample data from JSON file"""
        try:
            if os.path.exists(self.sample_data_file):
                with open(self.sample_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default sample data if file doesn't exist
                default_data = [{
                    "user_id": "jay",
                    "name": "Jay",
                    "email": "jayezy7@gmail.com",
                    "give": "experienced in product leadership, good at 0-1 projects",
                    "take": "mentorship",
                    "linkedin_url": "https://www.linkedin.com/in/agrawalrinkal/"
                }]
                self.save_sample_data(default_data)
                return default_data
        except Exception as e:
            print(f"Error loading sample data: {e}")
            return []
    
    def save_sample_data(self, data: List[Dict[str, Any]]) -> bool:
        """Save sample data to JSON file"""
        try:
            with open(self.sample_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving sample data: {e}")
            return False
    
    def add_user_data(self, user_data: Dict[str, Any]) -> bool:
        """Add new user data to the sample data file"""
        try:
            current_data = self.load_sample_data()
            
            # Generate user_id if not provided
            if 'user_id' not in user_data:
                user_data['user_id'] = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(current_data)}"
            
            # Add timestamp
            user_data['timestamp'] = datetime.now().isoformat()
            
            # Check if user already exists (by user_id or linkedin_url)
            existing_user = None
            for i, user in enumerate(current_data):
                if (user.get('user_id') == user_data['user_id'] or 
                    user.get('linkedin_url') == user_data.get('linkedin_url')):
                    existing_user = i
                    break
            
            if existing_user is not None:
                # Update existing user
                current_data[existing_user].update(user_data)
            else:
                # Add new user
                current_data.append(user_data)
            
            return self.save_sample_data(current_data)
        except Exception as e:
            print(f"Error adding user data: {e}")
            return False
    
    def update_user_with_linkedin_data(self, user_id: str, linkedin_data: Dict[str, Any]) -> bool:
        """Update user data with LinkedIn information"""
        try:
            current_data = self.load_sample_data()
            
            for user in current_data:
                if user.get('user_id') == user_id:
                    user.update({
                        'linkedin_data': linkedin_data,
                        'linkedin_processed': True,
                        'linkedin_processed_at': datetime.now().isoformat()
                    })
                    return self.save_sample_data(current_data)
            
            print(f"User with ID {user_id} not found")
            return False
        except Exception as e:
            print(f"Error updating user with LinkedIn data: {e}")
            return False
    
    def save_processed_data(self, processed_data: List[Dict[str, Any]]) -> bool:
        """Save processed data (with LinkedIn info) to JSON file"""
        try:
            with open(self.processed_data_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving processed data: {e}")
            return False
    
    def load_processed_data(self) -> List[Dict[str, Any]]:
        """Load processed data from JSON file"""
        try:
            if os.path.exists(self.processed_data_file):
                with open(self.processed_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading processed data: {e}")
            return []
    
    def save_matches_data(self, matches_data: Dict[str, Any]) -> bool:
        """Save match results to JSON file"""
        try:
            # Add timestamp to matches data
            matches_data['generated_at'] = datetime.now().isoformat()
            
            with open(self.matches_data_file, 'w', encoding='utf-8') as f:
                json.dump(matches_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving matches data: {e}")
            return False
    
    def load_matches_data(self) -> Dict[str, Any]:
        """Load match results from JSON file"""
        try:
            if os.path.exists(self.matches_data_file):
                with open(self.matches_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading matches data: {e}")
            return {}
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data by user_id"""
        try:
            current_data = self.load_sample_data()
            for user in current_data:
                if user.get('user_id') == user_id:
                    return user
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def get_user_by_linkedin_url(self, linkedin_url: str) -> Optional[Dict[str, Any]]:
        """Get user data by LinkedIn URL"""
        try:
            current_data = self.load_sample_data()
            for user in current_data:
                if user.get('linkedin_url') == linkedin_url:
                    return user
            return None
        except Exception as e:
            print(f"Error getting user by LinkedIn URL: {e}")
            return None
    
    def get_all_users_with_linkedin_data(self) -> List[Dict[str, Any]]:
        """Get all users that have LinkedIn data processed"""
        try:
            current_data = self.load_sample_data()
            return [user for user in current_data if user.get('linkedin_processed', False)]
        except Exception as e:
            print(f"Error getting users with LinkedIn data: {e}")
            return []
    
    def convert_form_data_to_user_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert frontend form data to user data format"""
        try:
            # Extract responses from form data
            responses = form_data.get('responses', [])
            user_data = {
                'user_id': form_data.get('userId', ''),
                'timestamp': form_data.get('timestamp', ''),
            }
            
            # Map form responses to user data fields
            for response in responses:
                question = response.get('question', '').lower()
                answer = response.get('answer', '')
                
                if 'first name' in question:
                    user_data['first_name'] = answer
                elif 'last name' in question:
                    user_data['last_name'] = answer
                elif 'linkedin' in question:
                    user_data['linkedin_url'] = answer
                elif 'looking for' in question:
                    user_data['take'] = answer
                elif 'bring' in question:
                    user_data['give'] = answer
                elif 'spice' in question or 'interests' in question:
                    user_data['interests'] = answer
            
            # Combine first and last name
            if 'first_name' in user_data and 'last_name' in user_data:
                user_data['name'] = f"{user_data['first_name']} {user_data['last_name']}"
            
            return user_data
        except Exception as e:
            print(f"Error converting form data: {e}")
            return {} 