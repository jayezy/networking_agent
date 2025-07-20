from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

class GiveTakeEvaluation(BaseModel):
    """Evaluation result for give/take compatibility"""
    compatibility_score: float = Field(description="Overall compatibility score (0-1)")
    give_quality_score: float = Field(description="Quality of what user can offer (0-1)")
    take_quality_score: float = Field(description="Quality of what user is seeking (0-1)")
    reasoning: str = Field(description="Detailed reasoning for the scores")
    match_potential: str = Field(description="Assessment of networking potential")

class GiveTakeEvaluatorAgent:
    """
    Agent responsible for evaluating give/take statements and generating compatibility scores
    """
    
    def __init__(self):
        self.llm = llm
    
    def evaluate_user_give_take(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a single user's give/take quality
        """
        prompt = f"""
        Evaluate the quality and networking potential of this user's give/take statements:
        
        Name: {user_data.get('name', 'Unknown')}
        About: {user_data.get('about', '')}
        Give: {user_data.get('give', '')}
        Take: {user_data.get('take', '')}
        
        Assess:
        1. Give Quality (0-1): How valuable and specific is what they can offer?
        2. Take Quality (0-1): How clear and actionable is what they're seeking?
        3. Overall Networking Potential: How likely are they to make meaningful connections?
        
        Provide detailed reasoning for each score.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert networking coach evaluating professional networking profiles."},
            {"role": "user", "content": prompt}
        ]
        
        result = self.llm.with_structured_output(GiveTakeEvaluation).invoke(messages)
        
        return {
            "give_quality_score": result.give_quality_score,
            "take_quality_score": result.take_quality_score,
            "overall_quality_score": result.compatibility_score,
            "evaluation_reasoning": result.reasoning,
            "match_potential": result.match_potential
        }
    
    def evaluate_compatibility_between_users(self, user1: Dict[str, Any], user2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate compatibility between two users based on their give/take
        """
        prompt = f"""
        Evaluate the networking compatibility between these two users:
        
        USER 1:
        Name: {user1.get('name', 'Unknown')}
        About: {user1.get('about', '')}
        Give: {user1.get('give', '')}
        Take: {user1.get('take', '')}
        
        USER 2:
        Name: {user2.get('name', 'Unknown')}
        About: {user2.get('about', '')}
        Give: {user2.get('give', '')}
        Take: {user2.get('take', '')}
        
        Assess their compatibility based on:
        1. Does User 1's "give" match User 2's "take"?
        2. Does User 2's "give" match User 1's "take"?
        3. Overall networking potential and synergy
        
        Provide a compatibility score (0-1) and detailed reasoning.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert networking matchmaker evaluating compatibility between professionals."},
            {"role": "user", "content": prompt}
        ]
        
        result = self.llm.with_structured_output(GiveTakeEvaluation).invoke(messages)
        
        return {
            "compatibility_score": result.compatibility_score,
            "give_take_match_score": (result.give_quality_score + result.take_quality_score) / 2,
            "reasoning": result.reasoning,
            "match_potential": result.match_potential
        }
    
    def evaluate_all_users(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate all users and their pairwise compatibility
        """
        results = {
            "individual_evaluations": {},
            "pairwise_compatibility": {},
            "overall_statistics": {}
        }
        
        # Evaluate individual users
        for user in users:
            user_name = user.get('name', 'Unknown')
            results["individual_evaluations"][user_name] = self.evaluate_user_give_take(user)
        
        # Evaluate pairwise compatibility
        for i, user1 in enumerate(users):
            user1_name = user1.get('name', 'Unknown')
            for j, user2 in enumerate(users):
                if i != j:  # Don't compare user with themselves
                    user2_name = user2.get('name', 'Unknown')
                    pair_key = f"{user1_name}__{user2_name}"
                    reverse_key = f"{user2_name}__{user1_name}"
                    
                    # Only evaluate each pair once
                    if pair_key not in results["pairwise_compatibility"] and reverse_key not in results["pairwise_compatibility"]:
                        compatibility = self.evaluate_compatibility_between_users(user1, user2)
                        results["pairwise_compatibility"][pair_key] = compatibility
        
        # Calculate overall statistics
        individual_scores = [eval_data["overall_quality_score"] for eval_data in results["individual_evaluations"].values()]
        compatibility_scores = [comp_data["compatibility_score"] for comp_data in results["pairwise_compatibility"].values()]
        
        results["overall_statistics"] = {
            "average_individual_quality": sum(individual_scores) / len(individual_scores) if individual_scores else 0,
            "average_compatibility_score": sum(compatibility_scores) / len(compatibility_scores) if compatibility_scores else 0,
            "total_users": len(users),
            "total_pairs_evaluated": len(results["pairwise_compatibility"])
        }
        
        return results
    
    def get_user_compatibility_scores(self, target_user: Dict[str, Any], all_users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Get compatibility scores for a target user against all other users
        """
        compatibility_scores = []
        
        for other_user in all_users:
            if other_user.get('name') != target_user.get('name'):
                compatibility = self.evaluate_compatibility_between_users(target_user, other_user)
                compatibility_scores.append({
                    "user": other_user,
                    "compatibility_score": compatibility["compatibility_score"],
                    "reasoning": compatibility["reasoning"],
                    "match_potential": compatibility["match_potential"]
                })
        
        # Sort by compatibility score (highest first)
        compatibility_scores.sort(key=lambda x: x["compatibility_score"], reverse=True)
        
        return compatibility_scores 