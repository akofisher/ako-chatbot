import os
import requests
from app.ai.persona import PERSONA

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_reply(message: str) -> str:
    response = requests.post(
        "https://api.openrouter.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": PERSONA},
                {"role": "user", "content": message},
            ],
        },
        timeout=20,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
