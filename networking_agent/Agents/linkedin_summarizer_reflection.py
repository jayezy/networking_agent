from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables (for OpenAI API key, etc.)
load_dotenv()

# Initialize the LLM (ensure your OpenAI API key is set in the environment)
llm = ChatOpenAI(model="gpt-4o")

# Mock function to fetch LinkedIn profile data from a URL (replace with real fetch if needed)
def fetch_linkedin_profile(url: str) -> str:
    if "deepakyadlapalli" in url:
        return (
            "Deepak Yadlapalli is a seasoned cloud architect with 10+ years of experience in cloud computing, AI, and enterprise solutions. "
            "He has worked at leading tech companies, delivered talks at international conferences, and is passionate about mentoring and open-source. "
            "His skills include AWS, Azure, GCP, Kubernetes, and large-scale distributed systems."
        )
    return "Profile not found."

# LLM agent to summarize the profile
def linkedin_summarizer_agent(url: str) -> str:
    profile_text = fetch_linkedin_profile(url)
    system_prompt = (
        "You are an expert career coach. Summarize the following LinkedIn profile in 3-5 sentences, focusing on key skills, experience, and unique strengths. "
        "Be concise and highlight what makes this person stand out."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": profile_text},
    ]
    summary = llm.invoke(messages)
    return summary.content

# Validator for the reflection loop
class ReflectionValidator(BaseModel):
    is_good: bool = Field(description="Is the summary clear, accurate, and does it capture the main strengths?")
    reason: str = Field(description="Reason for the evaluation.")

def reflection_validator(summary: str, profile_text: str) -> bool:
    validation_prompt = (
        "You are a strict reviewer. Given the LinkedIn profile and its summary, answer: Is the summary clear, accurate, and does it capture the main strengths? "
        "If yes, say True. If not, say False and explain what is missing."
    )
    messages = [
        {"role": "system", "content": validation_prompt},
        {"role": "user", "content": f"Profile: {profile_text}\nSummary: {summary}"},
    ]
    result = llm.with_structured_output(ReflectionValidator).invoke(messages)
    print(f"Validator: {result.reason}")
    return result.is_good

# Main reflection loop
def run_linkedin_reflection_loop(url: str, max_attempts: int = 3):
    profile_text = fetch_linkedin_profile(url)
    for attempt in range(max_attempts):
        print(f"\n--- Attempt {attempt+1} ---")
        summary = linkedin_summarizer_agent(url)
        print(f"Summary: {summary}")
        if reflection_validator(summary, profile_text):
            print("\nFinalized Summary:")
            print(summary)
            return summary
        print("Summary not good enough, retrying...\n")
    print("\nMax attempts reached. Returning last summary:")
    print(summary)
    return summary

if __name__ == "__main__":
    # --- Test the agent with the provided LinkedIn URL ---
    run_linkedin_reflection_loop("https://www.linkedin.com/in/deepakyadlapalli/") 