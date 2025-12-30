@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Calendário Gestão 2026/A
echo ============================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não está instalado ou não está no PATH!
    echo.
    echo Baixe Python em: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo [1/4] Verificando Python...
python --version
echo.

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo [2/4] Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERRO ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
    echo.
) else (
    echo [2/4] Ambiente virtual já existe, pulando...
    echo.
)

REM Ativar ambiente virtual
echo [3/4] Ativando ambiente virtual e instalando dependências...
call venv\Scripts\activate.bat

REM Instalar dependências
pip install -q flask flask-cors python-dotenv pillow
if errorlevel 1 (
    echo ERRO ao instalar dependências!
    pause
    exit /b 1
)
echo Dependências instaladas com sucesso!
echo.

REM Executar servidor
echo [4/4] Iniciando servidor...
echo.
echo ============================================================
echo Servidor iniciado com sucesso!
echo ============================================================
echo.
echo Acesse o site em:
echo   Site Principal: http://localhost:5000
echo   Painel Admin:   http://localhost:5000/admin
echo.
echo Pressione CTRL+C para parar o servidor
echo ============================================================
echo.

python app.py

pause
