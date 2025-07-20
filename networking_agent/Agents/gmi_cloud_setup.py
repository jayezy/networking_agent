import requests
import json

class GMICloudClient:
    def __init__(self, api_key, model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"):
        self.url = "https://api.gmi-serving.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.model = model

    @staticmethod
    def create_message(role, content):
        return {"role": role, "content": content}

    def build_payload(self, system_prompt, user_prompt, temperature=1, max_tokens=500):
        messages = [
            self.create_message("system", system_prompt),
            self.create_message("user", user_prompt)
        ]
        return {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

    def send_chat_completion(self, system_prompt, user_prompt, temperature=1, max_tokens=500):
        payload = self.build_payload(system_prompt, user_prompt, temperature, max_tokens)
        response = requests.post(self.url, headers=self.headers, json=payload)
        return payload, response

    @staticmethod
    def pretty_print_request_response(payload, response):
        print("Request payload:")
        print(json.dumps(payload, indent=2))
        print("\nResponse:")
        print(json.dumps(response.json(), indent=2))

# Example usage:
if __name__ == "__main__":
    api_key = ""
    client = GMICloudClient(api_key)
    system_prompt = "You are a helpful AI assistant that helps connect people based on their interests. "
    user_prompt = "User is interested in travel. suggest 3 citites that are must visit before age 30"
    payload, response = client.send_chat_completion(system_prompt, user_prompt)
    client.pretty_print_request_response(payload, response)
