from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
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
    model: Optional[str] = "gpt-4o-mini"


class ChatResponse(BaseModel):
    response: str
    cost: Optional[float] = None
    total_tokens: Optional[int] = None


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        print(f"[REQUEST] message: {request.message[:100]}...")
        print(f"[REQUEST] agent_type: {request.agent.type}")
        print(f"[REQUEST] model: {request.model}")
        
        chain = build_agent(
            agent_type=request.agent.type,
            persona=request.agent.persona.model_dump(),
            rules=request.agent.rules,
            model=request.model
        )

        result = chain.invoke({"input": request.message})
        
        # Garantir que result é sempre um dicionário
        if not isinstance(result, dict):
            result = {"response": str(result), "cost": None, "total_tokens": None}
        
        response_text = result.get("response", str(result))
        cost = result.get("cost")
        total_tokens = result.get("total_tokens")
        
        # Garantir que response_text é uma string
        if not isinstance(response_text, str):
            response_text = str(response_text)
        
        print(f"[RESPONSE] length: {len(response_text)}")
        print(f"[RESPONSE] content: {response_text[:200]}...")
        if cost is not None:
            print(f"[USAGE] cost: {cost}, total_tokens: {total_tokens}")

        return ChatResponse(
            response=response_text,
            cost=cost,
            total_tokens=total_tokens
        )

    except Exception as e:
        error_message = str(e).lower()
        print(f"[ERROR] {str(e)}")
        
        if any(keyword in error_message for keyword in ["quota", "limit", "resource_exhausted", "429"]):
            raise HTTPException(
                status_code=429,
                detail="Limite de créditos da API excedido. Tente novamente mais tarde."
            )
        
        raise HTTPException(status_code=500, detail=str(e))
