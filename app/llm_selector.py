import os
from langchain_openai import ChatOpenAI


def get_llm(model: str = "gpt-4o-mini"):
    api_key = os.getenv("APIFREE_API_KEY")
    base_url = os.getenv("APIFREE_BASE_URL", "https://api.openai.com/v1")
    
    if not api_key:
        raise ValueError("APIFREE_API_KEY não configurada no arquivo .env")
    
    print(f"[LLM] Usando base_url: {base_url}")
    print(f"[LLM] Modelo: {model}")
    
    # Configuração mais robusta para lidar com APIs não-oficiais
    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        max_tokens=2048,
        timeout=30,
        max_retries=2,
        # Não incluir stream_options para APIs não oficiais
        # model_kwargs={}
    )
    
    return llm
