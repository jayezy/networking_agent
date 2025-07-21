from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

class UserInput(BaseModel):
    """User input data structure"""
    name: str = Field(..., description="Full name of the user")
    linkedin_url: str = Field(..., description="LinkedIn profile URL")
    user_id: str = Field(..., description="Unique user id")
    about: str = Field(..., description="Quick summary about the user")
    give: str = Field(..., description="What the user can offer to others")
    take: str = Field(..., description="What the user is looking for")
    
    @validator('linkedin_url')
    def validate_linkedin_url(cls, v):
        if not v.startswith('https://www.linkedin.com/'):
            raise ValueError('LinkedIn URL must start with https://www.linkedin.com/')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @validator('about', 'give', 'take')
    def validate_text_fields(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Text fields must be at least 10 characters long')
        return v.strip()

class UserInputAgent:
    """
    Agent responsible for processing and validating user input
    """
    
    def __init__(self):
        self.llm = llm
    
    def validate_user_input(self, user_data: Dict[str, Any]) -> UserInput:
        """
        Validate and process user input data
        """
        try:
            user_input = UserInput(**user_data)
            return user_input
        except Exception as e:
            raise ValueError(f"Invalid user input: {str(e)}")
    
    def enhance_user_input(self, user_input: UserInput) -> Dict[str, Any]:
        """
        Enhance user input with additional processing
        """
        # Clean and enhance the input
        enhanced_data = {
            "name": user_input.name,
            "user_id": user_input.user_id,
            "linkedin_url": user_input.linkedin_url,
            "about": user_input.about,
            "give": user_input.give,
            "take": user_input.take,
            "input_quality_score": self._assess_input_quality(user_input)
        }
        
        return enhanced_data
    
    def _assess_input_quality(self, user_input: UserInput) -> float:
        """
        Assess the quality of user input (0-1 score)
        """
        prompt = f"""
        Assess the quality and completeness of this user's networking profile input:
        
        Name: {user_input.name}
        About: {user_input.about}
        Give: {user_input.give}
        Take: {user_input.take}
        
        Rate the quality from 0-1 based on:
        - Completeness of information
        - Specificity of give/take statements
        - Professional tone and clarity
        - Potential for meaningful networking matches
        
        Return only a number between 0 and 1.
        """
        
        try:
            response = self.llm.invoke(prompt)
            score = float(response.content.strip())
            return max(0.0, min(1.0, score))  # Clamp between 0 and 1
        except:
            return 0.5  # Default score if parsing fails
    
    def process_user_registration(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete user registration process
        """
        # Validate input
        user_input = self.validate_user_input(user_data)
        
        # Enhance input
        enhanced_data = self.enhance_user_input(user_input)
        
        return enhanced_data 