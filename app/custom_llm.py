"""
Cliente customizado para APIFREE.AI que contorna incompatibilidades com LangChain
"""
import os
import requests
from typing import Dict, List, Optional


class APIFreeLLM:
    """Cliente customizado para APIFREE.AI"""
    
    def __init__(self, model: str = "openai/gpt-5-mini", temperature: float = 0.7, max_tokens: int = 2048):
        self.api_key = os.getenv("APIFREE_API_KEY")
        self.base_url = os.getenv("APIFREE_BASE_URL", "https://apifree.ai/v1")
        
        # APIFREE usa formato "openai/modelo" ou apenas "modelo"
        # Se o modelo não tiver prefixo, adicionar "openai/"
        if "/" not in model:
            self.model = f"openai/{model}"
        else:
            self.model = model
            
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.api_key:
            raise ValueError("APIFREE_API_KEY não configurada")
        
        print(f"[CUSTOM_LLM] Inicializado com base_url: {self.base_url}")
        print(f"[CUSTOM_LLM] Modelo original: {model}")
        print(f"[CUSTOM_LLM] Modelo formatado: {self.model}")
    
    def invoke(self, messages: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Faz chamada direta à API APIFREE
        
        Args:
            messages: Lista de mensagens no formato [{"role": "system/user/assistant", "content": "..."}]
        
        Returns:
            Dict com 'content', 'total_tokens' e 'cost'
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        print(f"[CUSTOM_LLM] Fazendo requisição para: {url}")
        print(f"[CUSTOM_LLM] Headers: {headers}")
        print(f"[CUSTOM_LLM] Payload: {payload}")
        
        response = None
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            print(f"[CUSTOM_LLM] Status code: {response.status_code}")
            print(f"[CUSTOM_LLM] Response headers: {dict(response.headers)}")
            print(f"[CUSTOM_LLM] Response text (primeiros 500 chars): {response.text[:500]}")
            
            response.raise_for_status()
            
            # Verificar se a resposta tem conteúdo antes de tentar parsear JSON
            if not response.text or response.text.strip() == "":
                raise ValueError("API retornou resposta vazia")
            
            data = response.json()
            print(f"[CUSTOM_LLM] Resposta JSON: {str(data)[:300]}...")
            
            # Verificar se há erro na resposta
            if "error" in data:
                error_msg = data["error"].get("message", "Erro desconhecido")
                error_code = data["error"].get("code", "unknown")
                raise ValueError(f"API Error [{error_code}]: {error_msg}")
            
            # Extrair conteúdo da resposta
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                
                # Extrair informações de uso (tokens e custo)
                usage_info = {
                    'content': content,
                    'total_tokens': None,
                    'cost': None
                }
                
                if "usage" in data:
                    usage = data["usage"]
                    usage_info['total_tokens'] = usage.get("total_tokens")
                    
                    # Calcular custo aproximado se houver informação de tokens
                    # (valores aproximados, ajuste conforme necessário)
                    if usage_info['total_tokens']:
                        # Exemplo: $0.002 por 1K tokens (ajuste conforme seu modelo)
                        usage_info['cost'] = (usage_info['total_tokens'] / 1000) * 0.002
                
                print(f"[CUSTOM_LLM] Usage info: {usage_info}")
                return usage_info
            else:
                raise ValueError(f"Formato de resposta inesperado: {data}")
                
        except requests.exceptions.HTTPError as e:
            print(f"[CUSTOM_LLM HTTP ERROR] Status: {response.status_code}")
            print(f"[CUSTOM_LLM HTTP ERROR] Response: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"[CUSTOM_LLM REQUEST ERROR] {str(e)}")
            raise
        except ValueError as e:
            print(f"[CUSTOM_LLM VALUE ERROR] {str(e)}")
            print(f"[CUSTOM_LLM] Response text era: {response.text if 'response' in locals() else 'N/A'}")
            raise
        except Exception as e:
            print(f"[CUSTOM_LLM ERROR] {str(e)}")
            import traceback
            traceback.print_exc()
            raise
