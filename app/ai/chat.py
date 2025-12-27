# app/ai/chat.py
import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_reply(message: str) -> str:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://akofisher.github.io",
            "X-Title": "Ako Portfolio Chatbot",
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            "temperature": 0.6,
            "max_tokens": 200,
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]
