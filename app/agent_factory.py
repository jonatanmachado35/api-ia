from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.llm_selector import get_llm
from app.prompts import get_base_prompt


def build_agent(agent_type: str, persona: Dict[str, str], rules: List[str], model: str = "gpt-4o-mini"):
    llm = get_llm(model=model)
    
    base_prompt = get_base_prompt(agent_type)
    
    persona_description = f"""
Tom: {persona.get('tone', 'neutro')}
Estilo: {persona.get('style', 'padrão')}
Foco: {persona.get('focus', 'geral')}
"""
    
    rules_text = "\n".join([f"- {rule}" for rule in rules])
    
    system_message = f"""{base_prompt}

PERSONA:
{persona_description}

REGRAS OBRIGATÓRIAS:
{rules_text}

Responda sempre seguindo a persona e as regras acima.
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    return chain
