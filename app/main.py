from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.chat import ChatRequest, ChatResponse
from app.ai.chat import generate_reply

app = FastAPI(title="AI Chatbot API")


origins = [
    "http://localhost:5173",       
    "https://akofisher.github.io", 
    "https://www.akofisher.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    reply = generate_reply(payload.message)
    return {"reply": reply}
