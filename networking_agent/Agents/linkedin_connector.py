"""
linkedin_connector.py

This module provides a connector for interacting with LinkedIn, such as automating login, scraping, or sending messages.
"""
from playwright.sync_api import sync_playwright
import os
from gmi_cloud_setup import GMICloudClient
from exa_py import Exa
import re, json as pyjson

class LinkedInConnector:
    """A class to handle LinkedIn automation and API interactions."""

    def __init__(self, gmi_api_key=None):
        self.gmi_client = None
        if gmi_api_key:
            self.gmi_client = GMICloudClient(gmi_api_key)

    def exa_connect(self):
        """Establish a connection to the Exa service (placeholder)."""
        exa = Exa(api_key = "ea1a10d3-ad06-4ed1-a2bb-1532fd6507b3")
        return exa

    def exa_extract_contents(self, profile_url: str):
        exa = self.exa_connect()
        result = exa.get_contents(
            [profile_url],
            text = True,
        )
        return result

    def generate_user_prompt(self, user_scraped_linkedin_profile):
        return '''
        You are given raw LinkedIn profile data scraped from a user's public profile. This includes professional summaries, current and past roles, education, skills, and other relevant details.

        ## Input:
        {user_scraped_linkedin_profile}

        ## Task:
        Convert the above profile into a structured JSON object using the schema below. Follow these specific instructions for each key:

        - `name`: Full name of the user.
        - `summary`: A concise text summary (max 250 words) capturing the essence of the user’s background. Do not add any bullet points.
        - `interests`: A list of professional/technical interests, each with:
            - `skill`: The name of the interest or technology.
            - `proficiency_score`: A float between 0 and 1. Base this on endorsements, project usage, or frequency of mention.
        - `experience`: List of roles including:
            - `company`, `position`, `start_date`, `end_date`,`description`
        - `education`: List of educational qualifications with:
            - `school`, `degree`, `start_date`, `end_date`, `description`
        - `projects`: List of notable projects with:
            - `name`, `position`, `start_date`, `end_date`, `description`

        ## Output Format:
        Make sure the output is valid JSON in the exact format provided below. Do not add any thinking messages.
        ```json
        {{
            "name": "John Doe",
            "summary": "A text summary of the profile.",
            "interests": [
                {{
                "skill": "python",
                "proficiency_score": 0.85,
                }},
            ],
            "experience": [
                {{
                "company": "name of the company",
                "position": "Software Engineer",
                "start_date": "Jun 2022",
                "end_date": "Jan 2024",
                "description": "Worked on the Google Search Home team.",
                }},
            ],
            "education": [
                {{
                "school": "University of Minnesota",
                "degree": "Bachelor of Engineering",
                "start_date": "Aug 2018",
                "end_date": "May 2022",
                "description": "Major in Computer Science.",
                }},
            ],
            "projects": [
                {{
                "name": "project name",
                "position": "position",
                "start_date": "Jun 2022",
                "end_date": "Jan 2024",
                "description": "Built a standalone sentiment analysis app.",
                }},
            ],
        }}
        '''.format(user_scraped_linkedin_profile=user_scraped_linkedin_profile)

    def scrape_profile(self, profile_url: str):
        """Scrape data from a LinkedIn profile and extract structured JSON using LLM."""
        if not self.gmi_client:
            print("GMICloudClient is not initialized. Please provide an API key.")
            return None
        contents = self.exa_extract_contents(profile_url)
        print("Contents: ", contents)

        # Define prompts
        system_prompt = "You are an expert at extracting structured data from JSON."
        user_prompt = self.generate_user_prompt(contents)
        payload, response = self.gmi_client.send_chat_completion(system_prompt, user_prompt)
        self.gmi_client.pretty_print_request_response(payload, response)
        llm_response = response.json()
        print("llm_response: ", llm_response)
        content = llm_response.get('choices', [{}])[0].get('message', {}).get('content', '')
        extracted_json = self.extract_json_from_llm_output(content)
        return extracted_json

    @staticmethod
    def extract_json_from_llm_output(content):
        """
        Extract the first JSON object from LLM output, handling code blocks and plain JSON.
        Returns the parsed JSON object or None if not found/parsable.
        """
        import re, json as pyjson
        # Try to extract any JSON object in a code block
        match = re.search(r'```json[\s\S]*?(\{[\s\S]*?\})[\s\S]*?```', content)
        if not match:
            # Fallback: try to extract any JSON object
            match = re.search(r'(\{[\s\S]*?\})', content)
        if match:
            try:
                return pyjson.loads(match.group(1))
            except Exception as e:
                print(f"Error parsing extracted JSON: {e}")
                return None
        print("No JSON object found in LLM response.")
        return None

# Example usage (uncomment and set your API key to use):
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImM1NzIwNWE5LWViZTItNDM1OC04ODUyLTdmZjNmYzg0ZWMzZSIsInR5cGUiOiJpZV9tb2RlbCJ9.7l-bOTyW6kcD6mmj4zcdbtW-DBpH00BPcP3gZui4umI"
linkedin_connector = LinkedInConnector(gmi_api_key=api_key)
extracted_user_profile_json = linkedin_connector.scrape_profile("https://www.linkedin.com/in/agrawalrinkal/")

print("extracted_user_profile_json: ", extracted_user_profile_json)