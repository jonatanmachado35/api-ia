from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from app.llm_selector import get_llm
from app.prompts import get_base_prompt


def extract_response_and_usage(ai_message):
    """Extrai o conteúdo e metadados de uso da resposta da LLM"""
    # Garantir que ai_message não é None ou string
    if ai_message is None:
        return {'response': '', 'cost': None, 'total_tokens': None}
    
    if isinstance(ai_message, str):
        return {'response': ai_message, 'cost': None, 'total_tokens': None}
    
    # Extrair conteúdo
    content = ai_message.content if hasattr(ai_message, 'content') else str(ai_message)
    
    # Garantir que content é string
    if not isinstance(content, str):
        content = str(content)
    
    # Tentar extrair usage_metadata do response_metadata
    usage_data = {'cost': None, 'total_tokens': None}
    
    if hasattr(ai_message, 'response_metadata'):
        response_metadata = ai_message.response_metadata
        
        # Verificar se existe usage no response_metadata
        if isinstance(response_metadata, dict):
            if 'usage' in response_metadata:
                usage = response_metadata['usage']
                usage_data['cost'] = usage.get('cost')
                usage_data['total_tokens'] = usage.get('total_tokens')
            # Ou token_usage (dependendo do provider)
            elif 'token_usage' in response_metadata:
                token_usage = response_metadata['token_usage']
                usage_data['cost'] = token_usage.get('cost')
                usage_data['total_tokens'] = token_usage.get('total_tokens')
    
    # Também verificar usage_metadata direto
    if hasattr(ai_message, 'usage_metadata') and ai_message.usage_metadata:
        usage_metadata = ai_message.usage_metadata
        if isinstance(usage_metadata, dict):
            if not usage_data['total_tokens'] and 'total_tokens' in usage_metadata:
                usage_data['total_tokens'] = usage_metadata['total_tokens']
            if not usage_data['cost'] and 'cost' in usage_metadata:
                usage_data['cost'] = usage_metadata['cost']
    
    return {
        'response': content,
        'cost': usage_data['cost'],
        'total_tokens': usage_data['total_tokens']
    }


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
    
    # Chain que retorna o AIMessage completo com metadados
    chain = prompt | llm | RunnableLambda(extract_response_and_usage)
    
    return chain
