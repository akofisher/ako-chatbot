from .model import load_model, tokenizer, model
from .persona import PERSONA
import torch
from langdetect import detect
from collections import deque

# ✅ ლიმიტირებული conversation (მეხსიერების დაცვა)
conversation = deque(maxlen=6)  # ბოლო 6 შეტყობინება

# ✅ model იტვირთება ერთხელ
load_model()


def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return "Georgian" if lang == "ka" else "English"
    except:
        return "English"


def generate_reply(message: str) -> str:
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
            max_new_tokens=120,     # ⬇️ შემცირებული (ძალიან მნიშვნელოვანია)
            temperature=0.6,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # მხოლოდ assistant პასუხის ამოღება
    reply = full_text.split("Assistant")[-1].split(":")[-1].strip()

    conversation.append(f"Assistant: {reply}")
    return reply
