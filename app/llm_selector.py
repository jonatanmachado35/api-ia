import os
from langchain_openai import ChatOpenAI


def get_llm(model: str = "gpt-4o-mini"):
    api_key = os.getenv("APIFREE_API_KEY", "default")
    base_url = os.getenv("APIFREE_BASE_URL", "https://apifree.ai/v1")
    
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        max_tokens=2048
    )
