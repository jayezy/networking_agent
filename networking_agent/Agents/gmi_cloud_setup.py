import requests
import json

url = "https://api.gmi-serving.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImM1NzIwNWE5LWViZTItNDM1OC04ODUyLTdmZjNmYzg0ZWMzZSIsInR5cGUiOiJpZV9tb2RlbCJ9.7l-bOTyW6kcD6mmj4zcdbtW-DBpH00BPcP3gZui4umI"
}

payload = {
    "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    "messages": [
        {"role": "system", "content": "You are a helpful AI assistant that helps connect people based on their interests. "},
        {"role": "user", "content": "User is interested in travel. suggest 3 citites that are must visit before age 30"}
    ],
    "temperature": 1,
    "max_tokens": 500
}

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2))
