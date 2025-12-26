from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.chat import ChatRequest, ChatResponse
from app.ai.chat import generate_reply

app = FastAPI(title="AI Chatbot API")

# Allow requests from your frontend
origins = [
    "http://localhost:5173",
    "https://akofisher.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for testing
@app.get("/")
def root():
    return {"message": "AI Chatbot API is running!"}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        reply = generate_reply(payload.message)
        return {"reply": reply}
    except Exception as e:
        # Log the exception for debugging
        print(f"Error in /chat: {e}")
        # Return safe error response
        raise HTTPException(status_code=500, detail="Internal Server Error")
