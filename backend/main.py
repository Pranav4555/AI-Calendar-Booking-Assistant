from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    print(f"Query received: {request.query}")
    try:
        response = run_agent(request.query)
        print(f"Agent response: {response}")
        return {"response": response}
    except Exception as e:
        print(f"Error: {e}")
        return {"response": "Error occurred"}
