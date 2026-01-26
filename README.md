# AI Agent API

## Deploy no Render

1. Criar Web Service
2. Conectar repositório
3. Configurar variável de ambiente: `GOOGLE_API_KEY`
4. Deploy automático

## Executar localmente

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY=sua_chave
uvicorn app.main:app --reload --port 10000
```

## Endpoint

POST /chat

```json
{
  "message": "crie um post sobre IA",
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
