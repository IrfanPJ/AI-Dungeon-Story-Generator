import requests
from genres import GENRES

def generate_story(prompt, genre, num_samples=1):
    prefix = GENRES.get(genre, "")
    full_prompt = prefix + "\n" + prompt.strip()
    stories = []

    for _ in range(num_samples):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",   # Model name as string, e.g. "llama3"
                "prompt": full_prompt,
                "stream": False,
                "options": { "num_predict": 200 }
            }
        )

        try:
            data = response.json()
        except Exception as e:
            print("Failed to parse JSON response:", e)
            return ["Error: Failed to parse response from Ollama API"]

        if "response" not in data:
            print("Unexpected API response:", data)
            return ["Error: Invalid response from Ollama API"]

        stories.append(data["response"].strip())

    return stories
