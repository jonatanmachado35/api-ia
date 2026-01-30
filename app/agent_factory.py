from typing import Dict, List
from app.custom_llm import APIFreeLLM
from app.prompts import get_base_prompt


def build_agent(agent_type: str, persona: Dict[str, str], rules: List[str], model: str = "openai/gpt-5-mini"):
    """
    Constrói um agente usando cliente HTTP customizado para APIFREE
    """
    llm = APIFreeLLM(model=model)
    
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
    
    # Criar uma função que monta as mensagens e invoca o LLM
    def invoke(input_data: Dict[str, str]) -> Dict[str, any]:
        user_message = input_data.get("input", "")
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        # llm.invoke agora retorna dict com 'content', 'total_tokens', 'cost'
        result = llm.invoke(messages)
        
        return {
            'response': result.get('content', ''),
            'cost': result.get('cost'),
            'total_tokens': result.get('total_tokens')
        }
    
    # Criar um objeto que simula a interface do LangChain
    class SimpleChain:
        def invoke(self, input_data):
            return invoke(input_data)
    
    return SimpleChain()
