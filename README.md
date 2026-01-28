# AI Agent API

## Deploy no Render

1. Criar Web Service
2. Conectar repositório
3. Configurar variáveis de ambiente:
   - `APIFREE_API_KEY`
   - `APIFREE_BASE_URL` (opcional, padrão: https://apifree.ai/v1)
4. Deploy automático

## Executar localmente

```bash
pip install -r requirements.txt
export APIFREE_API_KEY=sua_chave
uvicorn app.main:app --reload --port 10000
```

## Endpoint

POST /chat

```json
{
  "message": "crie um post sobre IA",
  "model": "gpt-4o-mini",
  "agent": {
    "type": "social_media",
    "persona": {
      "tone": "irreverente",
      "style": "creator",
      "focus": "reels"
    },
    "rules": [
      "usar linguagem simples",
      "sempre sugerir CTA"
    ]
  }
}
```

## Modelos disponíveis

Qualquer modelo suportado por apifree.ai:
- gpt-4o-mini
- gpt-4o
- claude-3-5-sonnet
- gemini-2.0-flash
- etc.
