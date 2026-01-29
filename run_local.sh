#!/bin/bash

# Script para rodar a API localmente

# Ativar ambiente virtual
source venv/bin/activate

# Rodar o servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
