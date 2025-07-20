from typing import List, Dict, Any, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
import random
import re
import numpy as np

# Load environment variables
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")
embedding_model = OpenAIEmbeddings()

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def get_embedding(text):
    return embedding_model.embed_query(text)

# --- State Definition ---
class MatchState(TypedDict):
    user: Dict[str, Any]
    candidates: List[Dict[str, Any]]
    match_scores: List[Dict[str, Any]]
    top_matches: List[Dict[str, Any]]
    attempt: int
    validated: bool
    reason: str
    messages: List[Any]

# --- Reflection Validator Model ---
class MatchReflectionValidator(BaseModel):
    is_good: bool = Field(description="Is the match list relevant and well-justified?")
    reason: str = Field(description="Reason for the evaluation.")

class MatchmakingAgent:
    """
    Agent responsible for matching users based on their give/ask profiles
    """
    
    def __init__(self):
        self.llm = llm
        self.embedding_model = embedding_model
        self.graph = self._build_workflow()
    
    def _build_workflow(self):
        """Build the LangGraph workflow for matchmaking"""
        workflow = StateGraph(MatchState)
        workflow.add_node("score_matches", self._score_matches)
        workflow.add_node("select_top_matches", self._select_top_matches)
        workflow.add_node("reflection_validate", self._reflection_validate)
        workflow.add_node("output_matches", self._output_matches)

        workflow.add_edge("score_matches", "select_top_matches")
        workflow.add_edge("select_top_matches", "reflection_validate")
        workflow.add_conditional_edges(
            "reflection_validate",
            self._refine_or_accept,
            {
                "score_matches": "score_matches",
                "output_matches": "output_matches"
            }
        )
        workflow.add_edge("output_matches", END)
        workflow.set_entry_point("score_matches")
        
        return workflow.compile()
    
    def _score_matches(self, state: MatchState) -> MatchState:
        """Score matches using LLM and semantic similarity"""
        user = state["user"]
        candidates = state["candidates"]
        match_scores = []
        
        # Handle both 'ask' and 'take' field names
        user_ask = user.get("ask", user.get("take", ""))
        user_give_emb = get_embedding(user["give"])
        user_ask_emb = get_embedding(user_ask)
        
        for other in candidates:
            other_ask = other.get("ask", other.get("take", ""))
            other_give_emb = get_embedding(other["give"])
            other_ask_emb = get_embedding(other_ask)
            
            # Compute partial match scores
            ask_give_sim = cosine_similarity(user_ask_emb, other_give_emb)
            give_ask_sim = cosine_similarity(user_give_emb, other_ask_emb)
            avg_sim = (ask_give_sim + give_ask_sim) / 2
            
            prompt = (
                f"User's give: {user['give']}\nUser's ask: {user_ask}\n"
                f"Other's give: {other['give']}\nOther's ask: {other_ask}\n"
                f"Semantic similarity (user ask <-> other give): {ask_give_sim:.2f}\n"
                f"Semantic similarity (user give <-> other ask): {give_ask_sim:.2f}\n"
                "Score this match 0-1 and explain why, considering both the explicit info and the similarity scores."
            )
            messages = [
                {"role": "system", "content": "You are a networking matchmaker. Score and explain."},
                {"role": "user", "content": prompt},
            ]
            result = self.llm.invoke(messages).content
            score_match = re.search(r"([01](?:\.\d+)?)", result)
            llm_score = float(score_match.group(1)) if score_match else random.uniform(0.4, 0.8)
            
            # Blend LLM and similarity score
            final_score = 0.7 * llm_score + 0.3 * avg_sim
            
            match_scores.append({
                "name": other["name"],
                "linkedin_url": other["linkedin_url"],
                "title": other.get("title", ""),
                "summary": other.get("summary", ""),
                "tags": other.get("tags", []),
                "score": final_score,
                "llm_score": llm_score,
                "similarity": avg_sim,
                "reason": result
            })
        
        state["match_scores"] = match_scores
        return state
    
    def _select_top_matches(self, state: MatchState) -> MatchState:
        """Select top matches based on scores"""
        match_scores = state["match_scores"]
        match_scores.sort(key=lambda x: x["score"], reverse=True)
        state["top_matches"] = match_scores[:3]
        return state
    
    def _reflection_validate(self, state: MatchState) -> MatchState:
        """Validate matches using reflection"""
        user = state["user"]
        matches = state["top_matches"]
        user_ask = user.get("ask", user.get("take", ""))
        prompt = (
            f"User: {user['name']}\nAsk: {user_ask}\nGive: {user['give']}\n"
            f"Matches: {matches}\n"
            "Is this a good set of matches for the user, based on their ask/give? Answer True/False and explain."
        )
        messages = [
            {"role": "system", "content": "You are a strict reviewer of networking matches."},
            {"role": "user", "content": prompt},
        ]
        result = self.llm.with_structured_output(MatchReflectionValidator).invoke(messages)
        state["validated"] = result.is_good
        state["reason"] = result.reason
        return state
    
    def _refine_or_accept(self, state: MatchState) -> str:
        """Decide whether to refine or accept matches"""
        if state["validated"]:
            return "output_matches"
        elif state["attempt"] >= 2:
            return "output_matches"
        else:
            state["attempt"] += 1
            return "score_matches"
    
    def _output_matches(self, state: MatchState) -> MatchState:
        """Generate final match output"""
        user = state["user"]
        matches = state["top_matches"]
        reason = state.get("reason", "")
        
        if matches:
            response = f"Hi {user['name']}, here are your top networking matches:\n\n"
            for i, m in enumerate(matches, 1):
                response += f"**{i}. {m['name']}**\n"
                response += f"**Title:** {m['title']}\n"
                response += f"**Summary:** {m['summary']}\n"
                response += f"**Tags:** {', '.join(m['tags'])}\n"
                response += f"**LinkedIn:** {m['linkedin_url']}\n"
                response += f"**Recommendation Score:** {m['score']:.2f}\n"
                response += f"**Why:** {m['reason']}\n\n"
            response += f"**Reflection:** {reason}"
        else:
            response = "No good matches found. Try broadening your criteria."
        
        state.setdefault("messages", []).append(AIMessage(content=response))
        return state
    
    def find_matches_for_user(self, user: Dict[str, Any], all_users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find matches for a specific user"""
        candidates = [u for u in all_users if u["name"] != user["name"]]
        
        state = {
            "user": user,
            "candidates": candidates,
            "match_scores": [],
            "top_matches": [],
            "attempt": 0,
            "validated": False,
            "reason": "",
            "messages": [],
        }
        
        result = self.graph.invoke(state)
        return result
    
    def find_matches_for_all_users(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find matches for all users"""
        results = {}
        for user in users:
            result = self.find_matches_for_user(user, users)
            results[user["name"]] = result
        return results 