#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def criar_venv():
    """Cria o ambiente virtual se não existir."""
    venv_path = Path('venv')
    if not venv_path.exists():
        print("[1/4] Criando ambiente virtual...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("✓ Ambiente virtual criado com sucesso!")
    else:
        print("[1/4] Ambiente virtual já existe, pulando...")
    print()

def instalar_dependencias():
    """Instala as dependências necessárias."""
    print("[2/4] Instalando dependências...")
    
    if sys.platform == 'win32':
        pip_path = Path('venv/Scripts/pip.exe')
    else:
        pip_path = Path('venv/bin/pip')
    
    try:
        subprocess.run([str(pip_path), 'install', '-q', 'flask', 'flask-cors', 'python-dotenv', 'pillow'], check=True)
        print("✓ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar dependências!")
        sys.exit(1)
    print()

def iniciar_servidor():
    """Inicia o servidor Flask."""
    print("[3/4] Iniciando servidor...")
    print()
    print("=" * 60)
    print("Calendário Gestão 2026/A")
    print("=" * 60)
    print()
    print("Servidor iniciado com sucesso!")
    print()
    print("Acesse em:")
    print("  Site Principal: http://localhost:5000")
    print("  Painel Admin:   http://localhost:5000/admin")
    print()
    print("Pressione CTRL+C para parar o servidor")
    print("=" * 60)
    print()
    
    # Aguardar um pouco antes de abrir o navegador
    time.sleep(2)
    
    # Abrir navegador automaticamente
    print("[4/4] Abrindo navegador...")
    webbrowser.open('http://localhost:5000')
    
    # Executar o servidor
    if sys.platform == 'win32':
        python_path = Path('venv/Scripts/python.exe')
    else:
        python_path = Path('venv/bin/python')
    
    subprocess.run([str(python_path), 'app.py'])

def main():
    """Função principal."""
    print()
    print("=" * 60)
    print("Calendário Gestão 2026/A - Inicializador")
    print("=" * 60)
    print()
    
    try:
        criar_venv()
        instalar_dependencias()
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\n\nServidor parado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
