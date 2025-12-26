from .model import load_model, tokenizer, model
from .persona import PERSONA
import torch
from langdetect import detect

conversation = []

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        if lang == "ka":
            return "Georgian"
        else:
            return "English"
    except:
        return "English"

def generate_reply(message: str) -> str:
    load_model()

    conversation.append(f"User: {message}")

    user_lang = detect_language(message)

    prompt = f"""
{PERSONA}

Conversation:
{chr(10).join(conversation)}

Assistant ({user_lang}):
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=220,
            temperature=0.6,
            do_sample=True
        )

    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Get the part after "Assistant"
    reply = reply.split("Assistant")[-1].split(":")[-1].strip()

    conversation.append(f"Assistant: {reply}")
    return reply
