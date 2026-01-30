#!/bin/bash

# Script para testar a API localmente

PORT=${1:-8000}
BASE_URL="http://localhost:${PORT}"

echo "🔍 Testando API em ${BASE_URL}"
echo ""

# Teste 1: Health Check
echo "1️⃣ Health Check (GET /)"
curl -s "${BASE_URL}/" | jq '.' || echo "❌ Falhou"
echo ""
echo ""

# Teste 2: Chat Endpoint
echo "2️⃣ Chat Endpoint (POST /chat)"
curl -X POST "${BASE_URL}/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá, como vai?",
    "agent": {
      "type": "Assistente Virtual",
      "persona": {
        "tone": "Profissional",
        "style": "Formal",
        "focus": "Secretaria"
      },
      "rules": ["Seja breve e objetivo"]
    },
    "model": "gpt-4o-mini"
  }' | jq '.' 2>/dev/null || echo "❌ Falhou - Verifique se o servidor está rodando e o .env configurado"

echo ""
echo ""
echo "✅ Teste concluído!"
