from fastapi import FastAPI
from app.schemas.chat import ChatRequest, ChatResponse
from app.ai.chat import generate_reply
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()


origins = [
    "https://akofisher.github.io",
    "https://www.akofisher.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)



app = FastAPI(title="AI Chatbot API")

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    reply = generate_reply(payload.message)
    return {"reply": reply}
