@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual .venv ...
    py -m venv .venv
    if errorlevel 1 (
        echo No se pudo crear el entorno virtual. Instala Python 3.10+.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\streamlit.exe" (
    echo Instalando dependencias ...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Fallo la instalacion de dependencias.
        pause
        exit /b 1
    )
)

echo Iniciando EstaticaBot en http://localhost:8501 ...
".venv\Scripts\python.exe" -m streamlit run app.py

endlocal
