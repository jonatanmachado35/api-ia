# AI Agent API

## Configuração Local

### 1. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais:

```env
APIFREE_API_KEY=sua_chave_aqui
APIFREE_BASE_URL=https://apifree.ai/v1
```

### 4. Rodar localmente

**Opção 1: Script automatizado**
```bash
./run_local.sh
```

**Opção 2: Comando manual**
```bash
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API disponível em:
- Servidor: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/`

## Deploy no Render

1. Criar Web Service
2. Conectar repositório
3. Configurar variáveis de ambiente:
   - `APIFREE_API_KEY`
   - `APIFREE_BASE_URL` (opcional, padrão: https://apifree.ai/v1)
4. Deploy automático

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
