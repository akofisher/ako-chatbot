import os
from openai import OpenAI
from langdetect import detect
from app.ai.persona import PERSONA

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation = []

def detect_language(text: str) -> str:
    try:
        return "Georgian" if detect(text) == "ka" else "English"
    except:
        return "English"

def generate_reply(message: str) -> str:
    user_lang = detect_language(message)

    conversation.append({"role": "user", "content": message})

    messages = [
        {"role": "system", "content": PERSONA},
        *conversation[-6:]  # ბოლო 3 კითხვა/პასუხი
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,
        max_tokens=300,
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    return reply
