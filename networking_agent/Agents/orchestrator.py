import asyncio
import concurrent.futures
from typing import Dict, Any, List, Optional
from user_input_agent import UserInputAgent
from linkedin_processor_agent import LinkedInProcessorAgent
from give_take_evaluator_agent import GiveTakeEvaluatorAgent
from profile_analyzer_agent import ProfileAnalyzerAgent
from matchmaking_agent import MatchmakingAgent
from linkedin_connector import LinkedInConnector

class NetworkingOrchestrator:
    """
    Main orchestrator that coordinates all agents for the networking matchmaking system
    """
    
    def __init__(self):
        self.user_input_agent = UserInputAgent()
        self.linkedin_processor = LinkedInProcessorAgent()
        self.give_take_evaluator = GiveTakeEvaluatorAgent()
        self.profile_analyzer = ProfileAnalyzerAgent()
        self.matchmaking_agent = MatchmakingAgent()
    
    async def process_user_registration(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a new user registration with all agents
        """
        print(f"Processing registration for: {user_data.get('name', 'Unknown')}")
        
        # Step 1: Validate and enhance user input
        enhanced_user_data = self.user_input_agent.process_user_registration(user_data)
        
        # Step 2: Trigger LinkedIn scraping (simulated for now)
        linkedin_data = await self._scrape_linkedin_profile(enhanced_user_data['linkedin_url'])
        
        # Step 3: Run parallel processing
        results = await self._run_parallel_processing(enhanced_user_data, linkedin_data)
        
        return {
            "user_data": enhanced_user_data,
            "linkedin_data": linkedin_data,
            "processing_results": results,
            "status": "completed"
        }
    
    async def get_user_matches(self, user_data: Dict[str, Any], all_users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get matches for a specific user
        """
        print(f"Finding matches for: {user_data.get('name', 'Unknown')}")
        
        # Process the user if not already processed
        if 'processing_results' not in user_data:
            user_data = await self.process_user_registration(user_data)
        
        # Extract the actual user data for matchmaking
        actual_user_data = user_data.get('user_data', user_data)
        
        # Prepare candidates list with proper structure
        candidates = []
        for other_user in all_users:
            if isinstance(other_user, dict) and 'user_data' in other_user:
                # This is a processed user
                candidate_data = other_user['user_data']
                # Add LinkedIn summary and tags if available
                if 'processing_results' in other_user:
                    linkedin_summary = other_user['processing_results'].get('linkedin_summary', {})
                    profile_analysis = other_user['processing_results'].get('profile_analysis', {})
                    candidate_data.update({
                        'summary': linkedin_summary.get('summary', ''),
                        'tags': linkedin_summary.get('tags', []),
                        'title': other_user.get('linkedin_data', {}).get('title', ''),
                        'profile_analysis': profile_analysis
                    })
                candidates.append(candidate_data)
            else:
                # This is a raw user
                candidates.append(other_user)
        
        # Get matches using the matchmaking agent
        matches_result = self.matchmaking_agent.find_matches_for_user(actual_user_data, candidates)
        
        # Format the results for frontend display
        formatted_matches = self._format_matches_for_display(matches_result, user_data)
        
        return {
            "user": user_data,
            "matches": formatted_matches,
            "total_matches": len(formatted_matches)
        }
    
    async def get_all_user_matches(self, users_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get matches for all users in the system
        """
        print(f"Processing matches for {len(users_data)} users")
        
        # Process all users first
        processed_users = []
        for user_data in users_data:
            processed_user = await self.process_user_registration(user_data)
            processed_users.append(processed_user)
        
        # Get matches for all users
        all_matches = {}
        for user in processed_users:
            user_matches = await self.get_user_matches(user, processed_users)
            all_matches[user['user_data']['name']] = user_matches
        
        return {
            "users": processed_users,
            "all_matches": all_matches,
            "total_users": len(processed_users)
        }
    
    async def _scrape_linkedin_profile(self, linkedin_url: str) -> Dict[str, Any]:
        """
        Simulate LinkedIn scraping (replace with actual scraper integration)
        """
        # This is a placeholder - replace with your actual LinkedIn scraper
        print(f"Scraping LinkedIn profile: {linkedin_url}")
        
        # Simulated delay for scraping
        await asyncio.sleep(1)
        
        # Return mock LinkedIn data (replace with actual scraper output)
        return {
            "title": "Senior Software Engineer",
            "bio": "Experienced developer with expertise in Python and cloud technologies",
            "experience": [
                "Senior Software Engineer at TechCorp (2020-Present)",
                "Software Engineer at StartupXYZ (2018-2020)"
            ],
            "education": [
                "BS Computer Science, University of Technology"
            ]
        }
    
    async def _run_parallel_processing(self, user_data: Dict[str, Any], linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all processing agents in parallel
        """
        print("Running parallel processing with all agents...")
        
        # Create tasks for parallel execution
        tasks = [
            self._evaluate_give_take(user_data),
            self._analyze_profile(user_data, linkedin_data),
            self._generate_linkedin_summary(linkedin_data)
        ]
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks)
        
        return {
            "give_take_evaluation": results[0],
            "profile_analysis": results[1],
            "linkedin_summary": results[2]
        }
    
    async def _evaluate_give_take(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate user's give/take quality
        """
        return self.give_take_evaluator.evaluate_user_give_take(user_data)
    
    async def _analyze_profile(self, user_data: Dict[str, Any], linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user profile comprehensively
        """
        return self.profile_analyzer.analyze_user_profile(user_data, linkedin_data)
    
    async def _generate_linkedin_summary(self, linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate LinkedIn summary and tags
        """
        return self.linkedin_processor.generate_profile_summary_and_tags(linkedin_data)
    
    def _format_matches_for_display(self, matches_result: Dict[str, Any], user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format match results for frontend display
        """
        formatted_matches = []
        
        for match in matches_result.get('top_matches', []):
            # Calculate match percentage
            match_percentage = int(match['score'] * 100)
            
            # Get profile analysis for the match
            match_profile_analysis = match.get('profile_analysis', {})
            
            formatted_match = {
                "name": match['name'],
                "linkedin_url": match['linkedin_url'],
                "title": match.get('title', ''),
                "summary": match_profile_analysis.get('professional_summary', ''),
                "tags": match_profile_analysis.get('all_tags', []),
                "match_percentage": match_percentage,
                "match_score": match['score'],
                "reasoning": match.get('reason', ''),
                "skills_tags": match_profile_analysis.get('skills_tags', []),
                "industry_tags": match_profile_analysis.get('industry_tags', []),
                "networking_tags": match_profile_analysis.get('networking_tags', []),
                "career_stage": match_profile_analysis.get('career_stage', ''),
                "networking_persona": match_profile_analysis.get('networking_persona', '')
            }
            
            formatted_matches.append(formatted_match)
        
        # Sort by match percentage (highest first)
        formatted_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        return formatted_matches
    
    def get_user_dashboard_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive dashboard data for a user
        """
        if 'processing_results' not in user_data:
            raise ValueError("User data must be processed first")
        
        results = user_data['processing_results']
        
        return {
            "user_info": {
                "name": user_data['user_data']['name'],
                "linkedin_url": user_data['user_data']['linkedin_url'],
                "about": user_data['user_data']['about'],
                "give": user_data['user_data']['give'],
                "take": user_data['user_data']['take']
            },
            "profile_analysis": results['profile_analysis'],
            "give_take_evaluation": results['give_take_evaluation'],
            "linkedin_summary": results['linkedin_summary'],
            "networking_recommendations": self.profile_analyzer.generate_networking_recommendations(
                user_data['user_data'], 
                user_data.get('linkedin_data')
            )
        }

# Synchronous wrapper for easier integration
class NetworkingOrchestratorSync:
    """
    Synchronous wrapper for the orchestrator
    """
    
    def __init__(self):
        self.orchestrator = NetworkingOrchestrator()
    
    def process_user_registration(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous version of user registration processing
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.orchestrator.process_user_registration(user_data))
        finally:
            loop.close()
    
    def get_user_matches(self, user_data: Dict[str, Any], all_users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronous version of getting user matches
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.orchestrator.get_user_matches(user_data, all_users))
        finally:
            loop.close()
    
    def get_all_user_matches(self, users_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronous version of getting all user matches
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.orchestrator.get_all_user_matches(users_data))
        finally:
            loop.close()
    
    def get_user_dashboard_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous version of getting user dashboard data
        """
        return self.orchestrator.get_user_dashboard_data(user_data) 

    def scrape_linkedin_profile(self, linkedin_url: str, gmi_api_key: str = None) -> str:
        """
        Scrape a LinkedIn profile using LinkedinConnector and return the response.
        """
        connector = LinkedInConnector(gmi_api_key=gmi_api_key)
        return connector.scrape_profile(linkedin_url) 