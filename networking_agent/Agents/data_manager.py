from typing import List, Dict, Any

class DataManager:
    """
    Manages sample data and data utilities for the networking matchmaking system
    """
    
    @staticmethod
    def get_sample_linkedin_profiles() -> List[Dict[str, Any]]:
        """
        Get sample LinkedIn profiles for testing
        """
        return [
            {
                "name": "Deepak Yadlapalli",
                "linkedin_url": "https://www.linkedin.com/in/deepakyadlapalli/",
                "title": "Senior Cloud Architect at TechCorp",
                "bio": "Experienced cloud architect with 8+ years in AWS, Azure, and Kubernetes. Passionate about mentoring developers and contributing to open-source projects.",
                "experience": [
                    "Senior Cloud Architect at TechCorp (2020-Present)",
                    "DevOps Engineer at StartupXYZ (2018-2020)",
                    "Software Engineer at BigTech (2015-2018)"
                ],
                "education": [
                    "MS in Computer Science, Stanford University",
                    "BS in Engineering, MIT"
                ]
            },
            {
                "name": "Priya Sharma",
                "linkedin_url": "https://www.linkedin.com/in/priyasharma/",
                "title": "AI Product Manager at Google",
                "bio": "Former Google PM with expertise in AI/ML product development. Love building products that scale and mentoring aspiring PMs.",
                "experience": [
                    "AI Product Manager at Google (2021-Present)",
                    "Product Manager at StartupABC (2019-2021)",
                    "Software Engineer at TechStartup (2017-2019)"
                ],
                "education": [
                    "MBA, Harvard Business School",
                    "BS in Computer Science, UC Berkeley"
                ]
            },
            {
                "name": "Alex Kim",
                "linkedin_url": "https://www.linkedin.com/in/alexkim/",
                "title": "DevOps Lead at CloudScale",
                "bio": "DevOps and SRE expert with 6+ years experience. Conference speaker and community leader in the DevOps space.",
                "experience": [
                    "DevOps Lead at CloudScale (2021-Present)",
                    "SRE Engineer at TechGiant (2019-2021)",
                    "System Administrator at Startup (2017-2019)"
                ],
                "education": [
                    "BS in Computer Science, University of Washington",
                    "Certified Kubernetes Administrator"
                ]
            },
            {
                "name": "Sara Lee",
                "linkedin_url": "https://www.linkedin.com/in/saralee/",
                "title": "Full-Stack Engineer & Startup Founder",
                "bio": "Full-stack engineer with expertise in React, Node.js, and cloud infrastructure. Currently building my third startup.",
                "experience": [
                    "Founder & CTO at MyStartup (2022-Present)",
                    "Senior Full-Stack Engineer at TechCompany (2020-2022)",
                    "Frontend Engineer at WebAgency (2018-2020)"
                ],
                "education": [
                    "BS in Computer Science, Georgia Tech",
                    "Startup Accelerator Graduate"
                ]
            },
            {
                "name": "Mohit Patel",
                "linkedin_url": "https://www.linkedin.com/in/mohitpatel/",
                "title": "Senior Data Scientist at DataCorp",
                "bio": "Kaggle Grandmaster and data science mentor. Passionate about teaching Python and helping others break into data science.",
                "experience": [
                    "Senior Data Scientist at DataCorp (2021-Present)",
                    "Data Scientist at AnalyticsFirm (2019-2021)",
                    "Research Assistant at University (2017-2019)"
                ],
                "education": [
                    "MS in Data Science, Carnegie Mellon University",
                    "BS in Statistics, University of Michigan"
                ]
            }
        ]
    
    @staticmethod
    def validate_linkedin_profile(profile: Dict[str, Any]) -> bool:
        """
        Validate that a LinkedIn profile has the required fields
        """
        required_fields = ["name", "linkedin_url"]
        optional_fields = ["title", "bio", "experience", "education"]
        
        # Check required fields
        for field in required_fields:
            if field not in profile or not profile[field]:
                return False
        
        # Check that at least one optional field is present
        has_optional_data = any(
            field in profile and profile[field] 
            for field in optional_fields
        )
        
        return has_optional_data
    
    @staticmethod
    def format_profile_for_display(profile: Dict[str, Any]) -> str:
        """
        Format a profile for display purposes
        """
        return f"""
        Name: {profile.get('name', 'N/A')}
        Title: {profile.get('title', 'N/A')}
        LinkedIn: {profile.get('linkedin_url', 'N/A')}
        Bio: {profile.get('bio', 'N/A')}
        Experience: {len(profile.get('experience', []))} positions
        Education: {len(profile.get('education', []))} institutions
        """
    
    @staticmethod
    def get_profile_statistics(profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about a collection of profiles
        """
        total_profiles = len(profiles)
        profiles_with_title = sum(1 for p in profiles if p.get('title'))
        profiles_with_bio = sum(1 for p in profiles if p.get('bio'))
        profiles_with_experience = sum(1 for p in profiles if p.get('experience'))
        profiles_with_education = sum(1 for p in profiles if p.get('education'))
        
        return {
            "total_profiles": total_profiles,
            "profiles_with_title": profiles_with_title,
            "profiles_with_bio": profiles_with_bio,
            "profiles_with_experience": profiles_with_experience,
            "profiles_with_education": profiles_with_education,
            "completeness_rate": {
                "title": profiles_with_title / total_profiles if total_profiles > 0 else 0,
                "bio": profiles_with_bio / total_profiles if total_profiles > 0 else 0,
                "experience": profiles_with_experience / total_profiles if total_profiles > 0 else 0,
                "education": profiles_with_education / total_profiles if total_profiles > 0 else 0
            }
        } 