#!/bin/bash

# Script para executar o servidor do Calendário Gestão 2026/A

echo "=========================================="
echo "Calendário Gestão 2026/A"
echo "=========================================="
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -q flask flask-cors python-dotenv pillow

# Executar servidor
echo ""
echo "=========================================="
echo "Iniciando servidor..."
echo "=========================================="
echo ""
echo "Acesse o site em: http://localhost:5000"
echo "Painel de Admin: http://localhost:5000/admin"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo "=========================================="
echo ""

python3 app.py
