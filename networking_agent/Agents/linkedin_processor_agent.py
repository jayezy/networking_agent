from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

# --- LinkedIn Data Structure ---
class LinkedInProfile(BaseModel):
    name: str
    linkedin_url: str
    title: str = ""
    bio: str = ""
    experience: List[str] = []
    education: List[str] = []

# --- Summary and Tags Generator Models ---
class ProfileSummary(BaseModel):
    summary: str = Field(description="A concise 2-3 sentence summary of the person's background, expertise, and what they can offer")
    tags: List[str] = Field(description="5-8 relevant tags that capture their skills, industry, and expertise")

class LinkedInProcessorAgent:
    """
    Agent responsible for processing LinkedIn profile data and generating summaries and tags
    """
    
    def __init__(self):
        self.llm = llm
    
    def generate_profile_summary_and_tags(self, linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary and tags for a LinkedIn profile
        """
        # Prepare the profile data
        profile_text = f"""
        Name: {linkedin_data.get('name', 'N/A')}
        Title: {linkedin_data.get('title', 'N/A')}
        Bio: {linkedin_data.get('bio', 'N/A')}
        Experience: {'; '.join(linkedin_data.get('experience', []))}
        Education: {'; '.join(linkedin_data.get('education', []))}
        """
        
        prompt = f"""
        Based on the following LinkedIn profile information, generate a concise summary and relevant tags.
        
        Profile Information:
        {profile_text}
        
        Please provide:
        1. A 2-3 sentence summary that captures their background, expertise, and what they can offer
        2. 5-8 relevant tags that represent their skills, industry, and expertise
        
        Focus on what makes this person valuable for networking and collaboration.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at analyzing professional profiles and extracting key insights for networking purposes."},
            {"role": "user", "content": prompt}
        ]
        
        result = self.llm.with_structured_output(ProfileSummary).invoke(messages)
        
        return {
            "summary": result.summary,
            "tags": result.tags
        }
    
    def extract_give_from_profile(self, profile: Dict[str, Any]) -> str:
        """
        Extract what the person can offer based on their profile
        """
        title = profile.get("title", "")
        bio = profile.get("bio", "")
        experience = " ".join(profile.get("experience", []))
        
        prompt = f"""
        Based on this person's professional information, what can they offer to others in a networking context?
        
        Title: {title}
        Bio: {bio}
        Experience: {experience}
        
        Provide a concise statement (1-2 sentences) of what they can give/offer to others.
        Focus on their expertise, skills, knowledge, or connections they can share.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at identifying what professionals can offer in networking contexts."},
            {"role": "user", "content": prompt}
        ]
        
        result = self.llm.invoke(messages)
        return result.content.strip()
    
    def extract_ask_from_profile(self, profile: Dict[str, Any]) -> str:
        """
        Extract what the person is looking for based on their profile
        """
        title = profile.get("title", "")
        bio = profile.get("bio", "")
        experience = " ".join(profile.get("experience", []))
        
        prompt = f"""
        Based on this person's professional information, what are they likely looking for in a networking context?
        
        Title: {title}
        Bio: {bio}
        Experience: {experience}
        
        Provide a concise statement (1-2 sentences) of what they might be seeking.
        Consider their career stage, industry, and current role.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at identifying what professionals are seeking in networking contexts."},
            {"role": "user", "content": prompt}
        ]
        
        result = self.llm.invoke(messages)
        return result.content.strip()
    
    def process_linkedin_profiles(self, linkedin_profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw LinkedIn data and add summaries and tags
        """
        processed_users = []
        
        for profile in linkedin_profiles:
            # Generate summary and tags
            summary_data = self.generate_profile_summary_and_tags(profile)
            
            # Create enhanced user profile
            enhanced_profile = {
                "name": profile.get("name", ""),
                "linkedin_url": profile.get("linkedin_url", ""),
                "title": profile.get("title", ""),
                "bio": profile.get("bio", ""),
                "experience": profile.get("experience", []),
                "education": profile.get("education", []),
                "summary": summary_data["summary"],
                "tags": summary_data["tags"],
                # Extract give/ask from title and bio for matching
                "give": self.extract_give_from_profile(profile),
                "ask": self.extract_ask_from_profile(profile)
            }
            
            processed_users.append(enhanced_profile)
        
        return processed_users 