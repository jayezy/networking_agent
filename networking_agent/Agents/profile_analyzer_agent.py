from typing import Dict, Any, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

class ProfileAnalysis(BaseModel):
    """Comprehensive profile analysis result"""
    professional_summary: str = Field(description="2-3 sentence professional summary")
    networking_summary: str = Field(description="1-2 sentence networking-focused summary")
    skills_tags: List[str] = Field(description="5-8 skills and expertise tags")
    industry_tags: List[str] = Field(description="3-5 industry and domain tags")
    networking_tags: List[str] = Field(description="3-5 networking and collaboration tags")
    career_stage: str = Field(description="Career stage assessment (e.g., 'Early Career', 'Mid-Career', 'Senior')")
    networking_persona: str = Field(description="Networking persona type (e.g., 'Mentor', 'Collaborator', 'Connector')")

class ProfileAnalyzerAgent:
    """
    Agent responsible for analyzing LinkedIn profiles and user input to generate comprehensive summaries and tags
    """
    
    def __init__(self):
        self.llm = llm
    
    def analyze_user_profile(self, user_data: Dict[str, Any], linkedin_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze user profile combining LinkedIn data and user input
        """
        # Prepare combined profile data
        profile_info = f"""
        USER INPUT:
        Name: {user_data.get('name', 'Unknown')}
        About: {user_data.get('about', '')}
        Give: {user_data.get('give', '')}
        Take: {user_data.get('take', '')}
        """
        
        if linkedin_data:
            profile_info += f"""
            LINKEDIN DATA:
            Title: {linkedin_data.get('title', '')}
            Bio: {linkedin_data.get('bio', '')}
            Experience: {'; '.join(linkedin_data.get('experience', []))}
            Education: {'; '.join(linkedin_data.get('education', []))}
            """
        
        prompt = f"""
        Analyze this professional profile and create comprehensive insights for networking purposes:
        
        {profile_info}
        
        Generate:
        1. Professional Summary: 2-3 sentences about their background and expertise
        2. Networking Summary: 1-2 sentences focused on their networking value and goals
        3. Skills Tags: 5-8 specific skills and expertise areas
        4. Industry Tags: 3-5 industry and domain tags
        5. Networking Tags: 3-5 tags related to networking style and collaboration preferences
        6. Career Stage: Assess their career stage
        7. Networking Persona: Determine their primary networking persona type
        
        Focus on what makes them valuable for networking and collaboration.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert professional profile analyst specializing in networking and career development."},
            {"role": "user", "content": prompt}
        ]
        
        result = self.llm.with_structured_output(ProfileAnalysis).invoke(messages)
        
        return {
            "professional_summary": result.professional_summary,
            "networking_summary": result.networking_summary,
            "skills_tags": result.skills_tags,
            "industry_tags": result.industry_tags,
            "networking_tags": result.networking_tags,
            "career_stage": result.career_stage,
            "networking_persona": result.networking_persona,
            "all_tags": result.skills_tags + result.industry_tags + result.networking_tags
        }
    
    def compare_profiles_for_matching(self, user1: Dict[str, Any], user2: Dict[str, Any], 
                                    linkedin1: Dict[str, Any] = None, linkedin2: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Compare two profiles and generate matching insights
        """
        # Analyze both profiles
        analysis1 = self.analyze_user_profile(user1, linkedin1)
        analysis2 = self.analyze_user_profile(user2, linkedin2)
        
        # Generate comparison insights
        prompt = f"""
        Compare these two professional profiles for networking compatibility:
        
        PROFILE 1 - {user1.get('name', 'Unknown')}:
        Professional Summary: {analysis1['professional_summary']}
        Networking Summary: {analysis1['networking_summary']}
        Skills: {', '.join(analysis1['skills_tags'])}
        Industries: {', '.join(analysis1['industry_tags'])}
        Give: {user1.get('give', '')}
        Take: {user1.get('take', '')}
        
        PROFILE 2 - {user2.get('name', 'Unknown')}:
        Professional Summary: {analysis2['professional_summary']}
        Networking Summary: {analysis2['networking_summary']}
        Skills: {', '.join(analysis2['skills_tags'])}
        Industries: {', '.join(analysis2['industry_tags'])}
        Give: {user2.get('give', '')}
        Take: {user2.get('take', '')}
        
        Provide:
        1. Complementary Skills: Skills that complement each other
        2. Shared Interests: Areas of overlap or shared interests
        3. Networking Synergy: How they could benefit each other
        4. Conversation Starters: 3-5 conversation starter topics
        5. Collaboration Potential: Specific ways they could collaborate
        """
        
        messages = [
            {"role": "system", "content": "You are an expert networking matchmaker analyzing profile compatibility."},
            {"role": "user", "content": prompt}
        ]
        
        comparison_result = self.llm.invoke(messages)
        
        return {
            "profile1_analysis": analysis1,
            "profile2_analysis": analysis2,
            "comparison_insights": comparison_result.content,
            "complementary_skills": self._extract_complementary_skills(analysis1, analysis2),
            "shared_interests": self._extract_shared_interests(analysis1, analysis2)
        }
    
    def _extract_complementary_skills(self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]) -> List[str]:
        """
        Extract complementary skills between two profiles
        """
        skills1 = set(analysis1['skills_tags'])
        skills2 = set(analysis2['skills_tags'])
        
        # Find skills that are in one profile but not the other (complementary)
        complementary = list(skills1.symmetric_difference(skills2))
        
        return complementary[:5]  # Return top 5 complementary skills
    
    def _extract_shared_interests(self, analysis1: Dict[str, Any], analysis2: Dict[str, Any]) -> List[str]:
        """
        Extract shared interests between two profiles
        """
        all_tags1 = set(analysis1['all_tags'])
        all_tags2 = set(analysis2['all_tags'])
        
        # Find overlapping tags
        shared = list(all_tags1.intersection(all_tags2))
        
        return shared[:5]  # Return top 5 shared interests
    
    def generate_networking_recommendations(self, user_data: Dict[str, Any], 
                                          linkedin_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate specific networking recommendations for a user
        """
        analysis = self.analyze_user_profile(user_data, linkedin_data)
        
        prompt = f"""
        Based on this profile analysis, generate specific networking recommendations:
        
        Profile Analysis:
        Professional Summary: {analysis['professional_summary']}
        Networking Summary: {analysis['networking_summary']}
        Skills: {', '.join(analysis['skills_tags'])}
        Industries: {', '.join(analysis['industry_tags'])}
        Career Stage: {analysis['career_stage']}
        Networking Persona: {analysis['networking_persona']}
        Give: {user_data.get('give', '')}
        Take: {user_data.get('take', '')}
        
        Provide:
        1. Target Networking Groups: 3-5 types of people they should connect with
        2. Conversation Topics: 5-7 topics they can discuss
        3. Value Proposition: How they should present their value
        4. Networking Goals: Specific networking objectives
        5. Follow-up Strategies: How to maintain connections
        """
        
        messages = [
            {"role": "system", "content": "You are an expert networking coach providing personalized recommendations."},
            {"role": "user", "content": prompt}
        ]
        
        recommendations = self.llm.invoke(messages)
        
        return {
            "profile_analysis": analysis,
            "networking_recommendations": recommendations.content
        } 