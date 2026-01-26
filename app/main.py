from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from app.agent_factory import build_agent

app = FastAPI(title="AI Agent API")


class Persona(BaseModel):
    tone: str
    style: str
    focus: str


class Agent(BaseModel):
    type: str
    persona: Persona
    rules: List[str]


class ChatRequest(BaseModel):
    message: str
    agent: Agent


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        print(f"[REQUEST] message: {request.message[:100]}...")
        print(f"[REQUEST] agent_type: {request.agent.type}")
        
        chain = build_agent(
            agent_type=request.agent.type,
            persona=request.agent.persona.model_dump(),
            rules=request.agent.rules
        )

        response = chain.invoke({"input": request.message})
        
        print(f"[RESPONSE] length: {len(response)}")
        print(f"[RESPONSE] content: {response[:200]}...")

        return ChatResponse(response=response)

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
