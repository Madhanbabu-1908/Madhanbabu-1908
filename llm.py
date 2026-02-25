import os
from dotenv import load_dotenv
import litellm

load_dotenv()

def generate_response(prompt):
    api_key = os.getenv("LITELLM_API_KEY")

    if not api_key:
        raise ValueError("API KEY NOT FOUND")

    response = litellm.completion(
        model="openrouter/openai/gpt-4o-mini",
        api_key=api_key,
        api_base="https://openrouter.ai/api/v1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "My App"
        }
    )

    return response["choices"][0]["message"]["content"]
